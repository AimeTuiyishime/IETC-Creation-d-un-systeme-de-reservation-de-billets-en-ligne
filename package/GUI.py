import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
import datetime
from package.package_class_base import Client, Evenement, Reservation, Billet
from package.package_class_additionnel import Newsletter, Paiement, Lieu, CategorieSiege, Siege as SiegeConfig # SiegeConfig est utilisé pour la configuration statique des sièges

# ---Chemins des fichiers JSON---
# Ces chemins sont relatifs au script en cours d'exécution.
CHEMIN_DONNEES_CLIENTS = 'données_clients.json'
CHEMIN_DONNEES_EVENTS = 'données_event.json'
CHEMIN_CONFIGS_LIEUX = 'donnees_configurations_lieux.json'

# ---Variables globales pour les données de l'application---
# Utilisées pour stocker les instances d'objets chargées depuis les JSON ou créées pendant l'exécution.
clients_objects: list[Client] = [] # Liste des clients chargés depuis le JSON
evenements_objects: list[Evenement] = [] # Liste des événements chargés
reservations_objects: list[Reservation] = [] # Pour stocker toutes les réservations
utilisateur_actif: Client | None = None # L'utilisateur actuellement connecté
abonnements_newsletter_objects: list[Newsletter] = [] # Liste pour stocker les objets Newsletter
LISTE_CONFIGS_LIEUX: list[Lieu] = [] # Pour stocker les configurations de lieux chargées

_prochain_id_abonnement_newsletter = 1 # Pour générer des ID uniques pour les abonnements
_prochain_id_paiement = 1 # Pour générer des ID uniques pour les paiements

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
    evenements_temp = []
    for event_data in donnees_json:
        # Création initiale de l'objet Evenement
        evenement_obj = Evenement(
            id_event=event_data['id'],
            nom=event_data['nom'],
            date=event_data['date'],
            lieu_nom_str=event_data['lieu'], # Nom du lieu (str)
            description=event_data['description']
        )
        
        # Trouver la configuration du lieu correspondante
        config_lieu_trouvee = next((lc for lc in LISTE_CONFIGS_LIEUX if lc.nomLieu == event_data['lieu']), None)
        
        if config_lieu_trouvee:
            # Lier la configuration du lieu à l'événement
            evenement_obj.lier_config_lieu_et_initialiser_etat_sieges(config_lieu_trouvee) # Nom de méthode mis à jour
            evenements_temp.append(evenement_obj)
        else:
            print(f"Attention: Configuration de lieu non trouvée pour '{event_data['lieu']}' pour l'événement '{event_data['nom']}'. L'événement ne sera pas chargé.")
                
    evenements_objects = evenements_temp


# ---Fonction pour charger les configurations des lieux---
def charger_configurations_lieux():
    """Charge les configurations des lieux depuis le fichier JSON et crée les objets LieuConfig."""
    global LISTE_CONFIGS_LIEUX
    chemin_fichier = obtenir_chemin_fichier_json(CHEMIN_CONFIGS_LIEUX)
    
    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        donnees_json = json.load(file)
    
    configs_temp = []
    for lieu_data in donnees_json:
        categories_config_pour_lieu = []
        for cat_data in lieu_data.get('categories', []):
            sieges_config_pour_categorie = []
            for siege_data in cat_data.get('sieges', []):
                # L'état 'disponible' du JSON est l'état initial, la classe Siege le prend par défaut à True
                siege_obj = SiegeConfig(idSiege=siege_data['idSiege'],
                                        identificationSiege=siege_data['identification'],
                                        disponible=siege_data.get('disponible', True))
                sieges_config_pour_categorie.append(siege_obj)
            
            categorie_config_obj = CategorieSiege(
                idCategorieSiege=cat_data['idCategorieSiege'],
                nomCategorie=cat_data['nomCategorie'],
                prix=float(cat_data['prix']),
                sieges=sieges_config_pour_categorie
            )
            categories_config_pour_lieu.append(categorie_config_obj)
        
        lieu_config_obj = Lieu(
            nomLieu=lieu_data['nomLieu'],
            adresse=lieu_data['adresse'],
            capaciteTotaleIndicative=int(lieu_data['capaciteTotaleIndicative']),
            categories=categories_config_pour_lieu
        )
        configs_temp.append(lieu_config_obj)
    LISTE_CONFIGS_LIEUX = configs_temp

