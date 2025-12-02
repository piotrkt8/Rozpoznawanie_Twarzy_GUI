# gui.py
import os
import cv2
import time
import tkinter as tk
import tkinter.ttk as ttk  # <-- potrzebne do Progressbar
import shutil # do usuwania folderów
from tkinter import simpledialog, messagebox, Label, Button, Frame
from PIL import Image, ImageTk

# Importy własne
from camera_live import FaceRecognitionCamera
from haar_detector import detect_faces_opencv
from vggface_recognizer import VGGFaceRecognizer

class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Rozpoznawania Twarzy v2.0")
        self.root.geometry("950x700")
        
        # === STATUS APLIKACJI ===
        # Tryby: "IDLE" (nic), "PREVIEW" (kamera), "RECOGNITION" (rozpoznawanie)
        self.mode = "IDLE" 
        
        # Inicjalizacja modułów
        self.recognizer_logic = VGGFaceRecognizer()
        
        # Próba bezpiecznego załadowania kamery
        try:
            self.camera = FaceRecognitionCamera()
            print("[INFO] Kamera i model załadowane.")
        except Exception as e:
            print(f"[WARN] Uruchamiam bez aktywnej kamery: {e}")
            self.camera = None

        # === GUI ===
        # Główne okno wideo
        self.video_label = Label(root, bg="black")
        self.video_label.place(x=20, y=20, width=640, height=480)
        
        # Etykieta statusu
        self.status_label = Label(root, text="Status: Gotowy", font=("Arial", 12), fg="blue")
        self.status_label.place(x=20, y=510)

        # Panel sterowania
        control_frame = Frame(root)
        control_frame.place(x=680, y=20)

        # Przyciski
        Button(control_frame, text="▶ Start Kamery (Podgląd)", width=25, height=2, 
               command=self.set_mode_preview).pack(pady=5)
        
        Button(control_frame, text="🔍 Rozpoznawanie (Start)", width=25, height=2, bg="#d1ffbd",
               command=self.set_mode_recognition).pack(pady=5)
        
        Button(control_frame, text="⏹ ZATRZYMAJ / PAUZA", width=25, height=2, bg="#ffcccc",
               command=self.set_mode_idle).pack(pady=5)
        
        Frame(control_frame, height=20).pack() # Odstęp

        Button(control_frame, text="➕ Dodaj użytkownika", width=25, height=2, 
               command=self.add_user).pack(pady=5)
        Frame(control_frame, height=20).pack() # Odstęp
        
        Button(control_frame, text="🗑️ Usuń Użytkownika", width=25, height=2, bg="#ffcccc",
                command=self.delete_user).pack(pady=5)
        Frame(control_frame, height=20).pack() # Odstęp

        Button(control_frame, text="🧠 Trenuj Model", width=25, height=2, 
               command=self.train_model).pack(pady=5)
        
        Frame(control_frame, height=20).pack() # Odstęp

        Button(control_frame, text="📂 Importuj z 'dataset'", width=25, height=2, bg="#e1f7d5",
               command=self.process_dataset).pack(pady=5)
        
        Frame(control_frame, height=20).pack() # Odstęp

        Button(control_frame, text="⛔ Wyjście", width=25, height=2, 
               command=self.close_app).pack(pady=5)

        # === START GŁÓWNEJ PĘTLI ===
        self.update_loop()

    # --- STEROWANIE TRYBAMI ---
    def set_mode_preview(self):
        if self.ensure_camera():
            self.mode = "PREVIEW"
            self.status_label.config(text="Status: Podgląd kamery", fg="green")

    def set_mode_recognition(self):
        if self.ensure_camera():
            self.mode = "RECOGNITION"
            self.status_label.config(text="Status: ROZPOZNAWANIE AKTYWNE", fg="red")

    def set_mode_idle(self):
        self.mode = "IDLE"
        self.status_label.config(text="Status: Zatrzymano / Oczekiwanie", fg="blue")
        # Możemy wyczyścić ekran na czarno
        self.video_label.config(image='')
        self.video_label.bg = "black"

    def ensure_camera(self):
        """Sprawdza czy kamera istnieje, jak nie to próbuje ją włączyć."""
        if self.camera is None:
            try:
                self.camera = FaceRecognitionCamera()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można uruchomić kamery: {e}")
                return False
        return True

    # --- GŁÓWNA PĘTLA ODŚWIEŻANIA (SERCE PROGRAMU) ---
    def update_loop(self):
        """Ta funkcja wywołuje się sama co 10ms i obsługuje klatki wideo."""
        
        if self.camera is not None and self.mode != "IDLE":
            # Pobierz klatkę
            frame = self.camera.get_frame()
            
            if frame is not None:
                final_image = None
                
                # Logika zależna od trybu
                if self.mode == "PREVIEW":
                    # Czysty podgląd (tylko detekcja twarzy dla bajeru, bez rozpoznawania)
                    # Możemy po prostu pokazać frame, albo narysować ramki Haara
                    frame_resized = cv2.resize(frame, (400, 400))
                    faces = detect_faces_opencv(frame_resized)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame_resized, (x, y), (x+w, y+h), (255, 0, 0), 1)
                    final_image = frame_resized

                elif self.mode == "RECOGNITION":
                    # Pełne rozpoznawanie (korzystamy z logiki camera_live)
                    processed_frame, detections = self.camera.process_frame(frame)
                    final_image = processed_frame

                # Wyświetlenie w GUI
                if final_image is not None:
                    # Konwersja BGR -> RGB -> PIL -> ImageTk
                    img_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
                    img_pil = Image.fromarray(img_rgb)
                    # Skalowanie do rozmiaru okna w GUI (640x480)
                    img_pil = img_pil.resize((640, 480)) 
                    img_tk = ImageTk.PhotoImage(img_pil)
                    
                    self.video_label.config(image=img_tk)
                    self.video_label.image = img_tk

        # Zaplanuj kolejne wywołanie tej funkcji za 10 milisekund
        # To jest kluczowe - dzięki temu GUI nie zamarza!
        self.root.after(10, self.update_loop)

    # --- DODAWANIE UŻYTKOWNIKA ---
    # --- DODAWANIE UŻYTKOWNIKA (WERSJA NA KLAWISZ 'B') ---
    def add_user(self):
        # 1. Zatrzymaj procesy w tle
        self.set_mode_idle()
        self.root.update()
        
        if not self.ensure_camera(): return

        name = simpledialog.askstring("Nowy użytkownik", "Podaj nazwę użytkownika:")
        if not name: return

        user_folder = os.path.join("faces", name)
        os.makedirs(user_folder, exist_ok=True)
        
        # ZMIANA 1: Aktualizacja instrukcji w oknie
        messagebox.showinfo("Instrukcja", 
                            f"Zbiór danych dla: {name}\n\n"
                            "1. Ustaw głowę w kadrze.\n"
                            "2. Gdy ramka jest ZIELONA, wciśnij klawisz 'B', aby zrobić zdjęcie.\n"
                            "3. Zmieniaj pozy (przód, bok, góra, miny)!\n"
                            "4. Zbierzemy 20 ostrych zdjęć.")

        count = 0
        required = 20
        
        while count < required:
            frame = self.camera.get_frame()
            if frame is None: break
            
            display = frame.copy()
            faces = detect_faces_opencv(frame)
            
            face_detected = False
            
            if len(faces) > 0:
                face_detected = True
                (x, y, w, h) = faces[0]
                cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # ZMIANA 2: Aktualizacja napisu na wideo
                cv2.putText(display, "GOTOWY - Wcisnij 'B'", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(display, "Nie widze twarzy!", (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.putText(display, f"Zdjecie: {count}/{required}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            
            cv2.imshow("Dodawanie uzytkownika", display)
            
            key = cv2.waitKey(10) & 0xFF
            
            if key == 27: # ESC - Anuluj
                break
            
            # ZMIANA 3: Zmiana kodu klawisza ze spacji (32) na 'b' (ord('b'))
            elif key == ord('b'): 
                if face_detected:
                    (x, y, w, h) = faces[0]
                    
                    roi = frame[y:y+h, x:x+w]
                    roi = cv2.resize(roi, (224, 224))
                    
                    save_path = os.path.join(user_folder, f"{count}.jpg")
                    cv2.imwrite(save_path, roi)
                    
                    count += 1
                    print(f"[INFO] Zrobiono zdjęcie {count}/{required}")
                    
                    # Efekt wizualny (BŁYSK)
                    cv2.rectangle(display, (x, y), (x+w, y+h), (255, 255, 255), -1)
                    cv2.imshow("Dodawanie uzytkownika", display)
                    cv2.waitKey(100)
                else:
                    print("[WARN] Wciśnięto 'B', ale nie wykryto twarzy!")

        cv2.destroyWindow("Dodawanie uzytkownika")
        
        if count == required:
            messagebox.showinfo("Sukces", f"Zebrano {count} zdjęć dla {name}.\nTeraz kliknij 'Trenuj Model'!")
        else:
            messagebox.showwarning("Przerwano", "Nie zebrano wszystkich zdjęć.")

    # --- USUWANIE UŻYTKOWNIKA ---
    # To musi być wewnątrz klasy FaceApp (równo z innymi def)
    def delete_user(self):
        # To musi być wcięte (zazwyczaj 4 spacje lub 1 tabulator głębiej)
        faces_dir = "faces" 
        
        if not os.path.exists(faces_dir): 
            return
        
        users = os.listdir(faces_dir)
        if not users:
            messagebox.showinfo("Info", "Brak użytkowników do usunięcia.")
            return

        # Wybór użytkownika z listy
        target = simpledialog.askstring("Usuń", f"Wpisz nazwę do usunięcia:\n{', '.join(users)}")
        
        if target and target in users:
            path = os.path.join(faces_dir, target)
            try:
                import shutil # Import wewnątrz funkcji jest OK, jeśli zapomniałeś na górze
                shutil.rmtree(path) # Usuwa folder wraz z zawartością
                messagebox.showinfo("Sukces", f"Użytkownik {target} usunięty.\nPrzetrenuj model ponownie!")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))
        elif target:
            messagebox.showwarning("Błąd", "Nie ma takiego użytkownika.")
    
    # --- TRENING ---
    def train_model(self):
        # 1. Zatrzymaj inne procesy
        self.set_mode_idle()
        self.root.update()

        # 2. Stwórz okno ładowania (Popup)
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Przetwarzanie...")
        loading_window.geometry("400x150")
        loading_window.resizable(False, False)
        
        # Wycentrowanie okna względem głównego
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        loading_window.geometry(f"+{x}+{y}")

        # Elementy okna
        Label(loading_window, text="🚀 Trenowanie Sieci Neuronowej", font=("Arial", 12, "bold")).pack(pady=10)
        
        progress_bar = ttk.Progressbar(loading_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10)
        
        status_label = Label(loading_window, text="Inicjalizacja...", fg="gray")
        status_label.pack(pady=5)

        loading_window.update() # Wymuś narysowanie okna

        # 3. Funkcja aktualizująca pasek (callback)
        def update_progress(percent, text):
            progress_bar['value'] = percent
            status_label.config(text=text)
            loading_window.update() # To jest kluczowe - odświeża okno w trakcie pracy!

        # 4. Uruchom trening (może chwilę potrwać)
        try:
            # Przekazujemy naszą funkcję update_progress do recognizera
            result = self.recognizer_logic.train(progress_callback=update_progress)
            loading_window.destroy() # Zamknij pasek po wszystkim
            messagebox.showinfo("Sukces", result)
            
            # Przeładuj kamerę
            if self.camera:
                import joblib
                try:
                    self.camera = FaceRecognitionCamera() 
                    print("[INFO] Model przeładowany.")
                except:
                    pass
        except Exception as e:
            loading_window.destroy()
            messagebox.showerror("Błąd treningu", str(e))

    # --- IMPORT Z DATASET (ZAMIAST MAIN.PY) ---
    def process_dataset(self):
        # 1. Zatrzymaj kamerę i przygotuj GUI
        self.set_mode_idle()
        self.root.update()
        
        data_dir = 'dataset'
        faces_dir = 'faces'

        if not os.path.exists(data_dir):
            messagebox.showerror("Błąd", f"Nie znaleziono folderu '{data_dir}'!")
            return

        # 2. Policz pliki do przetworzenia (dla paska postępu)
        total_files = 0
        tasks = [] # Lista krotek (ścieżka_src, folder_dest, nazwa_pliku)
        
        for person_name in os.listdir(data_dir):
            person_dir = os.path.join(data_dir, person_name)
            if not os.path.isdir(person_dir): continue
            
            # Utwórz odpowiednik w folderze faces
            target_dir = os.path.join(faces_dir, person_name)
            os.makedirs(target_dir, exist_ok=True)
            
            for img_name in os.listdir(person_dir):
                tasks.append((os.path.join(person_dir, img_name), target_dir, img_name))

        total_files = len(tasks)
        if total_files == 0:
            messagebox.showinfo("Info", "Folder 'dataset' jest pusty.")
            return

        # 3. Otwórz okno ładowania
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Przetwarzanie datasetu...")
        loading_window.geometry("400x150")
        
        # Wycentrowanie
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        loading_window.geometry(f"+{x}+{y}")

        Label(loading_window, text="✂️ Wycinanie twarzy z 'dataset'", font=("Arial", 12, "bold")).pack(pady=10)
        progress_bar = ttk.Progressbar(loading_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10)
        status_label = Label(loading_window, text="Start...", fg="gray")
        status_label.pack(pady=5)
        loading_window.update()

        # 4. Pętla przetwarzania
        processed_count = 0
        success_count = 0

        for i, (src_path, target_dir, filename) in enumerate(tasks):
            try:
                # Wczytaj obraz
                img = cv2.imread(src_path)
                if img is None: continue
                
                # Zmniejsz duże zdjęcia dla szybkości detekcji (opcjonalne, ale zalecane)
                if img.shape[1] > 1000:
                    scale = 1000 / img.shape[1]
                    img = cv2.resize(img, (0,0), fx=scale, fy=scale)

                # Wykryj twarz (używamy Twojego detektora)
                faces = detect_faces_opencv(img)
                
                if len(faces) > 0:
                    # Bierzemy pierwszą/największą twarz
                    (x, y, w, h) = faces[0]
                    face_img = img[y:y+h, x:x+w]
                    
                    # Skalujemy do 224x224 (gotowe pod VGGFace)
                    face_resized = cv2.resize(face_img, (224, 224))
                    
                    # Zapisujemy w folderze faces
                    cv2.imwrite(os.path.join(target_dir, filename), face_resized)
                    success_count += 1
            
            except Exception as e:
                print(f"[WARN] Błąd przy {filename}: {e}")

            # Aktualizacja paska co 5 zdjęć (dla wydajności) lub na końcu
            processed_count += 1
            if processed_count % 5 == 0 or processed_count == total_files:
                percent = int((processed_count / total_files) * 100)
                progress_bar['value'] = percent
                status_label.config(text=f"Przetworzono: {processed_count}/{total_files} (Sukces: {success_count})")
                loading_window.update()

        loading_window.destroy()
        messagebox.showinfo("Koniec", f"Zakończono import!\n\nPrzetworzono plików: {total_files}\nWykryto twarzy: {success_count}\n\nTeraz kliknij 'Trenuj Model'.")

    # --- ZAMYKANIE ---
    def close_app(self):
        self.mode = "IDLE"
        if self.camera: self.camera.release()
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FaceApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Krytyczny błąd aplikacji: {e}")