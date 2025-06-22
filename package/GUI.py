import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
import datetime
from package.package_class_base import Client, Evenement, Reservation, Billet

# ---Chemins des fichiers JSON---
# Ces chemins sont relatifs au script en cours d'exécution.
CHEMIN_DONNEES_CLIENTS = 'données.json'
CHEMIN_DONNEES_EVENTS = 'données_event.json'

# ---Variables globales pour les données de l'application---
# Utilisées pour stocker les instances d'objets chargées depuis les JSON ou créées pendant l'exécution.
clients_objects: list[Client] = []
evenements_objects: list[Evenement] = []
reservations_objects: list[Reservation] = [] # Pour stocker toutes les réservations
utilisateur_actif: Client | None = None # L'utilisateur actuellement connecté

# ---Fonction pour obtenir le chemin absolu du fichier JSON---
def obtenir_chemin_fichier_json(nom_fichier: str) -> Path:
    """Retourne le chemin absolu du fichier JSON."""
    chemin_script = Path(__file__).resolve()
    chemin_dossier_script = chemin_script.parent
    return chemin_dossier_script / nom_fichier

# ---Fonctions de chargement des données---
def charger_donnees_clients():
    """Charge les données des clients depuis le fichier JSON et crée les objets Client."""
    global clients_objects
    chemin_fichier = obtenir_chemin_fichier_json(CHEMIN_DONNEES_CLIENTS)
    
    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        donnees_json = json.load(file)
    clients_objects = [Client(idClient=c['idclient'], nom=c['nom'], email=c['email'], mdp=c['password']) for c in donnees_json]

# ---Fonction pour charger les événements depuis le fichier JSON---
def charger_donnees_evenements():
    """Charge les données des événements depuis le fichier JSON et crée les objets Evenement."""
    global evenements_objects
    chemin_fichier = obtenir_chemin_fichier_json(CHEMIN_DONNEES_EVENTS)
    
    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        donnees_json = json.load(file)
    evenements_objects = [
        Evenement(
            id_event=i['id'], 
            nom=i['nom'], 
            date=i['date'], 
            lieu=i['lieu'], 
            description=i['description'], 
            places=i['places'], 
            prix=float(i['prix'])
        ) for i in donnees_json
    ]

# ---Initialisation des données au démarrage de l'application---
# Ces fonctions sont appelées une fois pour charger les données en mémoire.
charger_donnees_clients()
charger_donnees_evenements()

# ---Fonction pour afficher les détails de l'événement sélectionné---
def afficher_details_evenement(event, label):
    """Affiche les détails de l'événement sélectionné dans la Listbox.
    Cette fonction est appelée lorsque l'utilisateur sélectionne un événement dans la Listbox.
    Elle récupère l'index de l'événement sélectionné et affiche ses détails dans le label spécifié."""
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        # Utilisation de la liste d'objets Evenement
        evenement_obj = evenements_objects[index] 
        # Utilisation de la méthode afficher_details de l'objet Evenement
        details = evenement_obj.afficher_details() 
        label.config(text=details)
    else:
        label.config(text="Sélectionnez un événement pour voir les détails.")

# ---Fonction pour obtenir le prochain ID de réservation unique---
# la variable globale _prochain_id_reservation est utilisée pour générer des IDs uniques pour les réservations.
# Elle commence à 1 et s'incrémente à chaque nouvelle réservation.
_prochain_id_reservation = 1
def obtenir_prochain_id_reservation() -> int:
    """Génère un ID unique pour une nouvelle réservation."""
    global _prochain_id_reservation
    id_res = _prochain_id_reservation
    _prochain_id_reservation += 1
    return id_res

