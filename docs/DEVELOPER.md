#  Dokumentacja Deweloperska  
## System Rozpoznawania Twarzy – GUI

---

## Spis treści
1. Wprowadzenie  
2. Wymagania środowiska  
3. Instalacja  
4. Struktura projektu  
5. Opis głównych modułów  
6. Przepływ działania aplikacji  
7. Jak dodać nowe funkcje  
8. Debugowanie i logi  
9. Kontakt i rozwój projektu  

---

# 1. Wprowadzenie

Ten dokument opisuje szczegóły techniczne aplikacji:

- sposób instalacji,
- strukturę kodu,
- architekturę modułów,
- logikę przepływu danych,
- najważniejsze klasy i funkcje,
- wskazówki do rozbudowy projektu.

Aplikacja została napisana w Pythonie z wykorzystaniem:

- **OpenCV** – praca z kamerą i wykrywanie twarzy,  
- **TensorFlow + Keras** – generowanie wektorów cech (embeddings),  
- **Sklearn** – trenowanie klasyfikatora,  
- **Tkinter** – GUI,  
- **PIL** – obsługa obrazów.

---

# 2. Wymagania środowiska

### System
- Windows 10/11  
- Linux (Ubuntu 20+)

### Python
- Zalecany: Python **3.10**

### Biblioteki
Instalowane przez `requirements.txt`:
- opencv-python
- tensorflow
- numpy
- pillow
- scikit-learn
- joblib

---

# 3. Instalacja

Kroki instalacji dla dewelopera:

### 1. Utwórz środowisko
python -m venv venv

### 2. Aktywuj środowisko

Windows:
venv\Scripts\Activate.ps1

### 3. Zainstaluj zależności
pip install -r requirements.txt

### 4. Uruchom aplikację
python main.py


---

# 4. Struktura projektu
```text
projekt/
│
├── gui.py # Główne okno GUI (Tkinter)
├── main.py # Launcher GUI
├── camera_live.py # Klasa obsługująca kamerę i rozpoznawanie
├── haar_detector.py # Wykrywanie twarzy (Haar Cascade)
├── vggface_recognizer.py # Ekstrakcja embeddingów (TensorFlow)
│
├── faces/ # Zbiór zdjęć użytkowników
├── dataset/ # Folder do importu zdjęć
├── results/ # Zapis trenowanego modelu
│
├── requirements.txt
├── Readme.md
└── docs/                  # Dokumentacja
    ├── USER_GUIDE.md
    ├── DEVELOPER.md
    └── API_REFERENCE.md


---
```
# 5. Opis głównych modułów

## 5.1 `gui.py`  
Zawiera główne okno aplikacji.  
Najważniejsze funkcje:

- ładowanie GUI,
- reakcja na kliknięcia przycisków,
- sterowanie kamerą,
- uruchamianie treningu,
- dodawanie użytkownika,
- wyświetlanie komunikatów.

GUI używa klasy `CameraSystem` z modułu `camera_live.py`.

---

## 5.2 `camera_live.py`  
Zawiera klasę:

### **CameraSystem**
Odpowiada za:

- obsługę kamery (`cv2.VideoCapture`),
- wyszukiwanie twarzy (Haar Cascade),
- wycinanie twarzy,
- generowanie embeddingów,
- predykcję klasy,
- rysowanie ramek i opisów na obrazie.

---

## 5.3 `haar_detector.py`
Funkcja:

- `detect_faces_opencv(frame)`

Wykrywa twarze metodą Haar Cascade.  
Dodatkowe filtry eliminują fałszywe wykrycia (proporcje, rozmiar).


---

## 5.4 `vggface_recognizer.py`  
Zawiera klasę:

### **VGGFaceRecognizer**

Funkcje:

- ładowanie modelu TensorFlow,
- przygotowanie obrazów,
- normalizacja,
- ekstrakcja embeddingów,
- zapis i ładowanie modelu `logreg_model.pkl`.

Wektor embeddingu ma długość **2622** lub **2048** (zależnie od konfiguracji).

---

# 6. Przepływ działania aplikacji

### 1. Użytkownik klika „Dodaj użytkownika”
→ GUI uruchamia zbieranie 20 zdjęć z kamerą.  
→ Każde zdjęcie jest zapisywane w `faces/<nazwa>/`.

### 2. Użytkownik klika „Trenuj model”
→ Skrypt przechodzi przez wszystkie foldery w `faces/`,  
→ generuje embeddingi,  
→ trenuje klasyfikator Logistic Regression,  
→ zapisuje model do `results/logreg_model.pkl`.

### 3. Użytkownik klika „Start rozpoznawania”
→ Kamera uruchamia strumień,  
→ każda klatka jest analizowana,  
→ twarze są wykrywane, wycinane i przetwarzane,  
→ embedding trafia do modelu,  
→ wynik jest rysowany na obrazie.

---

# 7. Jak dodać nowe funkcje

### Dodanie przycisku w GUI  
1. Otwórz `gui.py`.  
2. Znajdź funkcję `create_buttons()`.  
3. Dodaj:

```python
tk.Button(panel, text="Nowa funkcja", command=self.nowa_funkcja).pack()

def nowa_funkcja(self):
    print("Nowa funkcja działa!")


###Dodanie innego detektora twarzy (np. DNN)
1. Dodaj nowy plik dnn_detector.py.
2. Zaimplementuj funkcję:
def detect_faces_dnn(frame): ...

3. W camera_live.py zamień:
from haar_detector import detect_faces_opencv
na:
from dnn_detector import detect_faces_dnn

###Podmiana modelu embeddingów (np. FaceNet)

1.Zastąp w vggface_recognizer.py model TensorFlow.
2.Zachowaj funkcję:
def extract_embeddings_batch(images)

# 8. Debugowanie i logi
##Włącz debug prints:
W każdym module:
print("[DEBUG] opis")
##Sprawdzenie kamery:
python camera_live.py
##Logi błędów TensorFlow:
set TF_CPP_MIN_LOG_LEVEL=0

##Dodatkowo
• Jeśli model nie ładuje się → usuń results/ i przetrenuj.
• Jeśli GUI nie działa → sprawdź wersję Tkinter.

# 9. Kontakt i rozwój
Kod został przygotowany tak, aby był łatwy do rozszerzania.
Projekt można rozwijać, dodając:

• lepsze modele rozpoznawania,
• bazę SQL zamiast folderów,
• logowanie aktywności,
• eksport raportów,
• integrację z API (np. serwer Flask).

