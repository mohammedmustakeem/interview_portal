import cv2
import base64
import numpy as np
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from ultralytics import YOLO
import mediapipe as mp
DISALLOWED_OBJECTS = {
    "cell phone", "laptop", "book", "tv",
    "remote", "watch"
}

PERSON_CLASS = "person"

# Tune these for speed vs accuracy tradeoff
CONSECUTIVE_FRAMES_THRESHOLD = 1   # ← was 3, now instant on first detection
INFERENCE_SIZE = 320               # ← was 640, 2x faster, slightly less accurate
CONFIDENCE = 0.35                  # ← slightly higher to reduce false positives at 320
mp_face_mesh = mp.solutions.face_mesh

class VisionService:

    _model = None  # Class-level singleton — model loads ONCE across all instances

    def __init__(self):
        if VisionService._model is None:
            print("Loading YOLO...")
            VisionService._model = YOLO("yolov8n.pt")  # ← nano, fastest model
            # Warm up the model so first real frame isn't slow
            dummy = np.zeros((320, 320, 3), dtype=np.uint8)
            VisionService._model(dummy, imgsz=INFERENCE_SIZE, verbose=False)
            print("YOLO loaded and warmed up.")
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.model = VisionService._model
        self.consecutive_counts = defaultdict(int)
        self.session_start = time.time()
        self.frame_times = []
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.start_time_up = None
        self.start_time_down = None
        self.look_threshold  = 1.0
        self.look_left_frames = 0
        self.look_right_frames = 0
        self.look_down_frames = 0
        self.look_up_frames = 0
        self.pitch_history = []
        self.yaw_history = []
        self.history_size = 5
        
        
    def _analyze_face(self, frame):
    
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
    
        warnings = []
    
        if not results.multi_face_landmarks:
            warnings.append(" No face detected")
            return warnings
    
        if len(results.multi_face_landmarks) > 1:
            warnings.append(" Multiple faces detected")
    
        for face_landmarks in results.multi_face_landmarks:
    
                # Nose landmark
                nose = face_landmarks.landmark[1]



                # Left eye
                left_eye = face_landmarks.landmark[33]
    
                # Right eye
                right_eye = face_landmarks.landmark[263]
    
                # Simple gaze estimation
                eye_diff = abs(left_eye.x - right_eye.x)
    
                if eye_diff > 0.35:
                    warnings.append(" Looking away from screen")
    
                    # Head position
                if nose.x < 0.25:
                    warnings.append(" Head turned left")
                if nose.x > 0.75:
                    warnings.append(" Head turned right")
                
        return warnings
    
    def _analyze_head_pose(self, frame):

        warnings = []
    
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
    
        if not results.multi_face_landmarks:
            warnings.append("No face detected")
            return warnings
    
        for face in results.multi_face_landmarks:
    
            landmarks = face.landmark
    
            # Key points
            image_points = np.array([
                (landmarks[1].x * w, landmarks[1].y * h),    # Nose
                (landmarks[152].x * w, landmarks[152].y * h), # Chin
                (landmarks[33].x * w, landmarks[33].y * h),   # Left eye
                (landmarks[263].x * w, landmarks[263].y * h), # Right eye
                (landmarks[61].x * w, landmarks[61].y * h),   # Left mouth
                (landmarks[291].x * w, landmarks[291].y * h)  # Right mouth
            ], dtype="double")
    
            # 3D model points
            model_points = np.array([
                (0.0, 0.0, 0.0),
                (0.0, -63.6, -12.5),
                (-43.3, 32.7, -26),
                (43.3, 32.7, -26),
                (-28.9, -28.9, -24.1),
                (28.9, -28.9, -24.1)
            ])
    
            focal_length = w
            center = (w / 2, h / 2)
    
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype="double")
    
            dist_coeffs = np.zeros((4,1))
    
            success, rotation_vector, translation_vector = cv2.solvePnP(
                model_points,
                image_points,
                camera_matrix,
                dist_coeffs
            )
    
            rmat, _ = cv2.Rodrigues(rotation_vector)
    
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    
            pitch, yaw, roll = angles
            pitch, yaw, roll = angles

            print("HEAD POSE RUNNING")
            print(f"Pitch={pitch:.2f}, Yaw={yaw:.2f}")
            # store history
            self.pitch_history.append(pitch)
            self.yaw_history.append(yaw)
            
            if len(self.pitch_history) > self.history_size:
                self.pitch_history.pop(0)
            
            if len(self.yaw_history) > self.history_size:
                self.yaw_history.pop(0)
            
            # moving average
            pitch = sum(self.pitch_history) / len(self.pitch_history)
            yaw = sum(self.yaw_history) / len(self.yaw_history)
            # Yaw → left/right
            # LEFT
            if abs(pitch) < 8:
                pitch = 0
            if abs(yaw) < 8:
                yaw = 0
                
                
            if yaw < -15:
                self.look_left_frames += 1
            else:
                self.look_left_frames = 0
            
            if self.look_left_frames >= 5:
                warnings.append("Looking left")
        
        
                # RIGHT
            if yaw > 15:
                self.look_right_frames += 1
            else:
                self.look_right_frames = 0
    
            if self.look_right_frames >= 5:
                warnings.append("Looking right")
    
    
                    # DOWN
            if pitch > 15:
                self.look_down_frames += 1
            else:
                self.look_down_frames = 0
                
            if self.look_down_frames >= 5:
                warnings.append("Looking down")
                    # UP
            if pitch < -15:
                self.look_up_frames += 1
            else:
                self.look_up_frames = 0
                
            if self.look_up_frames >= 5:
                warnings.append("Looking up")
                
        return warnings
    def _decode_frame(self, base64_string: str):
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        img_data = base64.b64decode(base64_string)
        np_arr = np.frombuffer(img_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    def _get_timing(self) -> dict:
        now = time.time()
        self.frame_times.append(now)
        if len(self.frame_times) > 30:
            self.frame_times.pop(0)

        fps = 0.0
        if len(self.frame_times) > 1:
            span = self.frame_times[-1] - self.frame_times[0]
            fps = round((len(self.frame_times) - 1) / span, 2) if span > 0 else 0.0

        return {
            "elapsed_seconds": round(now - self.session_start, 2),
            "fps": fps
        }

    def _run_inference(self, frame):
        """Pure inference — runs in thread pool to avoid blocking."""
        return self.model(
            frame,
            imgsz=INFERENCE_SIZE,  # 320 instead of 640
            conf=CONFIDENCE,
            verbose=False,
            half=True              # ← FP16 inference, ~2x faster on GPU
        )

    def _parse_results(self, results) -> tuple[list, int]:
        detections = []
        person_count = 0

        for r in results:
            for box in r.boxes:
                label = self.model.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                coords = box.xyxy[0].tolist()

                detections.append({
                    "label": label,
                    "confidence": round(confidence, 3),
                    "bbox": [round(c, 1) for c in coords]
                })

                if label == PERSON_CLASS:
                    person_count += 1

        return detections, person_count

    async def process_frame_async(self, base64_frame: str, phase: str) -> dict:
        """Async version — doesn't block your web server/event loop."""
        frame = self._decode_frame(base64_frame)
        if frame is None:
            return {"warnings": [], "detections": [], "timing": {}}

        timing = self._get_timing()

        # Run heavy inference in thread pool — won't block async event loop
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            self.executor,
            self._run_inference,
            frame
        )

        detections, person_count = self._parse_results(results)

        # Build issues immediately (threshold = 1 = instant)
        warnings = []
        face_warnings = self._analyze_face(frame)
        warnings.extend(face_warnings)
        
        pose_warnings = self._analyze_head_pose(frame)
        warnings.extend(pose_warnings)
        
        for det in detections:
            if det["label"] in DISALLOWED_OBJECTS:
                warnings.append(f" Prohibited object: {det['label']} ({det['confidence']:.0%})")

        if person_count == 0:
            warnings.append(" No person detected")
        elif person_count > 1:
            warnings.append(f" Multiple persons detected ({person_count})")

        return {
            "warnings": warnings,
            "detections": detections,
            "person_count": person_count,
            "phase": phase,
            "timing": timing
        }

    # # Sync wrapper if you're not using async
    # def process_frame(self, base64_frame: str, phase: str) -> dict:
    #     return asyncio.run(self.process_frame_async(base64_frame, phase))
