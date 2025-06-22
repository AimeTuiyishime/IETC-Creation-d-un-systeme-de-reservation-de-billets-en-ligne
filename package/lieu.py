class Lieu:
    def __init__(self, idLieu, nom, adresse, capacite):
        self.idLieu = idLieu
        self.nom = nom
        self.adresse = adresse
        self.capacite = capacite
        self.nombrePlacesDisponiblesInitial = capacite
        self.nombrePlacesRestantes = capacite

    def reserver_places(self, quantite):
        """Réserve un certain nombre de places si disponible."""
        if quantite <= self.nombrePlacesRestantes:
            self.nombrePlacesRestantes -= quantite
            return True
        return False

    def annuler_reservation(self, quantite):
        """Annule une réservation et remet les places disponibles."""
        if self.nombrePlacesRestantes + quantite <= self.capacite:
            self.nombrePlacesRestantes += quantite
            return True
        return False

    def __str__(self):
        return (f"Lieu {self.nom} (ID: {self.idLieu})\n"
                f"Adresse: {self.adresse}\n"
                f"Capacité totale: {self.capacite}\n"
                f"Places restantes: {self.nombrePlacesRestantes}")