# --- Fonctions pour les actions de l'utilisateur ---
def effectuer_reservation_gui(list_evene_widget, entry_nb_billets_widget, listbox_mes_billets_widget, lbl_details_evenement_widget):
    """Gère la logique de réservation de billets à partir de l'interface graphique."""
    global utilisateur_actif, evenements_objects, reservations_objects

    selection = list_evene_widget.curselection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un événement.")
        return
    
    index_evenement_selectionne = selection[0]
    evenement_selectionne = evenements_objects[index_evenement_selectionne]

    try:
        nb_billets_str = entry_nb_billets_widget.get()
        nb_billets = int(nb_billets_str)
        if nb_billets <= 0:
            messagebox.showerror("Nombre invalide", "Le nombre de billets doit être positif.")
            return
    except ValueError:
        messagebox.showerror("Entrée invalide", "Veuillez entrer un nombre valide pour les billets.")
        return

    # Vérifier la disponibilité avant de créer la réservation
    if not evenement_selectionne.verifier_disponibilite_places(nb_billets):
        messagebox.showinfo("Places insuffisantes", 
                            f"Il ne reste que {evenement_selectionne.places_disponibles} place(s) pour {evenement_selectionne.nom}.")
        return

    # Création de la réservation
    id_nouvelle_reservation = obtenir_prochain_id_reservation()
    nouvelle_reservation = Reservation(idReservation=id_nouvelle_reservation,
                                       idClient=utilisateur_actif.idClient,
                                       dateReservation=datetime.datetime.now())

    # Ajout des billets à la réservation
    # La méthode ajouterBillet de Reservation gère maintenant la mise à jour des places de l'événement
    if nouvelle_reservation.ajouterBillet(evenement=evenement_selectionne, quantite=nb_billets):
        utilisateur_actif.effectuerReservation(nouvelle_reservation)
        reservations_objects.append(nouvelle_reservation) # Garder une trace de toutes les réservations
        
        messagebox.showinfo("Réservation réussie", 
                            f"{nb_billets} billet(s) réservé(s) pour {evenement_selectionne.nom}.\n"
                            f"ID de la réservation: {nouvelle_reservation.idReservation}\n"
                            f"Montant total: {nouvelle_reservation.montantTotal} €")
        
        # Mettre à jour l'affichage des événements (nombre de places)
        list_evene_widget.delete(index_evenement_selectionne)
        list_evene_widget.insert(index_evenement_selectionne, 
                                 f"{evenement_selectionne.date} - {evenement_selectionne.nom} ({evenement_selectionne.places_disponibles} places)")
        list_evene_widget.selection_set(index_evenement_selectionne) # Re-sélectionner pour actualiser les détails

        # Mettre à jour les détails de l'événement affichés
        if lbl_details_evenement_widget:
             lbl_details_evenement_widget.config(text=evenement_selectionne.afficher_details())

        # Mettre à jour la liste "Mes Billets"
        actualiser_liste_mes_billets(listbox_mes_billets_widget)

# ---Fonction pour actualiser la liste des billets de l'utilisateur actif---
def actualiser_liste_mes_billets(listbox_widget):
    """Met à jour la Listbox affichant les billets de l'utilisateur actif."""
    listbox_widget.delete(0, tk.END) # Effacer les anciens billets
    if utilisateur_actif and hasattr(utilisateur_actif, 'reservations'):
        for reservation in utilisateur_actif.reservations:
            for billet in reservation.billets:
                # Trouver le nom de l'événement associé au billet
                evenement_associe = next((i for i in evenements_objects if i.id_event == billet.id_event), None)
                nom_evenement = evenement_associe.nom
                # Ajouter les détails du billet à la Listbox
                listbox_widget.insert(tk.END, billet.afficher_details_billet(nom_evenement=nom_evenement))