# ---Initialisation des données au démarrage de l'application---
charger_donnees_clients()
charger_configurations_lieux() # Charger en premier
charger_donnees_evenements()   # Puis charger les événements qui dépendent des configs lieux

# --- Fonction globale pour mettre à jour les détails de l'événement et le combobox des catégories ---
def maj_details_et_categories_evenement(
    event_tk,
    list_evene_widget: tk.Listbox, 
    lbl_details_widget: ttk.Label, 
    combo_categories_widget: ttk.Combobox, 
    categories_obj_list_pour_event_ref: list[CategorieSiege] # Référence à la liste qui stockera les objets catégorie
):
    """Met à jour le label des détails de l'événement et peuple le combobox des catégories."""
    global evenements_objects # Accès à la liste globale des événements

    selection = list_evene_widget.curselection()
    if selection:
        index = selection[0]
        if 0 <= index < len(evenements_objects):
            evenement_obj = evenements_objects[index]
            lbl_details_widget.config(text=evenement_obj.afficher_details())
            
            categories_obj_list_pour_event_ref.clear()
            combo_categories_widget['values'] = [] # Vider les valeurs affichées du combobox
            
            if evenement_obj.config_lieu_ref and evenement_obj.config_lieu_ref.categories:
                valeurs_combobox = []
                for cat_config_statique in evenement_obj.config_lieu_ref.categories:
                    # Calculer les sièges disponibles pour cette catégorie DANS CET EVENEMENT
                    sieges_dispo_cat_count = 0
                    for siege_cfg in cat_config_statique.sieges:
                        if evenement_obj.sieges_etat.get(siege_cfg.idSiege, False): # Vérifie l'état dans sieges_etat
                            sieges_dispo_cat_count += 1
                    
                    valeurs_combobox.append(
                        f"{cat_config_statique.nomCategorie} ({cat_config_statique.prix}€) - {sieges_dispo_cat_count} disp."
                    )
                    # Stocker la référence à l'objet de configuration statique de la catégorie
                    categories_obj_list_pour_event_ref.append(cat_config_statique) 
                
                combo_categories_widget['values'] = valeurs_combobox
                if valeurs_combobox:
                    combo_categories_widget.current(0)
                    combo_categories_widget.config(state='readonly')
                else:
                    combo_categories_widget.set("Aucune catégorie disponible")
                    combo_categories_widget.config(state='disabled')
            else:
                combo_categories_widget.set("Catégories non définies")
                combo_categories_widget.config(state='disabled')
        else:
            lbl_details_widget.config(text="Erreur: Index d'événement invalide.")
            combo_categories_widget.set("")
            combo_categories_widget.config(state='disabled')
            categories_obj_list_pour_event_ref.clear()
    else:
        lbl_details_widget.config(text="Sélectionnez un événement pour voir les détails.")
        combo_categories_widget.set("")
        combo_categories_widget.config(state='disabled')
        categories_obj_list_pour_event_ref.clear()


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

# ---Fonction pour obtenir le prochain ID d'abonnement Newsletter unique---
def obtenir_prochain_id_abonnement_newsletter() -> int:
    """Génère un ID unique pour un nouvel abonnement newsletter."""
    global _prochain_id_abonnement_newsletter
    id_abo = _prochain_id_abonnement_newsletter
    _prochain_id_abonnement_newsletter += 1
    return id_abo

# ---Fonction pour obtenir le prochain ID de paiement unique---
def obtenir_prochain_id_paiement() -> int:
    """Génère un ID unique pour un nouveau paiement."""
    global _prochain_id_paiement
    id_paiement = _prochain_id_paiement
    _prochain_id_paiement += 1
    return id_paiement

