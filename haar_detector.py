# haar_detector.py
import cv2
import numpy as np
from typing import List, Tuple

def detect_faces_opencv(
    img: np.ndarray, 
    scaleFactor: float = 1.2, 
    minNeighbors: int = 5, 
    minSize: Tuple[int, int] = (100, 100)
) -> List[Tuple[int, int, int, int]]:
    """
    Wykrywa twarze na obrazie przy użyciu kaskad Haara (OpenCV).

    Args:
        img (np.ndarray): Obraz wejściowy w formacie BGR lub Gray.
        scaleFactor (float): Parametr określający redukcję obrazu przy każdej skali.
        minNeighbors (int): Minimalna liczba sąsiadów prostokąta (czułość detekcji).
        minSize (Tuple[int, int]): Minimalny rozmiar wykrywanego obiektu.

    Returns:
        List[Tuple[int, int, int, int]]: Lista krotek (x, y, w, h) reprezentujących wykryte twarze.
    """
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        print("[ERROR] Błąd ładowania kaskady Haara.")
        return []

    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize
    )
    
    # Konwersja na listę krotek int
    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]