import datetime
from typing import List

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

    def effectuerReservation(self, reservation: 'Reservation'):
        """ 
        Ajoute une réservation à la liste des réservations du client.
        """
        self.reservations.append(reservation)
        # print(f"Réservation {reservation.idReservation} ajoutée pour le client {self.nom}.")

    # La méthode annulerReservation a été retirée de Client.
    # La logique d'annulation est gérée dans GUI.py.
    def gererAbonnementNewsletter(self, bool = True):
        """
        Permet de s'abonner ou de se désabonner d'une newsletter spécifique.
        """
        pass

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

    def ajouterBillet(self, evenement: 'Evenement', quantite: int = 1) -> bool:
        """
        Ajoute un ou plusieurs billets pour un événement donné à la réservation.
        Met à jour le montant total et gère la réservation des places de l'événement.
        Retourne True si l'ajout est réussi, False sinon.
        """
        if not evenement.verifier_disponibilite_places(quantite):
            # print(f"Pas assez de places disponibles pour {evenement.nom} pour {quantite} billet(s).")
            return False

        if evenement.reserver_places(quantite):
            for _ in range(quantite):
                id_billet = Reservation._prochain_id_billet
                Reservation._prochain_id_billet += 1
                
                nouveau_billet = Billet(id_billet=id_billet, 
                                        id_event=evenement.id_event, 
                                        id_reservation=self.idReservation, 
                                        prix=evenement.prix)
                self.billets.append(nouveau_billet)
                self.montantTotal += nouveau_billet.prix
            # print(f"{quantite} billet(s) pour {evenement.nom} ajouté(s) à la réservation {self.idReservation}.")
            return True
        # else:
            # print(f"Échec de la réservation des places pour {evenement.nom}.")
        return False

    def confirmerReservation(self):
        """
        Confirme la réservation, généralement après le paiement.
        (Peut être étendu avec la logique de paiement)
        """
        # print(f"Réservation {self.idReservation} confirmée.")
        pass

    def annulerReservation(self, evenements_data: List['Evenement']) -> bool:
        """
        Annule la réservation et les billets associés.
        Remet les places annulées à disposition pour l'événement concerné.
        """
        if not self.billets:
            # print(f"La réservation {self.idReservation} ne contient aucun billet à annuler.")
            return False

        id_event_concerne = self.billets[0].id_event
        # la fonction next() permet de trouver l'événement correspondant à l'ID
        # si l'événement n'est pas trouvé, elle retourne None
        evenement_concerne = next((i for i in evenements_data if i.id_event == id_event_concerne), None)

        if evenement_concerne:
            nombre_billets_annules = len(self.billets)
            evenement_concerne.annuler_places_reservees(nombre_billets_annules)
            # print(f"{nombre_billets_annules} places remises à disposition pour l'événement {evenement_concerne.nom}.")
        # else:
            # print(f"Erreur: Événement ID {id_event_concerne} non trouvé pour l'annulation des places.")

        self.billets.clear()
        self.montantTotal = 0.0
        # print(f"Réservation {self.idReservation} annulée. Tous les billets ont été supprimés.")
        return True

# ---Classe Evenement pour la gestion des événements proposés à la réservation---
class Evenement:
    """
    Représente un événement proposé à la réservation.
    """
    def __init__(self, id_event: int, nom: str, date: str, lieu: str, description: str, places: int, prix: float):
        self.id_event = id_event
        self.nom = nom
        self.date = date 
        self.lieu = lieu
        self.description = description
        self.places_disponibles = places
        self.prix = prix

    def afficher_details(self) -> str:
        """
        Retourne une chaîne formatée avec les détails de l'événement.
        """
        return (f"Nom: {self.nom}\nDate: {self.date}\nLieu: {self.lieu}\n"
                f"Description: {self.description}\nPrix: {self.prix} €\n"
                f"Places disponibles: {self.places_disponibles}")

    def verifier_disponibilite_places(self, nombre_places_demandees: int) -> bool:
        """
        Vérifie s'il y a suffisamment de places disponibles.
        """
        return self.places_disponibles >= nombre_places_demandees

    def reserver_places(self, nombre_places_reservees: int) -> bool:
        """
        Réserve un certain nombre de places si disponibles.
        """
        if self.verifier_disponibilite_places(nombre_places_reservees):
            self.places_disponibles -= nombre_places_reservees
            return True
        return False

    def annuler_places_reservees(self, nombre_places_annulees: int):
        """
        Augmente le nombre de places disponibles suite à une annulation.
        """
        self.places_disponibles += nombre_places_annulees

# ---Classe Billet pour la gestion des billets associés aux réservations---
class Billet:
    """
    Représente un billet pour un événement, associé à une réservation.
    """
    def __init__(self, id_billet: int, id_event: int, id_reservation: int, prix: float):
        self.id_billet = id_billet
        self.id_event = id_event
        self.id_reservation = id_reservation
        self.prix = prix

    def afficher_details_billet(self, nom_evenement: str) -> str:
        """
        Retourne une chaîne formatée avec les détails du billet.
        """
        return f"Billet ID: {self.id_billet} ({nom_evenement}) - Résa. ID: {self.id_reservation} - Prix: {self.prix} €"
