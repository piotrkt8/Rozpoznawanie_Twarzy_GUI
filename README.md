# Face Recognition App – Rozpoznawanie Twarzy z GUI

Aplikacja służy do **rozpoznawania twarzy w czasie rzeczywistym** z użyciem kamery internetowej.  
Wykorzystuje:

- OpenCV – detekcja twarzy  
- VGGFace – generowanie embeddingów (cech twarzy)  
- Logistic Regression – klasyfikacja osób  
- Tkinter – interfejs graficzny (GUI)  


# Funkcje aplikacji

### Rozpoznawanie twarzy (LIVE)
- wykrywanie twarzy z kamery  
- generowanie embeddingów VGGFace  
- predykcja osoby i pewności (%)  
- oznaczenie twarzy ramką (zielona – znany, czerwona – obcy)

### Dodawanie nowych osób
- wykonywanie 20 zdjęć twarzy przez kamerę  
- zapisywanie materiału do bazy `faces/<nazwa>/`

### Trening modelu
- trenowanie modelu na podstawie zapisanych zdjęć  
- zapis modelu: `results/logreg_model.pkl`

### GUI
- panel sterowania (Start, Stop, Dodaj użytkownika, Trenuj model, Usuń użytkownika)  
- podgląd obrazu z kamery  

---

# Technologie

| Technologia | Zastosowanie |
|------------|--------------|
| **Python 3.10+** | Język projektu |
| **OpenCV** | Obsługa kamery, wykrywanie twarzy |
| **TensorFlow / Keras (VGGFace)** | Wyciąganie embeddingów |
| **scikit-learn (Logistic Regression)** | Klasyfikator |
| **Tkinter** | Interfejs graficzny |
| **NumPy, PIL** | Przetwarzanie danych obrazowych |

---

# Struktura katalogów
## 📁 Struktura katalogów

```text
projekt/
│
├── gui.py                 # Interfejs graficzny (Logika przycisków, okna)
├── main.py                # Plik startowy aplikacji
├── camera_live.py         # Obsługa kamery i wątek detekcji
├── haar_detector.py       # Algorytm detekcji twarzy (Haar)
├── vggface_recognizer.py  # Logika sieci neuronowej (VGGFace)
│
├── faces/                 # Baza zdjęć (ignorowane przez git)
├── dataset/               # Folder importu (ignorowane przez git)
├── results/               # Zapisany model (.pkl)
│
├── requirements.txt       # Lista bibliotek
├── Readme.md              # Ten plik
└── docs/                  # Pełna dokumentacja
    ├── USER_GUIDE.md
    ├── DEVELOPER.md
    └── API_REFERENCE.md
---

# Instalacja

### 1. Pobierz projekt
```bash
git clone [https://github.com/piotrkt8/Rozpoznawanie_Twarzy_GUI.git](https://github.com/piotrkt8/Rozpoznawanie_Twarzy_GUI.git)
cd Rozpoznawanie_Twarzy_GUI

### 2. Utwórz środowisko wirtualne
python -m venv venv
venv\Scripts\Activate.ps1

###3. Zainstaluj wymagania
pip install -r requirements.txt

#Uruchomienie aplikacji Start GUI:
python main.py

# Po uruchomieniu otworzy się główne okno programu z:
• podglądem z kamery (po uruchomieniu rozpoznawania)
• panelami sterowania
• przyciskami: Start, Stop, Dodaj użytkownika, Trenuj, Usuń itd.

Dokumentacja projektu
• Instrukcja użytkownika:
docs/USER_GUIDE.md
• Dokumentacja deweloperska:
docs/DEVELOPER.md




Autor Projektu: Piotr Kozubek