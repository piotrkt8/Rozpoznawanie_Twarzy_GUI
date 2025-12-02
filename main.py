# main.py - Punkt startowy aplikacji
import tkinter as tk
from gui import FaceApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FaceApp(root)  # Tworzy GUI
        root.mainloop()      # Uruchamia pętlę zdarzeń
    except Exception as e:
        print(f"Błąd krytyczny: {e}")
        input("Wciśnij Enter, aby zamknąć...")