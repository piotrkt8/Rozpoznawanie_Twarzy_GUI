# camera_live.py
import cv2
import joblib
import os
import numpy as np
from PIL import Image
from typing import Optional, Tuple, List, Any

# Importy własne
from vggface_recognizer import extract_embeddings_batch
from haar_detector import detect_faces_opencv

MODEL_PATH = os.path.join('results', 'logreg_model.pkl')

class FaceRecognitionCamera:
    """Obsługa kamery i integracja z modelem rozpoznawania."""

    def __init__(self, cam_id: int = 0):
        """
        Inicjalizuje kamerę i ładuje model ML.
        
        Args:
            cam_id (int): ID urządzenia wideo (zazwyczaj 0).
        """
        self.clf: Any = None
        
        if os.path.exists(MODEL_PATH):
            try:
                self.clf = joblib.load(MODEL_PATH)
                print(f"[INFO] Model załadowany z {MODEL_PATH}")
            except Exception:
                print("[WARN] Model uszkodzony.")
        else:
            print("[WARN] Brak pliku modelu. Tryb tylko detekcji.")

        self.cap = cv2.VideoCapture(cam_id)
        if not self.cap.isOpened():
            raise RuntimeError("Nie można uruchomić kamery.")

    def get_frame(self) -> Optional[np.ndarray]:
        """Zwraca surową klatkę z kamery."""
        ret, frame = self.cap.read()
        return frame if ret else None

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Tuple[str, float, int, int, int, int]]]:
        """
        Przetwarza klatkę: wykrywa twarze, generuje embeddingi i klasyfikuje.

        Args:
            frame (np.ndarray): Klatka wejściowa.

        Returns:
            Tuple: (Obraz z ramkami, Lista detekcji [label, conf, x, y, w, h])
        """
        frame_resized = cv2.resize(frame, (400, 400))
        detections = []
        
        # Detekcja (łagodna)
        faces = detect_faces_opencv(frame_resized, minNeighbors=4, scaleFactor=1.1)

        # Jeśli brak modelu, tylko rysuj ramki "BRAK MODELU"
        if self.clf is None:
            # Próba hot-reload
            if os.path.exists(MODEL_PATH):
                try:
                    self.clf = joblib.load(MODEL_PATH)
                except:
                    pass
            
            if self.clf is None:
                for (x, y, w, h) in faces:
                     cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 0, 255), 2)
                     cv2.putText(frame_resized, "BRAK MODELU", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                return frame_resized, []

        # Właściwe rozpoznawanie
        for (x, y, w, h) in faces:
            face_roi = frame_resized[y:y + h, x:x + w]
            try:
                face_pil = Image.fromarray(cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)).resize((224, 224))
                embedding = extract_embeddings_batch([face_pil])

                if len(embedding) > 0:
                    prediction = self.clf.predict(embedding)[0]
                    probabilities = self.clf.predict_proba(embedding)[0]
                    pred_idx = self.clf.classes_.tolist().index(prediction)
                    confidence = probabilities[pred_idx]
                    label = prediction if confidence >= 0.5 else "Nieznany"
                else:
                    label = "Błąd"
                    confidence = 0.0

                detections.append((label, float(confidence), x, y, w, h))

                color = (0, 255, 0) if label != "Nieznany" else (0, 0, 255)
                text = f"{label} ({confidence*100:.1f}%)"
                cv2.rectangle(frame_resized, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame_resized, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            except Exception as e:
                print(f"[ERROR] {e}")

        return frame_resized, detections

    def release(self):
        self.cap.release()