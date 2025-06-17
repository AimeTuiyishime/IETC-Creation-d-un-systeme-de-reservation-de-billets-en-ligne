import datetime
from typing import List

class Client:
    """
    Représente un client du service de réservation.
    """
    def __init__(self, idClient: int, nom: str, email: str, mdp: str):
        self.idClient = idClient
        self.nom = nom
        self.email = email
        self.mdp = mdp
        # self.reservations = Reservation
        # self.abonnements: Newsletter

    def effectuerReservation(self):
        """ 
        Permet au client de faire une réservation.
        """
        pass

    def annulerReservation(self):
        """
        Demande l'annulation d'une réservation spécifique.
        """
        pass
    
    def gererAbonnementNewsletter(self):
        """
        Permet de s'abonner ou de se désabonner d'une newsletter.
        """
        pass

class Reservation:
    """
    Représente une réservation effectuée par un client pour un ou plusieurs billets.
    """
    def __init__(self, idReservation: int, idClient: int, dateReservation: datetime):
        self.idReservation = idReservation
        self.idClient = idClient
        self.dateReservation = dateReservation
        self.montantTotal = 0.0
        # self.billets = Billet 
        # self.paiements = Paiement

    def ajouterBillet(self):
        """
        Ajoute un billet à la réservation et met à jour le montant total.
        """
        pass

    def confirmerReservation(self):
        """
        Confirme la réservation, généralement après le paiement.
        """
        print(f"Réservation {self.idReservation} confirmée.")
        pass

    def annulerReservation(self):
        """
        Annule la réservation et les billets associés.
        """
        print(f"Réservation {self.idReservation} annulée.")
        pass
