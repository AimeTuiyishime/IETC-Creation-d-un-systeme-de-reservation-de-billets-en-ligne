import datetime
from typing import List, Dict
from package.package_class_additionnel import Newsletter, Paiement, Lieu, Siege, CategorieSiege

# ---Classe Client pour la gestion des clients dans le système de réservation---
class Client:
    """
    Représente un client du service de réservation.
    """
    def __init__(self, idClient: int, nom: str, email: str, mdp: str):
        self.idClient = idClient
        self.nom = nom
        self.email = email
        self.mdp = mdp
        self.reservations: List['Reservation'] = []
        self.est_abonne_newsletter: bool = False
        self.newsletter_abonnement: 'Newsletter' | None = None

    def effectuerReservation(self, reservation: 'Reservation'):
        """ 
        Ajoute une réservation à la liste des réservations du client.
        """
        self.reservations.append(reservation)

    def gererAbonnementNewsletter(self, s_abonner: bool, newsletter_obj: 'Newsletter' = None):
        """
        Permet de s'abonner ou de se désabonner d'une newsletter spécifique.
        Met à jour l'attribut est_abonne_newsletter et l'objet Newsletter associé.
        """
        self.est_abonne_newsletter = s_abonner
        # Si on s'abonne, on crée ou met à jour l'objet Newsletter
        if newsletter_obj:
            self.newsletter_abonnement = newsletter_obj
            if s_abonner:
                self.newsletter_abonnement.confirmerAbonnement()
            else:
                self.newsletter_abonnement.estActif = False
        # Si on se désabonne, on met à jour l'état de l'abonnement dans l'objet Newsletter      
        elif not s_abonner and hasattr(self, 'newsletter_abonnement') and self.newsletter_abonnement:
            self.newsletter_abonnement.estActif = False

# ---Classe Reservation pour la gestion des réservations de billets---
class Reservation:
    """
    Représente une réservation effectuée par un client pour un ou plusieurs billets.
    """
    _prochain_id_billet = 1 

    def __init__(self, idReservation: int, idClient: int, dateReservation: datetime.datetime):
        self.idReservation = idReservation
        self.idClient = idClient
        self.dateReservation = dateReservation
        self.montantTotal: float = 0.0
        self.billets: List['Billet'] = []
        self.paiement: 'Paiement' | None = None # Ajout de l'attribut pour le paiement

    def ajouter_billet_pour_siege(self, evenement: 'Evenement', siege_config: 'Siege', categorie_config: 'CategorieSiege') -> bool:
        """
        Ajoute un billet pour un siège spécifique (objet Siege de la config statique) à la réservation.
        Met à jour le montant total et appelle la réservation du siège sur l'événement (qui mettra à jour sieges_etat).
        Retourne True si l'ajout est réussi, False sinon.
        """
        if not evenement.config_lieu_ref or not siege_config or not categorie_config:
            # return False # Si l'événement n'a pas de config de lieu ou si le siège/catégorie sont invalides
            return False

        # Tenter de réserver le siège via l'événement (qui gère la dispo dans son sieges_etat)
        if evenement.reserver_siege(siege_config.idSiege): # Passe l'ID du siège
            id_billet = Reservation._prochain_id_billet
            Reservation._prochain_id_billet += 1
            
            prix_billet = categorie_config.prix # Le prix vient de la config de la catégorie
            
            nouveau_billet = Billet(id_billet=id_billet,
                                    id_event=evenement.id_event,
                                    id_reservation=self.idReservation,
                                    id_siege_str=siege_config.idSiege, # ID du siège de la config
                                    identification_siege_str=siege_config.identificationSiege, # Nom du siège de la config
                                    nom_categorie_str=categorie_config.nomCategorie, # Nom de la catégorie de la config
                                    prix_float=prix_billet)
            self.billets.append(nouveau_billet)
            self.montantTotal += prix_billet
            
            # return True # Si le siège a été réservé avec succès et le billet ajouté
            return True
        
        # Si le siège n'était pas disponible ou la réservation a échoué
        return False

    def annulerReservation(self, evenements_data: List['Evenement']) -> bool:
        """
        Annule la réservation et les billets associés.
        Remet les sièges annulés à disposition pour l'événement concerné.
        """
        if not self.billets:
            # return False # Pas de billets à annuler
            return False

        # On suppose que tous les billets de cette réservation concernent le même événement
        # On prend le premier billet pour obtenir l'ID de l'événement
        id_event_initial = self.billets[0].id_event
        evenement_concerne = next((evt for evt in evenements_data if evt.id_event == id_event_initial), None)

        if not evenement_concerne or not evenement_concerne.config_lieu_ref: # Vérifier config_lieu_ref
            # return False # Si l'événement n'est pas trouvé ou n'a pas de config de lieu
            return False

        for billet_annule in self.billets:
            # billet_annule.id_siege contient l'ID du siège (str)
            # La méthode liberer_siege de Evenement prend maintenant cet ID directement.
            evenement_concerne.liberer_siege(billet_annule.id_siege)

        # On vide la liste des billets et remet le montant total à zéro
        self.billets.clear()
        self.montantTotal = 0.0
        # return True # Réservation annulée avec succès
        return True