# --- Fonctions pour les actions de l'utilisateur ---
def effectuer_reservation_gui(
    list_evene_widget, 
    combo_categories_sieges_widget,
    categories_runtime_list: list[CategorieSiege], # Liste des objets CategorieConfigLieu (runtime)
    entry_nb_billets_widget, 
    listbox_mes_billets_widget, 
    lbl_details_evenement_widget
):
    """Gère la logique de réservation de billets à partir de l'interface graphique,
       en utilisant la catégorie de siège sélectionnée."""
    global utilisateur_actif, evenements_objects, reservations_objects

    selection_event = list_evene_widget.curselection()
    if not selection_event:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un événement.")
        return
    
    index_evenement_selectionne = selection_event[0]
    evenement_selectionne = evenements_objects[index_evenement_selectionne]

    # Récupérer la catégorie sélectionnée
    index_categorie_selectionnee = combo_categories_sieges_widget.current()
    if index_categorie_selectionnee < 0 : # Aucune catégorie sélectionnée
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une catégorie de siège.")
        return
    
    # S'assurer que la liste categories_runtime_list (qui contient maintenant les refs aux configs statiques)
    # est bien celle de l'événement courant. maj_details_et_categories_evenement la peuple.
    if not categories_runtime_list or index_categorie_selectionnee >= len(categories_runtime_list):
        messagebox.showerror("Erreur Catégorie", "Erreur interne : la catégorie sélectionnée n'est pas valide ou la liste des catégories n'est pas à jour.")
        return
        
    categorie_config_selectionnee = categories_runtime_list[index_categorie_selectionnee]

    try:
        nb_billets_str = entry_nb_billets_widget.get()
        nb_billets = int(nb_billets_str)
        if nb_billets <= 0:
            messagebox.showerror("Nombre invalide", "Le nombre de billets doit être positif.")
            return
    except ValueError:
        messagebox.showerror("Entrée invalide", "Veuillez entrer un nombre valide pour les billets.")
        return

    # Vérifier la disponibilité dans la catégorie sélectionnée en utilisant sieges_etat de l'événement
    sieges_config_disponibles_categorie = []
    for siege_cfg in categorie_config_selectionnee.sieges:
        if evenement_selectionne.sieges_etat.get(siege_cfg.idSiege, False):
            sieges_config_disponibles_categorie.append(siege_cfg)

    if len(sieges_config_disponibles_categorie) < nb_billets:
        messagebox.showinfo("Places insuffisantes",
                            f"Il ne reste que {len(sieges_config_disponibles_categorie)} place(s) disponible(s) "
                            f"dans la catégorie '{categorie_config_selectionnee.nomCategorie}' pour {evenement_selectionne.nom}.")
        return
        
    # Sélectionner les sièges (configs statiques) spécifiques à réserver dans cette catégorie
    sieges_configs_a_reserver = sieges_config_disponibles_categorie[:nb_billets]

    # Création de la réservation
    id_nouvelle_reservation = obtenir_prochain_id_reservation()
    nouvelle_reservation = Reservation(idReservation=id_nouvelle_reservation,
                                       idClient=utilisateur_actif.idClient,
                                       dateReservation=datetime.datetime.now())
    
    billets_ajoutes_avec_succes = 0
    # sieges_configs_a_reserver contient les objets Siege de la config statique
    for siege_config_pour_billet in sieges_configs_a_reserver: 
        if nouvelle_reservation.ajouter_billet_pour_siege(evenement=evenement_selectionne,
                                                          siege_config=siege_config_pour_billet, 
                                                          categorie_config=categorie_config_selectionnee):
            billets_ajoutes_avec_succes += 1

    # Vérifier si tous les billets ont été ajoutés avec succès
    if billets_ajoutes_avec_succes == nb_billets:
        utilisateur_actif.effectuerReservation(nouvelle_reservation)
        reservations_objects.append(nouvelle_reservation)

        # Création et traitement du paiement
        id_paiement = obtenir_prochain_id_paiement()
        nouveau_paiement = Paiement(idPaiement=id_paiement,
                                    idReservation=nouvelle_reservation.idReservation,
                                    montant=nouvelle_reservation.montantTotal)
        nouveau_paiement.effectuerPaiement() # Supposons que le paiement est immédiat
        nouvelle_reservation.paiement = nouveau_paiement # Lier le paiement à la réservation

        message_succes = (f"{nb_billets} billet(s) réservé(s) pour {evenement_selectionne.nom}.\n"
                          f"ID de la réservation: {nouvelle_reservation.idReservation}\n"
                          f"Montant total: {nouvelle_reservation.montantTotal} €\n"
                          f"Statut du paiement: {nouveau_paiement.statutPaiement}")
        messagebox.showinfo("Réservation réussie", message_succes)
        
        # Mettre à jour l'affichage des détails de l'événement et le combobox des catégories
        # si l'événement concerné est celui actuellement sélectionné.
        current_selection_indices = list_evene_widget.curselection()
        if current_selection_indices and current_selection_indices[0] == index_evenement_selectionne:
            # Créer un objet event factice pour appeler maj_details_et_categories_evenement,
            # car cette fonction attend un event Tkinter comme argument.
            # On passe None pour event_tk car la fonction n'utilise pas cet argument quand elle est appelée ainsi.
            maj_details_et_categories_evenement(
                None, # event_tk_dummy
                list_evene_widget,
                lbl_details_evenement_widget,
                combo_categories_sieges_widget,
                categories_runtime_list # C'est la liste des objets catégorie pour l'event courant
            )

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
                evenement_associe = next((evt for evt in evenements_objects if evt.id_event == billet.id_event), None)
                nom_evenement = "Événement inconnu"
                if evenement_associe:
                    nom_evenement = evenement_associe.nom
                
                details_billet_str = billet.afficher_details_billet(nom_evenement=nom_evenement)
                # Ajouter le statut du paiement
                if reservation.paiement:
                    details_billet_str += f" - Paiement: {reservation.paiement.statutPaiement}"

                # Ajouter le billet à la listbox    
                listbox_widget.insert(tk.END, details_billet_str)

