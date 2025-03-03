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

        # Boutons
        self.start_button = ttk.Button(root, text="Go", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(root, text="Reset chrono", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(root, text="Save time", command=self.save_time)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_file_button = ttk.Button(root, text="Reset fichier", command=self.reset_file)
        self.clear_file_button.pack(side=tk.LEFT, padx=5)

        self.export_button = ttk.Button(root, text="Ouvrir CSV", command=self.open_csv)
        self.export_button.pack(side=tk.LEFT, padx=5)

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
        self.rang = 1  # Réinitialise le classement
        self.display_time()

    def save_time(self):
        # Obtenir la date et l'heure
        date_heure = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

        # Définir le classement en format : 1er, 2e, 3e, etc.
        if self.rang == 1:
            rang_txt = "1er"
        else:
            rang_txt = f"{self.rang}e"

        # Construire la ligne à enregistrer (sans dossard)
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

    def reset_file(self):
        # Demander confirmation avant de supprimer les données
        confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment effacer les résultats ?")
        if confirmation:
            with open("Temps_arrivees.csv", "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Classement", "Temps", "Dossard", "Date/Heure"])  # Réécrit l'en-tête
            messagebox.showinfo("Réinitialisation", "Le fichier a été vidé avec succès.")

    def open_csv(self):
        if os.path.exists("Temps_arrivees.csv"):
            os.startfile("Temps_arrivees.csv")  # Ouvre le fichier sur Windows
        else:
            messagebox.showerror("Erreur", "Aucun fichier de résultats trouvé.")

# Lancer l'application
root = tk.Tk()
chronometre = Chronometre(root)
root.mainloop()
