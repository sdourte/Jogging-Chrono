import time
import tkinter as tk
from tkinter import ttk

class Chronometre:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronomètre")
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

        # Affichage du temps
        self.label = ttk.Label(root, text="00:00:00.00", font=("Helvetica", 30))
        self.label.pack(pady=20)

        # Boutons
        self.start_button = ttk.Button(root, text="Démarrer", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(root, text="Arrêter", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(root, text="Réinitialiser", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.save_button = ttk.Button(root, text="Enregistrer temps", command=self.save_time)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.update_chrono()

    def update_chrono(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.display_time()
        self.root.after(10, self.update_chrono)

    def display_time(self):
        centiemes = int((self.elapsed_time % 1) * 100)
        secondes = int(self.elapsed_time) % 60
        minutes = (int(self.elapsed_time) // 60) % 60
        heures = int(self.elapsed_time) // 3600
        self.label.config(text=f"{heures:02}:{minutes:02}:{secondes:02}.{centiemes:02}")

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.display_time()

    def save_time(self):
        with open("temps_arrivee.txt", "a") as file:
            file.write(self.label.cget("text") + "\n")

# Lancer l'application
root = tk.Tk()
chronometre = Chronometre(root)
root.mainloop()
