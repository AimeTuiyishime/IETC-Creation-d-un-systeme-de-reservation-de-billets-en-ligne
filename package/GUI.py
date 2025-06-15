import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# ---Chemins des fichiers JSON---
données = 'données.json'
données_event = 'données_event.json'

# ---Fonction pour obtenir le chemin absolu du fichier JSON--
def obtenir_chemin_fichier_json(nom_fichier):
    """Retourne le chemin absolu du fichier JSON.
    Cette fonction combine le chemin du script actuel avec le nom du fichier JSON
    pour garantir que le chemin est correct, quel que soit le système d'exploitation.
    """
    chemin_script = Path(__file__).resolve()  # Obtient le chemin absolu du script
    chemin_dossier_script = chemin_script.parent  # Obtient le dossier contenant le script
    chemin_fichier_json = chemin_dossier_script / nom_fichier  # Combine les chemins de manière OS-agnostique
    return chemin_fichier_json

# ---Chargement des données depuis les fichiers JSON---
with open(obtenir_chemin_fichier_json(données), 'r', encoding='utf-8') as file:
    données = json.load(file)
with open(obtenir_chemin_fichier_json(données_event), 'r', encoding='utf-8') as file:
    données_event = json.load(file)

# ---Fonction pour afficher la fenêtre de connexion---
def afficher_fenetre_login():
    """Affiche la fenêtre de connexion.
    Cette fonction crée une fenêtre de connexion avec des champs pour le nom d'utilisateur et le mot de passe,
    ainsi qu'un bouton pour valider la connexion.
    Elle est appelée au démarrage du script pour permettre à l'utilisateur de se connecter."""
    # ---Création de la fenêtre login---
    fenetre_login = tk.Tk()
    fenetre_login.title("Connexion")

    # ---Style---
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", padding=5, font=('Helvetica', 10))
    style.configure("TButton", padding=5, font=('Helvetica', 10, 'bold'))
    style.configure("TEntry", padding=5, font=('Helvetica', 10))
    style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'))

    # ---Définir les dimensions de la fenêtre---
    largeur_fenetre = 300
    hauteur_fenetre = 195

    # ---Obtenir les dimensions de l'écran---
    largeur_ecran = fenetre_login.winfo_screenwidth()
    hauteur_ecran = fenetre_login.winfo_screenheight()

    # ---Calculer les coordonnées x et y pour centrer la fenêtre---
    x_coordonnee = int((largeur_ecran / 2) - (largeur_fenetre / 2))
    y_coordonnee = int((hauteur_ecran / 2) - (hauteur_fenetre / 2))

    # ---Définir la géométrie de la fenêtre pour la centrer---
    fenetre_login.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x_coordonnee}+{y_coordonnee}")

    # ---Étiquette et champ de saisie pour le nom d'utilisateur---
    label_nom_utilisateur = tk.Label(fenetre_login, text="Nom d'utilisateur:")
    label_nom_utilisateur.pack(pady=5)

    entry_nom_utilisateur = tk.Entry(fenetre_login)
    entry_nom_utilisateur.pack(pady=5)
    entry_nom_utilisateur.focus_set() # Met le focus sur ce champ au démarrage

    # ---Étiquette et champ de saisie pour le mot de passe---
    label_mot_de_passe = tk.Label(fenetre_login, text="Mot de passe:")
    label_mot_de_passe.pack(pady=5)

    entry_mot_de_passe = tk.Entry(fenetre_login, show="*") # show="*" masque le mot de passe
    entry_mot_de_passe.pack(pady=5)

    # ---Fonction pour valider la connexion---
    def valider_connexion():
        """Récupère le nom d'utilisateur et le mot de passe et affiche un message.
        Si les informations sont correctes, ferme la fenêtre de connexion et affiche la fenêtre principale."""
        nom_utilisateur = entry_nom_utilisateur.get() # Récupération du nom d'utilisateur
        mot_de_passe = entry_mot_de_passe.get() # Récupération du mot de passe

        for i in range(len(données)):
            if nom_utilisateur == données[i]['nom'] and mot_de_passe == données[i]['password']: # Vérification des informations de connexion
                fenetre_login.destroy()
                afficher_fenetre_principale()
                break
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    # ---Bouton de connexion---
    bouton_connexion = tk.Button(fenetre_login, text="Se connecter", command=valider_connexion)
    bouton_connexion.pack(pady=10)

    # ---Lier la touche "Entrée" à la fonction de validation pour toute la fenêtre---
    fenetre_login.bind('<Return>', lambda event: valider_connexion()) # Permet de valider la connexion en appuyant sur "Entrée"

    # ---Lancer la fenêtre de connexion---
    fenetre_login.mainloop()

