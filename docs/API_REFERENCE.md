# 📘 API_REFERENCE.md — Dokumentacja Funkcji i Klas

# 📦 API Reference – Dokumentacja Kodów  
**Face Recognition App (OpenCV + VGGFace + GUI)**  
Wersja: 1.0

---

# 1. Moduł `haar_detector.py`

## `detect_faces_opencv(img, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))`
Wykrywa twarze na obrazie przy użyciu kaskad Haar.

### Argumenty:
- **img (np.ndarray)** — obraz wejściowy  
- **scaleFactor (float)** — skala piramidy obrazu  
- **minNeighbors (int)** — czułość detekcji  
- **minSize (tuple)** — minimalny rozmiar twarzy  

### Zwraca:
Lista `(x, y, w, h)` wykrytych twarzy.

---

# 2. Moduł `vggface_recognizer.py`

## Stałe:
- **resnet** — model InceptionResnetV1 VGGFace2  
- **MODEL_PATH** — ścieżka: `results/logreg_model.pkl`  

---

## 2.1. `extract_embeddings_batch(images_pil)`
Zwraca embeddingi 512-D dla listy obrazów PIL.

### Zwraca:
`np.ndarray (N, 512)`

---

## 2.2. Klasa **VGGFaceRecognizer**

### `__init__(self)`
Tworzy struktury zapisowe modelu.

### `train(self, progress_callback=None)`
Trenuje Logistic Regression na danych z `faces/`.

### Zwraca:
Tekst statusu np. `"Model wytrenowany pomyślnie!"`

---

# 3. Moduł `camera_live.py`

## Klasa **FaceRecognitionCamera**

### `__init__(self, cam_id=0)`
Ładuje model ML i inicjalizuje kamerę.

### `get_frame(self)`
Pobiera surową klatkę.

### `process_frame(self, frame)`
Detekcja + rozpoznawanie twarzy.

Zwraca `(frame, detections)`.

### `release(self)`
Zamyka kamerę.

---

# 4. Moduł `gui.py`

## Klasa **FaceApp** — GUI aplikacji

### Najważniejsze metody:
- `start_camera()`  
- `stop_camera()`  
- `capture_face()`  
- `train_model()`  
- `update_frame()`  
- `show_message()`  

---

# 5. Moduł `main.py`

Uruchamia GUI aplikacji.

```python
root = Tk()
app = FaceApp(root)
root.mainloop()
```

---
