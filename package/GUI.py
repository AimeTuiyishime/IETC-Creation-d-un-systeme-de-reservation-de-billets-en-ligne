import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

données = '/Users/aime/EXO_PROGAM/CPOO/PROJET/CPOO_Projet/package/données.json'
chemin_script = Path(__file__).resolve() # Obtient le chemin absolu du script
chemin_dossier_script = chemin_script.parent # Obtient le dossier contenant le script
chemin_fichier_json = chemin_dossier_script / données# Combine les chemins de manière OS-agnostique
with open(chemin_fichier_json, 'r', encoding='utf-8') as file:
    données = json.load(file)

def valider_connexion():
    """Récupère le nom d'utilisateur et le mot de passe et affiche un message."""
    nom_utilisateur = entry_nom_utilisateur.get()
    mot_de_passe = entry_mot_de_passe.get()

    for i in range(len(données)):
        if nom_utilisateur == données[i]['nom'] and mot_de_passe == données[i]['password']:
            fenetre_login.destroy()
            messagebox.showinfo("Connexion Réussie", "Connexion réussie !")
            afficher_fenetre_principale()
            break
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

def afficher_fenetre_principale():
    """Crée et affiche la fenêtre principale après une connexion réussie."""
    fenetre_principale = tk.Tk()
    fenetre_principale.title("Tableau de bord")
    fenetre_principale.geometry("400x300") # Taille de la nouvelle fenêtre

    # Centrer la nouvelle fenêtre
    largeur_fenetre_p = 400
    hauteur_fenetre_p = 300
    largeur_ecran = fenetre_principale.winfo_screenwidth()
    hauteur_ecran = fenetre_principale.winfo_screenheight()
    x_coordonnee_p = int((largeur_ecran / 2) - (largeur_fenetre_p / 2))
    y_coordonnee_p = int((hauteur_ecran / 2) - (hauteur_fenetre_p / 2))
    fenetre_principale.geometry(f"{largeur_fenetre_p}x{hauteur_fenetre_p}+{x_coordonnee_p}+{y_coordonnee_p}")

    label_accueil = tk.Label(fenetre_principale, text="Bienvenue dans l'application !", font=("Arial", 16))
    label_accueil.pack(pady=20)

    # Vous pouvez ajouter d'autres widgets à cette fenêtre principale ici
    bouton_quitter_principal = tk.Button(fenetre_principale, text="Quitter", command=fenetre_principale.destroy)
    bouton_quitter_principal.pack(pady=10)

    fenetre_principale.mainloop()

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