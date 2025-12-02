# vggface_recognizer.py
import torch
import numpy as np
import os
import joblib
from PIL import Image
from facenet_pytorch import InceptionResnetV1
from sklearn.linear_model import LogisticRegression
from typing import List, Callable, Union

# === KONFIGURACJA ===
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
MODEL_PATH = os.path.join('results', 'logreg_model.pkl')

def extract_embeddings_batch(images_pil: List[Image.Image]) -> np.ndarray:
    """
    Przetwarza listę obrazów PIL przez sieć neuronową i zwraca wektory cech (embeddingi).

    Args:
        images_pil (List[Image.Image]): Lista obrazów PIL.

    Returns:
        np.ndarray: Tablica wektorów o wymiarach (N, 512).
    """
    if not images_pil:
        return np.array([])
    
    batch = []
    for img in images_pil:
        if img.size != (160, 160):
            img = img.resize((160, 160))
        
        img_tensor = torch.tensor(np.array(img)).float()
        
        if img_tensor.ndim == 2:
            img_tensor = img_tensor.unsqueeze(2).repeat(1, 1, 3)
            
        img_tensor = img_tensor.permute(2, 0, 1)
        img_tensor = (img_tensor - 127.5) / 128.0
        batch.append(img_tensor)

    batch_tensor = torch.stack(batch).to(device)

    with torch.no_grad():
        embeddings = resnet(batch_tensor).cpu().numpy()
        
    return embeddings

class VGGFaceRecognizer:
    """Klasa zarządzająca treningiem modelu i logiką rozpoznawania."""
    
    def __init__(self):
        self.model_path = MODEL_PATH
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def train(self, progress_callback: Callable[[int, str], None] = None) -> str:
        """
        Trenuje model klasyfikatora na podstawie zdjęć z folderu 'faces'.

        Args:
            progress_callback (Callable): Funkcja do aktualizacji paska postępu w GUI.

        Returns:
            str: Komunikat statusu (np. "Model wytrenowany pomyślnie!").
        """
        faces_dir = 'faces'
        X, y = [], []

        if not os.path.exists(faces_dir):
            return "Brak folderu faces"

        users = [d for d in os.listdir(faces_dir) if os.path.isdir(os.path.join(faces_dir, d))]
        
        if len(users) < 2:
            return "Za mało użytkowników (min. 2)."

        # Inwentaryzacja plików
        files_to_process = []
        for user in users:
            user_dir = os.path.join(faces_dir, user)
            for img_name in os.listdir(user_dir):
                files_to_process.append((user, os.path.join(user_dir, img_name)))
        
        total_files = len(files_to_process)
        if total_files == 0:
            return "Brak zdjęć."

        # Przetwarzanie wsadowe
        processed_count = 0
        current_batch_imgs = []
        current_batch_labels = []
        BATCH_SIZE = 5 
        
        for i, (user, img_path) in enumerate(files_to_process):
            try:
                img = Image.open(img_path).convert('RGB')
                current_batch_imgs.append(img)
                current_batch_labels.append(user)
            except Exception:
                pass
            
            if len(current_batch_imgs) >= BATCH_SIZE or i == total_files - 1:
                embs = extract_embeddings_batch(current_batch_imgs)
                if len(embs) > 0:
                    X.extend(embs)
                    y.extend(current_batch_labels)
                
                processed_count += len(current_batch_imgs)
                current_batch_imgs = []
                current_batch_labels = []

                if progress_callback:
                    percent = int((processed_count / total_files) * 90)
                    progress_callback(percent, f"Analiza: {user}")

        # Trening
        if progress_callback:
            progress_callback(95, "Trening modelu...")
            
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, y)

        joblib.dump(clf, self.model_path)
        return "Model wytrenowany pomyślnie!"