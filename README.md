# 🎯 Face Recognition App – Rozpoznawanie Twarzy z GUI

Aplikacja służy do **rozpoznawania twarzy w czasie rzeczywistym** z użyciem kamery internetowej.  
Wykorzystuje:

- OpenCV – detekcja twarzy  
- VGGFace – generowanie embeddingów (cech twarzy)  
- Logistic Regression – klasyfikacja osób  
- Tkinter – interfejs graficzny (GUI)  

Projekt spełnia wymagania:  
✔ **PPP – Python**  
✔ **OiRPOS – Open Source + dokumentacja + pliki markdown**

---

# 🚀 Funkcje aplikacji

### 🔍 Rozpoznawanie twarzy (LIVE)
- wykrywanie twarzy z kamery  
- generowanie embeddingów VGGFace  
- predykcja osoby i pewności (%)  
- oznaczenie twarzy ramką (zielona – znany, czerwona – obcy)

### ➕ Dodawanie nowych osób
- wykonywanie 20 zdjęć twarzy przez kamerę  
- zapisywanie materiału do bazy `faces/<nazwa>/`

### 🧠 Trening modelu
- trenowanie modelu na podstawie zapisanych zdjęć  
- zapis modelu: `results/logreg_model.pkl`

### 🖥️ GUI
- panel sterowania (Start, Stop, Dodaj użytkownika, Trenuj model, Usuń użytkownika)  
- podgląd obrazu z kamery  

---

# 🛠️ Technologie

| Technologia | Zastosowanie |
|------------|--------------|
| **Python 3.10+** | Język projektu |
| **OpenCV** | Obsługa kamery, wykrywanie twarzy |
| **TensorFlow / Keras (VGGFace)** | Wyciąganie embeddingów |
| **scikit-learn (Logistic Regression)** | Klasyfikator |
| **Tkinter** | Interfejs graficzny |
| **NumPy, PIL** | Przetwarzanie danych obrazowych |

---

# 📁 Struktura katalogów
projekt/
│
├── gui.py                 # Interfejs graficzny
├── main.py                # Plik startowy
├── camera_live.py         # Obsługa kamery
├── haar_detector.py       # Detekcja twarzy
├── vggface_recognizer.py  # Sieci neuronowe
│
├── faces/                 # Baza zdjęć (ignorowane przez git)
├── dataset/               # Import zdjęć (ignorowane przez git)
├── results/               # Zapisany model
│
├── requirements.txt       # Lista bibliotek
├── Readme.md              # Ten plik
└── docs/                  # Dokumentacja
    ├── USER_GUIDE.md
    ├── DEVELOPER.md
    └── API_REFERENCE.md

---

# 🔧 Instalacja

### 1. Pobierz projekt
```bash
git clone <adres_repo>
cd projekt

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

📄 Dokumentacja projektu
Komplet dokumentacji znajduje się w katalogu docs/:
• Instrukcja użytkownika:
docs/USER_GUIDE.md
• Dokumentacja deweloperska:
docs/DEVELOPER.md




Autor Projektu: Piotr Kozubek