# ---Fonction pour annuler une réservation/billet à partir de l'interface graphique---
def annuler_billet_reservation_gui(entry_billet_id_annul_widget, list_evene_widget, listbox_mes_billets_widget, lbl_details_evenement_widget):
    """Gère la logique d'annulation d'une réservation/billet à partir de l'interface graphique."""
    global utilisateur_actif, evenements_objects, reservations_objects

    try:
        id_reservation_a_annuler_str = entry_billet_id_annul_widget.get()
        if not id_reservation_a_annuler_str.strip():
            messagebox.showwarning("Champ vide", "Veuillez entrer l'ID de la réservation à annuler.")
            return
        id_reservation_a_annuler = int(id_reservation_a_annuler_str)
    except ValueError:
        messagebox.showerror("Entrée invalide", "L'ID de la réservation doit être un nombre.")
        return

    # Trouver la réservation dans la liste globale des réservations
    reservation_a_annuler = next((i for i in reservations_objects if i.idReservation == id_reservation_a_annuler and i.idClient == utilisateur_actif.idClient), None)

    if not reservation_a_annuler:
        messagebox.showerror("Erreur", f"Aucune réservation active trouvée avec l'ID {id_reservation_a_annuler} pour vous.")
        return
        
    # L'ID de l'événement est nécessaire pour la méthode annulerReservation de Reservation
    # On suppose que tous les billets d'une réservation sont pour le même événement (simplification)
    id_event_concerne = reservation_a_annuler.billets[0].id_event
    
    # La méthode annulerReservation de la classe Reservation s'occupe de remettre les places
    # et de vider la liste des billets de la réservation.
    # Elle a besoin de la liste globale des événements pour trouver l'objet Evenement à mettre à jour.
    if reservation_a_annuler.annulerReservation(evenements_data=evenements_objects):
        # Retirer la réservation de la liste des réservations de l'utilisateur
        if reservation_a_annuler in utilisateur_actif.reservations:
             utilisateur_actif.reservations.remove(reservation_a_annuler)
        # Optionnel: Retirer de la liste globale si on ne veut plus la suivre du tout
        if reservation_a_annuler in reservations_objects:
            reservations_objects.remove(reservation_a_annuler)
        
        # Mettre à jour l'affichage des événements (nombre de places)
        index_evenement_maj = next(i for i, evt in enumerate(evenements_objects) if evt.id_event == id_event_concerne)
        evenement_maj = evenements_objects[index_evenement_maj]
        list_evene_widget.delete(index_evenement_maj)
        list_evene_widget.insert(index_evenement_maj, f"{evenement_maj.date} - {evenement_maj.nom} ({evenement_maj.places_disponibles} places)")
            
        # Si l'événement annulé était sélectionné, mettre à jour ses détails
        selection_courante = list_evene_widget.curselection()
        if selection_courante and selection_courante[0] == index_evenement_maj:
            if lbl_details_evenement_widget:
                lbl_details_evenement_widget.config(text=evenement_maj.afficher_details())
            
        # Mettre à jour la liste "Mes Billets"
        actualiser_liste_mes_billets(listbox_mes_billets_widget)
        entry_billet_id_annul_widget.delete(0, tk.END) # Vider le champ après annulation
    else:
        messagebox.showerror("Échec de l'annulation", f"L'annulation de la réservation {id_reservation_a_annuler} a échoué.")

