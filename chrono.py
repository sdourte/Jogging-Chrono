import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import customtkinter as ctk
import csv
import os
import winsound
import threading

# Configuration de customtkinter
ctk.set_appearance_mode("dark")  # Thème sombre
ctk.set_default_color_theme("blue")  # Couleur des boutons

class Chronometre:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronomètre")
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.rang = 1  # Compteur du classement
        self.last_times = []  # Stocke les derniers temps enregistrés
        self.previous_time = None  # Stocke le dernier temps enregistré pour calculer le delta
        
        # Frame principale pour centrer les éléments
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(expand=True, fill="both")
        
        # Grand titre
        self.title_label = ctk.CTkLabel(self.main_frame, text="🏃 Chronomètre - Jogging 🏃",
                                        font=("Arial", 40, "bold"), text_color="cyan")
        self.title_label.pack(pady=10)

        # Affichage du temps
        self.label = ctk.CTkLabel(self.main_frame, text="00:00:00.00", font=("Courier", 100, "bold"), text_color="white")
        self.label.pack(pady=20)

        # Conteneur pour les boutons
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=10)

        # Boutons
        self.start_button = ctk.CTkButton(button_frame, text="▶️ Go", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ctk.CTkButton(button_frame, text="⏹ Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = ctk.CTkButton(button_frame, text="🔄 Reset", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.save_button = ctk.CTkButton(button_frame, text="💾 Save", command=self.save_time)
        self.save_button.grid(row=0, column=3, padx=5)
        
        # Bouton pour changer le thème
        self.theme_button = ctk.CTkButton(button_frame, text="Switch theme", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=4, padx=5)

        # Liste des derniers temps enregistrés
        self.last_times_label = ctk.CTkLabel(self.main_frame, text="Derniers temps :", font=("Arial", 14))
        self.last_times_label.pack(pady=5)

        self.last_times_listbox = ctk.CTkTextbox(self.main_frame, height=100, width=400)
        self.last_times_listbox.pack(pady=5)

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
        self.label.configure(text=f"{heures:02}:{minutes:02}:{secondes:02}.{centiemes:02}")

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
        self.last_times_listbox.delete("0.0", "end")  # Effacer la liste des derniers temps
        self.last_times = []
        self.root.focus_set()  # Remet le focus sur la fenêtre

    def play_sound(self):
        """Joue un son en arrière-plan sans bloquer le programme."""
        # Utilisation d'un thread pour jouer le son sans bloquer le programme
        threading.Thread(target=lambda: winsound.Beep(1000, 500), daemon=True).start()

    def save_time(self):
        """Sauvegarde le temps actuel dans un fichier CSV et TXT avec un delta."""
        date_heure = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

        # Définir le classement en format : 1er, 2e, 3e, etc.
        rang_txt = "1er" if self.rang == 1 else f"{self.rang}e"

        temps = self.label.cget("text")

        # Conversion du temps en secondes pour calculer le delta
        def convert_to_seconds(time_str):
            h, m, s, cs = map(int, time_str.replace(":", " ").replace(".", " ").split())  
            return h * 3600 + m * 60 + s + cs / 100  # Ajout des centièmes de seconde
        
        current_time_seconds = convert_to_seconds(temps)
        
        if self.previous_time is None:
            delta = "—"  # Pas de delta pour le premier coureur
        else:
            delta_seconds = current_time_seconds - self.previous_time
            delta_h = int(delta_seconds // 3600)
            delta_m = int((delta_seconds % 3600) // 60)
            delta_s = delta_seconds % 60
            delta = f"{delta_h:02}:{delta_m:02}:{delta_s:05.2f}"  # Format hh:mm:ss.ss

        self.previous_time = current_time_seconds  # Met à jour le dernier temps enregistré

        ligne = [rang_txt, temps, delta, date_heure]
        
        # Joue un bip de 1000 Hz pendant 500 ms
        self.play_sound()
        print("✅ Son joué avec succès (mais inaudible si volume coupé)")

        # Sauvegarde dans un fichier CSV
        with open("Temps_arrivees.csv", "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(ligne)

        # Sauvegarde aussi dans un fichier TXT pour backup (en UTF-8)
        with open("Temps_arrivees.txt", "a", encoding="utf-8") as txt_file:
            txt_file.write(f"Place : {rang_txt} - Temps : {temps} - Delta : {delta} - Date & Heure : {date_heure}\n")

        self.rang += 1  # Augmenter le compteur du classement
        self.update_last_times(rang_txt, temps, delta)  # Met à jour la liste des derniers temps
        self.root.focus_set()  # Remet le focus sur la fenêtre
    
    def toggle_theme(self):
        """Bascule entre le mode clair et sombre."""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("dark")
            self.label.configure(text_color="white")
            self.title_label.configure(text_color="white")
        else:
            ctk.set_appearance_mode("light")
            self.label.configure(text_color="black")
            self.title_label.configure(text_color="black")

    def update_last_times(self, rang, temps, delta):
        """Met à jour la liste des derniers temps affichés avec le delta."""
        entry = f"Place : {rang} - Temps : {temps} - Delta : {delta}"
        self.last_times.insert(0, entry)  # Ajoute en haut de la liste
        if len(self.last_times) > 5:  # Garde seulement les 5 derniers temps
            self.last_times.pop()

        # Mise à jour de l'affichage
        self.last_times_listbox.delete("0.0", "end")
        for item in self.last_times:
            self.last_times_listbox.insert("end", item + "\n")

# Lancer l'application
root = ctk.CTk()
chronometre = Chronometre(root)
root.mainloop()
