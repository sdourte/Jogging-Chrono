import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

class Chronometre:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronomètre")
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.rang = 1  # Compteur du classement

        # Affichage du temps
        self.label = ttk.Label(root, text="00:00:00.00", font=("Helvetica", 30))
        self.label.pack(pady=20)

        # Conteneur pour les boutons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Boutons
        self.start_button = ttk.Button(button_frame, text="Go", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset chrono", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save time", command=self.save_time)
        self.save_button.grid(row=0, column=3, padx=5)

        self.clear_file_button = ttk.Button(button_frame, text="Reset fichier", command=self.reset_file)
        self.clear_file_button.grid(row=0, column=4, padx=5)

        self.export_button = ttk.Button(button_frame, text="Ouvrir CSV", command=self.open_csv)
        self.export_button.grid(row=0, column=5, padx=5)

        # Forcer le focus sur la fenêtre principale pour éviter les problèmes avec Espace
        self.root.focus_set()

        self.update_chrono()
        self.bind_keys()  # Ajout des raccourcis clavier

    def bind_keys(self):
        """Associe la touche Espace à la sauvegarde du temps sans perturber le chrono."""
        self.root.bind("<space>", self.on_space_press)

    def on_space_press(self, event):
        """Sauvegarde le temps quand on appuie sur Espace et empêche le comportement par défaut."""
        self.save_time()
        return "break"  # Empêche la propagation de l'événement à Tkinter

    def update_chrono(self):
        """Met à jour l'affichage du chrono toutes les 10 ms."""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.display_time()
        self.root.after(10, self.update_chrono)

    def display_time(self):
        """Affiche le temps écoulé au format hh:mm:ss.cs."""
        centiemes = int((self.elapsed_time % 1) * 100)
        secondes = int(self.elapsed_time) % 60
        minutes = (int(self.elapsed_time) // 60) % 60
        heures = int(self.elapsed_time) // 3600
        self.label.config(text=f"{heures:02}:{minutes:02}:{secondes:02}.{centiemes:02}")

    def start(self):
        """Démarre le chronomètre et enlève le focus des boutons."""
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
        self.root.focus_set()  # Remet le focus sur la fenêtre

    def stop(self):
        """Arrête le chronomètre."""
        self.running = False
        self.root.focus_set()  # Remet le focus sur la fenêtre

    def reset(self):
        """Réinitialise le chronomètre et le classement."""
        self.running = False
        self.elapsed_time = 0
        self.rang = 1  # Réinitialise le classement
        self.display_time()
        self.root.focus_set()  # Remet le focus sur la fenêtre

    def save_time(self):
        """Sauvegarde le temps actuel dans un fichier CSV et TXT."""
        date_heure = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

        # Définir le classement en format : 1er, 2e, 3e, etc.
        rang_txt = "1er" if self.rang == 1 else f"{self.rang}e"

        temps = self.label.cget("text")
        ligne = [rang_txt, temps, "?", date_heure]

        # Sauvegarde dans un fichier CSV
        with open("Temps_arrivees.csv", "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(ligne)

        # Sauvegarde aussi dans un fichier TXT pour backup
        with open("Temps_arrivees.txt", "a") as txt_file:
            txt_file.write(f"{rang_txt} - {temps} - Dossard: ? - {date_heure}\n")

        self.rang += 1  # Augmenter le compteur du classement
        self.root.focus_set()  # Remet le focus sur la fenêtre

    def reset_file(self):
        """Efface les résultats enregistrés après confirmation."""
        confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment effacer les résultats ?")
        if confirmation:
            with open("Temps_arrivees.csv", "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Classement", "Temps", "Dossard", "Date/Heure"])  # Réécrit l'en-tête
            messagebox.showinfo("Réinitialisation", "Le fichier a été vidé avec succès.")
        self.root.focus_set()  # Remet le focus sur la fenêtre

    def open_csv(self):
        """Ouvre le fichier CSV contenant les résultats."""
        if os.path.exists("Temps_arrivees.csv"):
            os.startfile("Temps_arrivees.csv")  # Ouvre le fichier sur Windows
        else:
            messagebox.showerror("Erreur", "Aucun fichier de résultats trouvé.")
        self.root.focus_set()  # Remet le focus sur la fenêtre

# Lancer l'application
root = tk.Tk()
chronometre = Chronometre(root)
root.mainloop()
