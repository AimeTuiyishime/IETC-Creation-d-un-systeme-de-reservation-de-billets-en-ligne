from datetime import datetime

class Paiement:
    def __init__(self, idPaiement, idReservation, montant):
        self.idPaiement = idPaiement
        self.idReservation = idReservation
        self.montant = montant
        self.statutPaiement = "En attente"
        self.datePaiement = None

    def effectuerPaiement(self):
        if self.statutPaiement != "Payé":
            self.statutPaiement = "Payé"
            self.datePaiement = datetime.now()
            return True
        return False

    def rembourserPaiement(self):
        if self.statutPaiement == "Payé":
            self.statutPaiement = "Remboursé"
            return True
        return False

    def __str__(self):
        return (f"Paiement ID: {self.idPaiement}, Réservation: {self.idReservation}, "
                f"Montant: {self.montant:.2f}€, Statut: {self.statutPaiement}, "
                f"Date: {self.datePaiement if self.datePaiement else 'Non effectué'}")