# ---Fonction pour afficher la fenêtre principale après une connexion réussie---
def afficher_fenetre_principale():
    """Crée et affiche la fenêtre principale. 
    Affiche les événements disponibles et permet la réservation de billets.
    """
    fenetre_principale = tk.Tk()
    fenetre_principale.title("Réservation de billets")
    fenetre_principale.geometry("900x800") # Taille de la nouvelle fenêtre

    # ---Style---
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", padding=5, font=('Helvetica', 10))
    style.configure("TButton", padding=5, font=('Helvetica', 10, 'bold'))
    style.configure("TEntry", padding=5, font=('Helvetica', 10))
    style.configure("TListbox", font=('Helvetica', 10))
    style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'))

    # ---Centrer la nouvelle fenêtre---
    largeur_fenetre_p = 900
    hauteur_fenetre_p = 800
    largeur_ecran = fenetre_principale.winfo_screenwidth()
    hauteur_ecran = fenetre_principale.winfo_screenheight()
    x_coordonnee_p = int((largeur_ecran / 2) - (largeur_fenetre_p / 2))
    y_coordonnee_p = int((hauteur_ecran / 2) - (hauteur_fenetre_p / 2))
    fenetre_principale.geometry(f"{largeur_fenetre_p}x{hauteur_fenetre_p}+{x_coordonnee_p}+{y_coordonnee_p}")

    # ---Configure les éléments de l'interface utilisateur---
    frame_princip = ttk.Frame(fenetre_principale, padding="10")
    frame_princip.pack(expand=True, fill=tk.BOTH)

    # ---Section Événements---
    frame_evene = ttk.LabelFrame(frame_princip, text="Événements Disponibles", padding="10")
    frame_evene.pack(expand=True, fill=tk.BOTH, pady=5)

    list_evene = tk.Listbox(frame_evene, height=10, exportselection=False, font=('Consolas', 10))
    list_evene.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
    list_evene.bind('<<ListboxSelect>>', lambda event: afficher_details_evenement(event, lbl_details_evenement)) # Affiche les détails de l'événement sélectionné

    scrollbar_evene = ttk.Scrollbar(frame_evene, orient=tk.VERTICAL, command=list_evene.yview)
    scrollbar_evene.pack(side=tk.LEFT, fill=tk.Y)
    list_evene.config(yscrollcommand=scrollbar_evene.set) # La scrollbar sera gérée par la listbox

    # ---Section Détails Événement---
    details_frame_evene = ttk.Frame(frame_evene)
    details_frame_evene.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
    ttk.Label(details_frame_evene, text="Détails de l'Événement:", style="Header.TLabel").pack(anchor=tk.W, pady=(0,10))
    lbl_details_evenement = ttk.Label(details_frame_evene, text="Sélectionnez un événement pour voir les détails.", justify=tk.LEFT, wraplength=300)
    lbl_details_evenement.pack(anchor=tk.NW, fill=tk.X) # Permet de remplir le label avec les détails de l'événement sélectionné

    # ---Remplissage de la Listbox avec les événements---
    for evenement in données_event:
        list_evene.insert(tk.END, f"{evenement['date']} - {evenement['nom']}")

    # --- Section Actions (Réservation / Annulation) ---
    frame_action = ttk.LabelFrame(frame_princip, text="Actions", padding="10")
    frame_action.pack(fill=tk.X, pady=5)

    # ---Réservation---
    frame_reserv = ttk.Frame(frame_action)
    frame_reserv.pack(fill=tk.X, pady=5)
    ttk.Label(frame_reserv, text="Nb Billets:").pack(side=tk.LEFT, padx=5)
    entry_nb_billets = ttk.Entry(frame_reserv, width=3)
    entry_nb_billets.insert(0, 1)
    entry_nb_billets.pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_reserv, text="Réserver Billets", command=None).pack(side=tk.LEFT, padx=5)

    # ---Annulation---
    frame_annula = ttk.Frame(frame_action)
    frame_annula.pack(fill=tk.X, pady=5)
    ttk.Label(frame_annula, text="Billet à Annuler:").pack(side=tk.LEFT, padx=5)
    entry_billet_id_annul = ttk.Entry(frame_annula, width=5)
    entry_billet_id_annul.pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_annula, text="Annuler Billet", command=None).pack(side=tk.LEFT, padx=5)

    # ---Section Mes Billets---
    frame_billet = ttk.LabelFrame(frame_princip, text="Mes Billets", padding="10")
    frame_billet.pack(fill=tk.X, pady=5)

    listbox_mes_billets = tk.Listbox(frame_billet, height=5, font=('Consolas', 10))
    listbox_mes_billets.pack(fill=tk.X, expand=True, padx=(0,10))
    scrollbar_mes_billets = ttk.Scrollbar(frame_billet, orient=tk.VERTICAL, command=listbox_mes_billets.yview)
    listbox_mes_billets.config(yscrollcommand=scrollbar_mes_billets.set) # La scrollbar sera gérée par la listbox

    ttk.Button(frame_billet, text="Voir Mes Billets Actifs", command=None).pack(side=tk.LEFT, padx=5, pady=5)

# ---Fonction pour afficher les détails de l'événement sélectionné---
def afficher_details_evenement(event, label):
    """Affiche les détails de l'événement sélectionné dans la Listbox.
    Cette fonction est appelée lorsque l'utilisateur sélectionne un événement dans la Listbox.
    Elle récupère l'index de l'événement sélectionné et affiche ses détails dans le label spécifié."""
    selection = event.widget.curselection() # Récupère la sélection actuelle de la Listbox
    if selection:
        index = selection[0]
        evenement = données_event[index]
        details = f"Nom: {evenement['nom']}\nDate: {evenement['date']}\nLieu: {evenement['lieu']}\nDescription: {evenement['description']}\nPrix: {evenement['prix']} €\nPlaces disponibles: {evenement['places']}"
        label.config(text=details) # Affiche les détails de l'événement sélectionné
    else:
        label.config(text="Sélectionnez un événement pour voir les détails.")