# ---Classe Evenement pour la gestion des événements proposés à la réservation---
class Evenement:
    """
    Représente un événement proposé à la réservation.
    Utilise une configuration de lieu (`LieuConfig`) pour gérer les sièges et leurs disponibilités
    pour cette instance spécifique de l'événement.
    """
    def __init__(self, id_event: int, nom: str, date: str, lieu_nom_str: str, description: str):
        self.id_event = id_event
        self.nom = nom
        self.date = date
        self.lieu_nom_str = lieu_nom_str # Nom du lieu tel que lu depuis données_event.json
        self.description = description
        
        # Référence à la configuration statique du lieu (partagée entre événements au même lieu)
        self.config_lieu_ref: 'Lieu' | None = None
        # Dictionnaire pour l'état de disponibilité des sièges pour CET événement spécifique
        # Clé: idSiege (str), Valeur: bool (True si disponible, False si réservé)
        self.sieges_etat: Dict[str, bool] = {}

    def lier_config_lieu_et_initialiser_etat_sieges(self, lieu_config_original: 'Lieu'):
        """
        Lie la configuration statique du lieu à cet événement et initialise l'état
        de disponibilité de tous les sièges de ce lieu comme étant disponibles pour cet événement.
        """
        if not lieu_config_original:
            self.config_lieu_ref = None
            self.sieges_etat = {}
            return

        self.config_lieu_ref = lieu_config_original
        self.sieges_etat = {}
        for categorie in self.config_lieu_ref.categories:
            for siege in categorie.sieges:
                self.sieges_etat[siege.idSiege] = True # Initialement tous disponibles pour cet événement

    def afficher_details(self) -> str:
        """
        Retourne une chaîne formatée avec les détails de l'événement, y compris le lieu
        et les catégories de sièges avec leur disponibilité pour cet événement.
        """
        details_str = (f"Nom: {self.nom}\nDate: {self.date}\n"
                       f"Description: {self.description}\n")
        if self.config_lieu_ref:
            details_str += f"Lieu: {self.config_lieu_ref.nomLieu} ({self.config_lieu_ref.adresse})\n"
            details_str += "Catégories de sièges disponibles:\n"
            total_sieges_disponibles_evenement = 0
            for cat_config in self.config_lieu_ref.categories:
                # Compter les sièges disponibles pour cette catégorie DANS CET EVENEMENT
                sieges_dispo_cat_count = 0
                for siege_config in cat_config.sieges:
                    if self.sieges_etat.get(siege_config.idSiege, False): # True si dans dict et True
                        sieges_dispo_cat_count += 1
                
                total_sieges_disponibles_evenement += sieges_dispo_cat_count
                details_str += (f"  - {cat_config.nomCategorie}: {cat_config.prix} € "
                                f"({sieges_dispo_cat_count} siège(s) disponible(s))\n")
            details_str += f"Total sièges disponibles pour l'événement: {total_sieges_disponibles_evenement}\n"
        else:
            details_str += f"Lieu: {self.lieu_nom_str} (Configuration du lieu non chargée ou invalide)\n"
            details_str += "Détails des sièges non disponibles.\n"
        return details_str

    def verifier_disponibilite_places(self, quantite: int, id_categorie_config_lieu: str = None) -> bool:
        """
        Vérifie s'il y a suffisamment de sièges disponibles (pour cet événement),
        optionnellement pour une catégorie spécifique.
        """
        if not self.config_lieu_ref:
            # Si la config du lieu n'est pas liée, on ne peut pas vérifier la disponibilité
            return False
            
        if id_categorie_config_lieu:
            categorie_trouvee = next((cat for cat in self.config_lieu_ref.categories if cat.idCategorieConfigLieu == id_categorie_config_lieu), None)
            if not categorie_trouvee:
                # Si la catégorie n'est pas trouvée, on ne peut pas vérifier la disponibilité
                return False
            
            # Compter les sièges disponibles dans la catégorie trouvée
            sieges_dispo_dans_categorie_count = 0
            for siege_config in categorie_trouvee.sieges:
                if self.sieges_etat.get(siege_config.idSiege, False):
                    sieges_dispo_dans_categorie_count +=1
            return sieges_dispo_dans_categorie_count >= quantite
        # Si aucune catégorie n'est spécifiée, on vérifie dans toutes les catégories du lieu
        # On compte les sièges disponibles dans toutes les catégories de ce lieu pour cet événement
        else: 
            total_sieges_disponibles = 0
            for cat_config in self.config_lieu_ref.categories:
                for siege_config in cat_config.sieges:
                    if self.sieges_etat.get(siege_config.idSiege, False):
                        total_sieges_disponibles +=1
            return total_sieges_disponibles >= quantite

    def reserver_siege(self, siege_id_str: str) -> bool:
        """
        Tente de réserver un siège spécifique pour cet événement en mettant à jour son état.
        Retourne True si le siège était disponible et a été réservé, False sinon.
        """
        if not self.config_lieu_ref: # S'assurer que la config est liée
            return False
            
        if self.sieges_etat.get(siege_id_str, False): # Si le siège existe dans le dict et est True
            self.sieges_etat[siege_id_str] = False # Marquer comme réservé pour cet événement
            return True
        return False # Siège non trouvé dans sieges_etat ou déjà réservé

    def liberer_siege(self, siege_id_str: str):
        """
        Libère un siège spécifique pour cet événement en mettant à jour son état.
        """
        if not self.config_lieu_ref: # S'assurer que la config est liée
            return

        # On remet le siège à disposition dans l'état de l'événement
        if siege_id_str in self.sieges_etat:
            self.sieges_etat[siege_id_str] = True # Marquer comme disponible pour cet événement

# ---Classe Billet pour la gestion des billets associés aux réservations---
class Billet:
    """
    Représente un billet pour un événement, associé à une réservation et à un siège spécifique.
    """
    def __init__(self, id_billet: int, id_event: int, id_reservation: int, 
                 id_siege_str: str, identification_siege_str: str, nom_categorie_str: str, prix_float: float):
        self.id_billet = id_billet
        self.id_event = id_event 
        self.id_reservation = id_reservation
        self.id_siege: str = id_siege_str # ID unique du siège (ex: "SCA-A1")
        self.identification_siege: str = identification_siege_str # Nom lisible (ex: "A1")
        self.nom_categorie: str = nom_categorie_str
        self.prix: float = prix_float

    def afficher_details_billet(self, nom_evenement: str) -> str:
        """
        Retourne une chaîne formatée avec les détails du billet, incluant le siège.
        """
        return (f"Billet ID: {self.id_billet} ({nom_evenement})\n"
                f"  Résa. ID: {self.id_reservation}, Siège: {self.identification_siege} ({self.nom_categorie})\n"
                f"  Prix: {self.prix} €")