# ---Fonction pour afficher la fenêtre de connexion---
def afficher_fenetre_login():
    """Affiche la fenêtre de connexion."""
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
        nom_utilisateur = entry_nom_utilisateur.get()
        mot_de_passe = entry_mot_de_passe.get()

        global utilisateur_actif # Indiquer qu'on modifie la variable globale
        utilisateur_trouve = None
        for client_obj in clients_objects:
            if client_obj.nom == nom_utilisateur and client_obj.mdp == mot_de_passe:
                utilisateur_trouve = client_obj
                break
        
        if utilisateur_trouve:
            utilisateur_actif = utilisateur_trouve
            # Initialiser les réservations de l'utilisateur actif
            if hasattr(utilisateur_actif, 'reservations'):
                 utilisateur_actif.reservations = [] 
            else: # S'assurer que l'attribut existe
                utilisateur_actif.reservations = []

            fenetre_login.destroy()
            afficher_fenetre_principale()
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

    # --- Section Utilisateur ---
    user_frame = ttk.LabelFrame(frame_princip, text="Utilisateur", padding="10")
    user_frame.pack(fill=tk.X, pady=5)
    user_status = ttk.Label(user_frame, text=f"Utilisateur Actif: {utilisateur_actif.nom}", style="Header.TLabel")
    user_status.pack(side=tk.LEFT, padx=5)

    # ---Bouton pour changer d'utilisateur---
    def detruire_fenetre():
        """Ferme la fenêtre principale et retourne à la fenêtre de connexion."""
        fenetre_principale.destroy()
        afficher_fenetre_login() # Recharge la fenêtre de login, réinitialisant l'état global si nécessaire
    ttk.Button(user_frame, text="Changer d'Utilisateur", command=detruire_fenetre).pack(side=tk.RIGHT)

    # ---Boutons pour la Newsletter---
    # Cadre pour les boutons de newsletter pour un meilleur agencement
    newsletter_frame = ttk.Frame(user_frame)
    newsletter_frame.pack(side=tk.RIGHT, padx=10)
    ttk.Button(newsletter_frame, text="S'abonner Newsletter", command=None).pack(side=tk.LEFT)
    # Ajout d'un bouton de désabonnement
    ttk.Button(newsletter_frame, text="Se désabonner", command=None).pack(side=tk.LEFT, padx=5)
    
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
    lbl_details_evenement.pack(anchor=tk.NW, fill=tk.X)

    # ---Remplissage de la Listbox avec les événements---
    # Utilisation des objets Evenement chargés
    for evenement_obj in evenements_objects:
        list_evene.insert(tk.END, f"{evenement_obj.date} - {evenement_obj.nom} ({evenement_obj.places_disponibles} places)")

    # --- Section Actions (Réservation / Annulation) ---
    frame_action = ttk.LabelFrame(frame_princip, text="Actions", padding="10")
    frame_action.pack(fill=tk.X, pady=5)

    # ---Réservation---
    frame_reserv = ttk.Frame(frame_action)
    frame_reserv.pack(fill=tk.X, pady=5)
    ttk.Label(frame_reserv, text="Nb Billets:").pack(side=tk.LEFT, padx=5)
    entry_nb_billets = ttk.Entry(frame_reserv, width=3)
    entry_nb_billets.insert(0, "1") # Valeur par défaut
    entry_nb_billets.pack(side=tk.LEFT, padx=5)
    # Connection de la fonction de réservation au bouton
    ttk.Button(frame_reserv, text="Réserver Billets", 
               command=lambda: effectuer_reservation_gui(list_evene, entry_nb_billets, listbox_mes_billets, lbl_details_evenement)
              ).pack(side=tk.LEFT, padx=5)

    # ---Annulation---
    frame_annula = ttk.Frame(frame_action)
    frame_annula.pack(fill=tk.X, pady=5)
    ttk.Label(frame_annula, text="ID Réservation à Annuler:").pack(side=tk.LEFT, padx=5) # Texte clarifié
    entry_billet_id_annul = ttk.Entry(frame_annula, width=5)
    entry_billet_id_annul.pack(side=tk.LEFT, padx=5)
    # Connection de la fonction d'annulation au bouton
    ttk.Button(frame_annula, text="Annuler Réservation", # Texte clarifié
               command=lambda: annuler_billet_reservation_gui(entry_billet_id_annul, list_evene, listbox_mes_billets, lbl_details_evenement)
              ).pack(side=tk.LEFT, padx=5)

    # ---Section Mes Billets---
    frame_billet = ttk.LabelFrame(frame_princip, text="Mes Billets (Réservations Actives)", padding="10") # Titre clarifié
    frame_billet.pack(fill=tk.X, pady=5)

    listbox_mes_billets = tk.Listbox(frame_billet, height=5, font=('Consolas', 10))
    listbox_mes_billets.pack(fill=tk.X, expand=True, padx=(0,10), side=tk.LEFT) # side=tk.LEFT pour permettre au bouton d'être à côté
    
    scrollbar_mes_billets = ttk.Scrollbar(frame_billet, orient=tk.VERTICAL, command=listbox_mes_billets.yview)
    scrollbar_mes_billets.pack(side=tk.LEFT, fill=tk.Y) # Scrollbar à gauche de la listbox
    listbox_mes_billets.config(yscrollcommand=scrollbar_mes_billets.set)

    # Appel initial pour charger les billets si l'utilisateur en a déjà (peu probable à ce stade, mais bonne pratique)
    actualiser_liste_mes_billets(listbox_mes_billets)
    
    fenetre_principale.mainloop()