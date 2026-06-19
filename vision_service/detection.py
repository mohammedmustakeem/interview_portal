import cv2
import base64
import numpy as np
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import mediapipe as mp
import urllib.request
import tarfile
import os

MODEL_DIR   = os.path.join(os.path.expanduser("~"), ".cache", "mobilenet_ssd_coco")
PROTO_URL   = "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
WEIGHTS_URL = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"

COCO_PHONE_ID  = 77
COCO_PERSON_ID = 1

#  Resize all frames to this before any processing — 2x faster
PROCESS_WIDTH  = 480
PROCESS_HEIGHT = 360

def _ensure_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    proto   = os.path.join(MODEL_DIR, "ssd_mobilenet_v2_coco.pbtxt")
    weights = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
    if not os.path.exists(proto):
        print("Downloading prototxt...")
        urllib.request.urlretrieve(PROTO_URL, proto)
    if not os.path.exists(weights):
        tar_path = os.path.join(MODEL_DIR, "model.tar.gz")
        print("Downloading model (~180MB)...")
        urllib.request.urlretrieve(WEIGHTS_URL, tar_path)
        with tarfile.open(tar_path) as tar:
            for member in tar.getmembers():
                if member.name.endswith("frozen_inference_graph.pb"):
                    member.name = os.path.basename(member.name)
                    tar.extract(member, MODEL_DIR)
        os.remove(tar_path)
        print(" Model ready")
    return proto, weights


class VisionService:

    _net = None

    def __init__(self):
        if VisionService._net is None:
            proto, weights = _ensure_model()
            print("Loading SSD MobileNet...")
            net = cv2.dnn.readNetFromTensorflow(weights, proto)
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            VisionService._net = net
            print(" Model loaded")
        
        self.net = VisionService._net
        
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=2,          #
            refine_landmarks=False,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.4,
        )
        
        self.executor      = ThreadPoolExecutor(max_workers=1)  # 1 is enough, avoids context switching
        self.session_start = time.time()
        self.away_frames      = 0
        self.FRAME_THRESH     = 2
        
        self.phone_cache      = False   # last known result
        self.person_cache     = 0        # ← add
        self._last_face_count = 0
        self.phone_frame_skip = 0
        self.PHONE_EVERY_N    = 3       # run phone detection every 3 frames
        self.frame_count      = 0
        self.start_time       = time.time()
        
    def _decode_and_resize(self, b64: str):
        """Decode base64 and immediately resize — all processing on small frame."""
        if "," in b64:
            b64 = b64.split(",")[1]
        arr   = np.frombuffer(base64.b64decode(b64), np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return None
        return cv2.resize(frame, (PROCESS_WIDTH, PROCESS_HEIGHT))
    
    def _check_face(self, frame):
        
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
    
        if not results.multi_face_landmarks:
            self._last_face_count = 0
            return False, "Please stay on camera"
        
        self._last_face_count = len(results.multi_face_landmarks)
        
        if self._last_face_count > 1:
            return False, "Multiple people detected"
    
        lm = results.multi_face_landmarks[0].landmark
    
        nose     = lm[1]
        l_eye    = lm[33]
        r_eye    = lm[263]
        chin     = lm[152]
        forehead = lm[10]
    
        # Check 1: nose position in frame
        if not (0.20 < nose.x < 0.80 and 0.15 < nose.y < 0.85):
            return False, "Please stay on camera"
    
        # Check 2: eye symmetry (left/right turn detection)
        l_dist = abs(nose.x - l_eye.x)
        r_dist = abs(nose.x - r_eye.x)
        if l_dist < 0.01 or r_dist < 0.01:
            return False, "Please look at the camera"
        if max(l_dist, r_dist) / min(l_dist, r_dist) > 3.5:
            return False, "Please look at the camera"
    
        # Check 3: vertical gaze (up/down detection)
        face_h = abs(chin.y - forehead.y)
        if face_h < 0.01:
            return False, "Please look at the camera"
        if not (0.30 < (nose.y - forehead.y) / face_h < 0.75):
            return False, "Please look at the camera"
    
        return True, None
    
    def _run_phone_detection(self, frame):
       
        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=1.0,
            size=(300, 300),
            mean=(0, 0, 0),
            swapRB=True,
            crop=False
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        phone_detected = False
        person_count   = 0
        for i in range(detections.shape[2]):
            conf     = float(detections[0, 0, i, 2])
            class_id = int(detections[0, 0, i, 1])
            if conf < 0.50:
                continue
            if class_id == COCO_PHONE_ID:
               phone_detected = True
            if class_id == COCO_PERSON_ID:
                person_count += 1
         
        return phone_detected, person_count   
    
    def recalibrate(self):
        self.away_frames      = 0
        self.phone_cache      = False
        self.person_cache     = 0
        self._last_face_count = 0
        self.phone_frame_skip = 0
    def _get_timing(self):
       self.frame_count += 1
       elapsed = round(time.time() - self.session_start, 2)
       fps     = round(self.frame_count / elapsed, 2) if elapsed > 0 else 0.0
       return {"elapsed_seconds": elapsed, "fps": fps}
   
    async def process_frame_async(self, base64_frame: str, phase: str) -> dict:
        frame = self._decode_and_resize(base64_frame)
        if frame is None:
            return {"warnings": [], "timing": {}, "phase": phase}
    
        timing = self._get_timing()
        loop   = asyncio.get_event_loop()
        result = 0
        self.phone_frame_skip += 1
        if self.phone_frame_skip >= self.PHONE_EVERY_N:
            self.phone_frame_skip = 0
            phone, person  = await loop.run_in_executor(
                self.executor, self._run_phone_detection, frame
            )
            self.phone_cache  = phone    # bool — False or True
            self.person_cache = person
        face_ok, face_warning = self._check_face(frame)

        warnings = []

        if hasattr(self, '_last_face_count') and self._last_face_count > 1:
            warnings.append("Multiple people detected")
        elif hasattr(self, 'person_cache') and self.person_cache > 1:
            warnings.append("Multiple people detected")
        elif not face_ok:
            self.away_frames += 1
            if self.away_frames >= self.FRAME_THRESH:
                warnings.append(face_warning)
        else:
            self.away_frames = 0
        if self.phone_cache:
            warnings.append("Cell phone detected")
        return {
            "warnings":   warnings,
            "phase":      phase,
            "timing":     timing,
        }