# ---Fonction pour annuler une réservation/billet à partir de l'interface graphique---
def annuler_billet_reservation_gui(
    entry_billet_id_annul_widget, 
    list_evene_widget, 
    listbox_mes_billets_widget, 
    lbl_details_evenement_widget,
    combo_categories_sieges_widget,
    categories_runtime_list_ref: list[CategorieSiege]
):
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
    
    # La méthode annulerReservation de la classe Reservation s'occupe de libérer les sièges
    # et de vider la liste des billets de la réservation.
    # Elle a besoin de la liste globale des événements pour trouver l'objet Evenement à mettre à jour.
    message_annulation = f"Réservation {id_reservation_a_annuler} annulée."
    
    # Gérer le remboursement si un paiement a été effectué
    if reservation_a_annuler.paiement and reservation_a_annuler.paiement.statutPaiement == "Payé":
        if reservation_a_annuler.paiement.rembourserPaiement():
            message_annulation += f"\nPaiement remboursé (Statut: {reservation_a_annuler.paiement.statutPaiement})."
        else:
            message_annulation += f"\nÉchec du remboursement du paiement (Statut: {reservation_a_annuler.paiement.statutPaiement})."
    elif reservation_a_annuler.paiement:
        message_annulation += f"\nStatut du paiement: {reservation_a_annuler.paiement.statutPaiement} (aucun remboursement nécessaire)."


    if reservation_a_annuler.annulerReservation(evenements_data=evenements_objects):
        # Retirer la réservation de la liste des réservations de l'utilisateur
        if reservation_a_annuler in utilisateur_actif.reservations:
             utilisateur_actif.reservations.remove(reservation_a_annuler)
        # Retirer également de la liste globale pour éviter qu'elle ne soit rechargée
        if reservation_a_annuler in reservations_objects:
            reservations_objects.remove(reservation_a_annuler)
        
        messagebox.showinfo("Annulation Réussie", message_annulation)

        # Mettre à jour l'affichage des détails de l'événement et le combobox des catégories
        # si l'événement concerné est celui actuellement sélectionné.
        evenement_concerne_obj = next((evt for evt in evenements_objects if evt.id_event == id_event_concerne), None)
        if evenement_concerne_obj: # S'assurer que l'objet événement a été trouvé
            current_selection_indices = list_evene_widget.curselection()
            if current_selection_indices:
                index_evt_selectionne_dans_liste = current_selection_indices[0]
                # Vérifier si l'événement annulé est celui actuellement sélectionné dans la liste
                if index_evt_selectionne_dans_liste < len(evenements_objects) and \
                   evenements_objects[index_evt_selectionne_dans_liste].id_event == id_event_concerne:
                    
                    maj_details_et_categories_evenement(
                        None, # event_tk_dummy
                        list_evene_widget,
                        lbl_details_evenement_widget,
                        combo_categories_sieges_widget,
                        categories_runtime_list_ref
                    )

        # Mettre à jour la liste "Mes Billets"
        actualiser_liste_mes_billets(listbox_mes_billets_widget)
        entry_billet_id_annul_widget.delete(0, tk.END) # Vider le champ après annulation
    
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
            
            # Récupérer les réservations existantes pour cet utilisateur depuis la liste globale
            reservations_de_l_utilisateur = []
            if hasattr(utilisateur_actif, 'idClient'): # Vérifier que utilisateur_actif est bien un Client
                for res in reservations_objects: # reservations_objects est la liste globale
                    if res.idClient == utilisateur_actif.idClient:
                        reservations_de_l_utilisateur.append(res)
            
            # Assigner les réservations trouvées (ou une liste vide si aucune)
            if hasattr(utilisateur_actif, 'reservations'): # L'attribut doit exister (défini dans Client.__init__)
                utilisateur_actif.reservations = reservations_de_l_utilisateur 
            
            # Initialiser l'état de la newsletter pour l'utilisateur
            if not hasattr(utilisateur_actif, 'est_abonne_newsletter'):
                utilisateur_actif.est_abonne_newsletter = False
            if not hasattr(utilisateur_actif, 'newsletter_abonnement'):
                utilisateur_actif.newsletter_abonnement = None
            
            # Tentative de retrouver un objet Newsletter existant pour cet utilisateur s'il se reconnecte
            newsletter_existante = next((n for n in abonnements_newsletter_objects if n.emailClient == utilisateur_actif.email), None)
            if newsletter_existante:
                utilisateur_actif.newsletter_abonnement = newsletter_existante
                utilisateur_actif.est_abonne_newsletter = newsletter_existante.estActif

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
    fenetre_principale.geometry("900x800")

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
        afficher_fenetre_login()
    ttk.Button(user_frame, text="Changer d'Utilisateur", command=detruire_fenetre).pack(side=tk.RIGHT)

    # ---Boutons pour la Newsletter---
    newsletter_frame = ttk.Frame(user_frame)
    newsletter_frame.pack(side=tk.RIGHT, padx=10)

    btn_abonner_newsletter = ttk.Button(newsletter_frame, text="S'abonner Newsletter")
    btn_desabonner_newsletter = ttk.Button(newsletter_frame, text="Se désabonner")

    def maj_etat_boutons_newsletter():
        """Met à jour l'état (activé/désactivé) des boutons de newsletter."""
        if utilisateur_actif and utilisateur_actif.est_abonne_newsletter:
            btn_abonner_newsletter.config(state=tk.DISABLED)
            btn_desabonner_newsletter.config(state=tk.NORMAL)
        else:
            btn_abonner_newsletter.config(state=tk.NORMAL)
            btn_desabonner_newsletter.config(state=tk.DISABLED)

    def abonner_newsletter_gui():
        global utilisateur_actif, abonnements_newsletter_objects
        if utilisateur_actif and not utilisateur_actif.est_abonne_newsletter:
            id_abo = obtenir_prochain_id_abonnement_newsletter()
            # Vérifier si un objet newsletter existe déjà pour cet email pour le réactiver
            newsletter_existante = next((n for n in abonnements_newsletter_objects if n.emailClient == utilisateur_actif.email), None)
            if newsletter_existante:
                utilisateur_actif.gererAbonnementNewsletter(s_abonner=True, newsletter_obj=newsletter_existante)
            else:
                nouvel_abonnement = Newsletter(idAbonnement=id_abo, emailClient=utilisateur_actif.email)
                utilisateur_actif.gererAbonnementNewsletter(s_abonner=True, newsletter_obj=nouvel_abonnement)
                abonnements_newsletter_objects.append(nouvel_abonnement)
            
            messagebox.showinfo("Newsletter", f"{utilisateur_actif.nom}, vous êtes maintenant abonné à la newsletter.")
            maj_etat_boutons_newsletter()

    def desabonner_newsletter_gui():
        global utilisateur_actif
        if utilisateur_actif and utilisateur_actif.est_abonne_newsletter:
            utilisateur_actif.gererAbonnementNewsletter(s_abonner=False) # L'objet newsletter est déjà sur le client
            messagebox.showinfo("Newsletter", f"{utilisateur_actif.nom}, vous êtes maintenant désabonné de la newsletter.")
            maj_etat_boutons_newsletter()

    btn_abonner_newsletter.config(command=abonner_newsletter_gui)
    btn_desabonner_newsletter.config(command=desabonner_newsletter_gui)
    
    btn_abonner_newsletter.pack(side=tk.LEFT)
    btn_desabonner_newsletter.pack(side=tk.LEFT, padx=5)
    maj_etat_boutons_newsletter() # Appel initial pour définir l'état correct des boutons

    # ---Section Événements---
    frame_evene = ttk.LabelFrame(frame_princip, text="Événements Disponibles", padding="10")
    frame_evene.pack(expand=True, fill=tk.BOTH, pady=5)

    list_evene = tk.Listbox(frame_evene, height=10, exportselection=False, font=('Consolas', 10))
    list_evene.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
    
    # Ajout d'une scrollbar verticale pour la Listbox des événements
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
    for evenement_obj in evenements_objects: # evenements_objects est global
        list_evene.insert(tk.END, f"{evenement_obj.date} - {evenement_obj.nom}")

    # --- Section Actions (Réservation / Annulation) ---
    frame_action = ttk.LabelFrame(frame_princip, text="Actions", padding="10")
    frame_action.pack(fill=tk.X, pady=5)

    # ---Réservation---
    frame_reserv = ttk.Frame(frame_action)
    frame_reserv.pack(fill=tk.X, pady=5)

    ttk.Label(frame_reserv, text="Catégorie:").pack(side=tk.LEFT, padx=(5,0))
    combo_categories_sieges = ttk.Combobox(frame_reserv, width=35, state="disabled") 
    combo_categories_sieges.pack(side=tk.LEFT, padx=5)
    
    # Cette liste sera une référence à la liste définie dans afficher_fenetre_principale
    # et sera modifiée par maj_details_et_categories_evenement (qui sera globale)
    # Elle doit être initialisée ici pour que le lambda de btn_reserver puisse la capturer.
    categories_objets_pour_event_selectionne_ref: list[CategorieSiege] = [] 

    # Liaison de la Listbox des événements à la fonction globale de mise à jour
    # Le lambda est utilisé pour passer les arguments nécessaires à la fonction globale.
    list_evene.bind('<<ListboxSelect>>', 
                    lambda event_tk: maj_details_et_categories_evenement(
                        event_tk,
                        list_evene,
                        lbl_details_evenement,
                        combo_categories_sieges,
                        categories_objets_pour_event_selectionne_ref
                    )
    )

    ttk.Label(frame_reserv, text="Nb Billets:").pack(side=tk.LEFT, padx=(10,0))
    entry_nb_billets = ttk.Entry(frame_reserv, width=3)
    entry_nb_billets.insert(0, "1") # Valeur par défaut
    entry_nb_billets.pack(side=tk.LEFT, padx=5)
    
    # La commande du bouton Réserver devra maintenant aussi passer le combobox ou sa sélection
    btn_reserver = ttk.Button(frame_reserv, text="Réserver Billets", 
               command=lambda: effectuer_reservation_gui(
                   list_evene,
                   combo_categories_sieges,
                   categories_objets_pour_event_selectionne_ref,
                   entry_nb_billets,
                   listbox_mes_billets,
                   lbl_details_evenement
                )
              )
    btn_reserver.pack(side=tk.LEFT, padx=5)

    # ---Annulation---
    frame_annula = ttk.Frame(frame_action)
    frame_annula.pack(fill=tk.X, pady=5)
    ttk.Label(frame_annula, text="ID Réservation à Annuler:").pack(side=tk.LEFT, padx=5)
    entry_billet_id_annul = ttk.Entry(frame_annula, width=5)
    entry_billet_id_annul.pack(side=tk.LEFT, padx=5)
    # Connection de la fonction d'annulation au bouton
    btn_annuler = ttk.Button(frame_annula, text="Annuler Réservation",
               command=lambda: annuler_billet_reservation_gui(
                   entry_billet_id_annul, 
                   list_evene, 
                   listbox_mes_billets, 
                   lbl_details_evenement,
                   combo_categories_sieges,
                   categories_objets_pour_event_selectionne_ref
                )
            )
    btn_annuler.pack(side=tk.LEFT, padx=5)

    # ---Section Mes Billets---
    frame_billet = ttk.LabelFrame(frame_princip, text="Mes Billets (Réservations Actives)", padding="10")
    frame_billet.pack(fill=tk.X, pady=5)

    listbox_mes_billets = tk.Listbox(frame_billet, height=5, font=('Consolas', 10))
    listbox_mes_billets.pack(fill=tk.X, expand=True, padx=(0,10), side=tk.LEFT) # side=tk.LEFT pour permettre au bouton d'être à côté
    
    scrollbar_mes_billets = ttk.Scrollbar(frame_billet, orient=tk.VERTICAL, command=listbox_mes_billets.yview)
    scrollbar_mes_billets.pack(side=tk.LEFT, fill=tk.Y) # Scrollbar à gauche de la listbox
    listbox_mes_billets.config(yscrollcommand=scrollbar_mes_billets.set)

    # Appel initial pour charger les billets si l'utilisateur en a déjà
    actualiser_liste_mes_billets(listbox_mes_billets)
    
    fenetre_principale.mainloop()