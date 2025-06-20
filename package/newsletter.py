class Newsletter:
    def __init__(self, idAbonnement, emailClient, estActif=True):
        self.idAbonnement = idAbonnement
        self.emailClient = emailClient
        self.estActif = estActif
        
    def confirmerAbonnement(self):
        self.estActif = True
        
    def envoyerNewsLetter(self, message):
        if self.estActif:
            print(f"Envoi de la newsletter à {self.emailClient}: \n {message}")
            return True
        else:
            print(f"Abonnement inactif pour {self.emailClient}.")
            return False
    
    def __str__(self):
        statut = "Actif" if self.estActif else "Inactif"
        return f"Newsletter [{self.idAbonnement}] - {self.emailClient} ({statut})"