import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def _analyze_face(self, frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

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

