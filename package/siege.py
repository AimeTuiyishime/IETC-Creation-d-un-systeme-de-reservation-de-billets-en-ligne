class Siege: 
    def __init__(self, idSiege, idLieu, idCategorie, identificationSiege, disponible=True):
        self.idSiege = idSiege
        self.idLieu = idLieu
        self.idCategorie = idCategorie
        self.identificationSiege = identificationSiege
        self.disponible = disponible
        
    def estDisponible(self):
        return self.disponible
    
    def reserver(self):
        if self.estDisponible():
            self.disponible = False
            return True
        return False
    
    def liberer(self):
        self.disponible = True
        
    def __str__(self):
        etat = "Disponible" if self.estDisponible() else "Réservé"
        return f"Siège {self.identificationSiege} ({etat}) - Catégorie {self.idCategorie}, Lieu {self.idLieu}"