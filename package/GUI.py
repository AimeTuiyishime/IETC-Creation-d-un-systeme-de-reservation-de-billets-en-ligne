import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# Chemins des fichiers JSON
données = 'données.json'
données_event = 'données_event.json'

# Fonction pour obtenir le chemin absolu du fichier JSON
def obtenir_chemin_fichier_json(nom_fichier):
    """Retourne le chemin absolu du fichier JSON."""
    chemin_script = Path(__file__).resolve()  # Obtient le chemin absolu du script
    chemin_dossier_script = chemin_script.parent  # Obtient le dossier contenant le script
    chemin_fichier_json = chemin_dossier_script / nom_fichier  # Combine les chemins de manière OS-agnostique
    return chemin_fichier_json

# Chargement des données depuis les fichiers JSON
with open(obtenir_chemin_fichier_json(données), 'r', encoding='utf-8') as file:
    données = json.load(file)
with open(obtenir_chemin_fichier_json(données_event), 'r', encoding='utf-8') as file:
    données_event = json.load(file)

# Fonction pour valider la connexion
def valider_connexion():
    """Récupère le nom d'utilisateur et le mot de passe et affiche un message."""
    nom_utilisateur = entry_nom_utilisateur.get()
    mot_de_passe = entry_mot_de_passe.get()

    for i in range(len(données)):
        if nom_utilisateur == données[i]['nom'] and mot_de_passe == données[i]['password']:
            fenetre_login.destroy()
            afficher_fenetre_principale()
            break
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# Fonction pour afficher la fenêtre principale après une connexion réussie
def afficher_fenetre_principale():
    """Crée et affiche la fenêtre principale après une connexion réussie."""
    fenetre_principale = tk.Tk()
    fenetre_principale.title("Réservation de billets")
    fenetre_principale.geometry("800x600") # Taille de la nouvelle fenêtre

    # Centrer la nouvelle fenêtre
    largeur_fenetre_p = 800
    hauteur_fenetre_p = 600
    largeur_ecran = fenetre_principale.winfo_screenwidth()
    hauteur_ecran = fenetre_principale.winfo_screenheight()
    x_coordonnee_p = int((largeur_ecran / 2) - (largeur_fenetre_p / 2))
    y_coordonnee_p = int((hauteur_ecran / 2) - (hauteur_fenetre_p / 2))
    fenetre_principale.geometry(f"{largeur_fenetre_p}x{hauteur_fenetre_p}+{x_coordonnee_p}+{y_coordonnee_p}")

    # --- Section pour la liste d'événements ---
    events_frame = ttk.LabelFrame(fenetre_principale)
    events_frame.pack(expand=True, fill=tk.BOTH, pady=20)

    # Titre de la section
    dispo_event_frame = ttk.Frame(events_frame)
    dispo_event_frame.pack(side=tk.TOP, fill=tk.X, padx=0)   
    ttk.Label(dispo_event_frame, text="Événements Disponibles:", style="Header.TLabel").pack(anchor=tk.W, pady=(0,5))

    # Listbox pour afficher les événements
    listbox_evenements = tk.Listbox(events_frame, height=10, exportselection=False, font=('Consolas', 10))
    listbox_evenements.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

    # Lier la sélection de la Listbox à l'affichage des détails de l'événement    
    scrollbar_evenements = ttk.Scrollbar(events_frame, orient=tk.VERTICAL, command=listbox_evenements.yview)
    scrollbar_evenements.pack(side=tk.LEFT, fill=tk.Y)
    listbox_evenements.config(yscrollcommand=scrollbar_evenements.set)
    listbox_evenements.bind('<<ListboxSelect>>', lambda event: afficher_details_evenement(event, lbl_details_evenement))

    # Remplissage de la Listbox avec les événements
    for evenement in données_event:
        listbox_evenements.insert(tk.END, f"{evenement['date']} - {evenement['nom']}")

    # --- Section Détails Événement ---
    details_event_frame = ttk.Frame(events_frame)
    details_event_frame.pack(side=tk.TOP, fill=tk.X, padx=0)

    # Titre de la section    
    ttk.Label(details_event_frame, text="Détails de l'Événement:", style="Header.TLabel").pack(anchor=tk.W, pady=(0,10))
    lbl_details_evenement = ttk.Label(details_event_frame, text="Sélectionnez un événement pour voir les détails.", justify=tk.LEFT, wraplength=300)
    lbl_details_evenement.pack(anchor=tk.NW, fill=tk.X)

    fenetre_principale.mainloop()

# Fonction pour afficher les détails de l'événement sélectionné
def afficher_details_evenement(event, label):
    """Affiche les détails de l'événement sélectionné dans la Listbox."""
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        evenement = données_event[index]
        details = f"Nom: {evenement['nom']}\nDate: {evenement['date']}\nLieu: {evenement['lieu']}\nDescription: {evenement['description']}\nPrix: {evenement['prix']} €\nPlaces disponibles: {evenement['places']}"
        label.config(text=details)
    else:
        label.config(text="Sélectionnez un événement pour voir les détails.")

# Création de la fenêtre login
fenetre_login = tk.Tk()
fenetre_login.title("Connexion")

# Définir les dimensions de la fenêtre
largeur_fenetre = 300
hauteur_fenetre = 190

# Obtenir les dimensions de l'écran
largeur_ecran = fenetre_login.winfo_screenwidth()
hauteur_ecran = fenetre_login.winfo_screenheight()

# Calculer les coordonnées x et y pour centrer la fenêtre
x_coordonnee = int((largeur_ecran / 2) - (largeur_fenetre / 2))
y_coordonnee = int((hauteur_ecran / 2) - (hauteur_fenetre / 2))

# Définir la géométrie de la fenêtre pour la centrer
fenetre_login.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x_coordonnee}+{y_coordonnee}")

# Étiquette et champ de saisie pour le nom d'utilisateur
label_nom_utilisateur = tk.Label(fenetre_login, text="Nom d'utilisateur:")
label_nom_utilisateur.pack(pady=5) # pady ajoute un peu d'espace vertical

entry_nom_utilisateur = tk.Entry(fenetre_login)
entry_nom_utilisateur.pack(pady=5)
entry_nom_utilisateur.focus_set() # Met le focus sur ce champ au démarrage

# Étiquette et champ de saisie pour le mot de passe
label_mot_de_passe = tk.Label(fenetre_login, text="Mot de passe:")
label_mot_de_passe.pack(pady=5)

entry_mot_de_passe = tk.Entry(fenetre_login, show="*") # show="*" masque le mot de passe
entry_mot_de_passe.pack(pady=5)

# Bouton de connexion
bouton_connexion = tk.Button(fenetre_login, text="Se connecter", command=valider_connexion)
bouton_connexion.pack(pady=10)

# Lier la touche "Entrée" à la fonction de validation pour toute la fenêtre
fenetre_login.bind('<Return>', lambda event: valider_connexion())