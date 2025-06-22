from datetime import datetime

# ===============================
# Classe : Lieu
# ===============================

class Lieu:
    def __init__(self, idLieu, nom, adresse, capacite):
        self.idLieu = idLieu
        self.nom = nom
        self.adresse = adresse
        self.capacite = capacite
        self.nombrePlacesDisponiblesInitial = capacite
        self.nombrePlacesRestantes = capacite

    def reserver_places(self, quantite):
        """
        Réserve un certain nombre de places si elles sont disponibles.

        Args:
            quantite (int): Le nombre de places à réserver.

        Returns:
            bool: True si la réservation a été effectuée, False sinon.
        """
        if quantite <= self.nombrePlacesRestantes:
            self.nombrePlacesRestantes -= quantite
            return True
        return False

    def annuler_reservation(self, quantite):
        """
        Annule une réservation et remet les places disponibles.

        Args:
            quantite (int): Le nombre de places à annuler.

        Returns:
            bool: True si l’annulation est possible et effectuée, False sinon.
        """
        if self.nombrePlacesRestantes + quantite <= self.capacite:
            self.nombrePlacesRestantes += quantite
            return True
        return False

    def __str__(self):
        return (f"Lieu {self.nom} (ID: {self.idLieu})\n"
                f"Adresse: {self.adresse}\n"
                f"Capacité totale: {self.capacite}\n"
                f"Places restantes: {self.nombrePlacesRestantes}")
        
# ===============================
# Classe : Paiement
# ===============================

class Paiement:
    def __init__(self, idPaiement, idReservation, montant):
        self.idPaiement = idPaiement
        self.idReservation = idReservation
        self.montant = montant
        self.statutPaiement = "En attente"
        self.datePaiement = None

    def effectuerPaiement(self):
        """
        Effectue le paiement si le statut est encore 'En attente'.

        Returns:
            bool: True si le paiement a été effectué, False sinon.
        """
        if self.statutPaiement != "Payé":
            self.statutPaiement = "Payé"
            self.datePaiement = datetime.now()
            return True
        return False

    def rembourserPaiement(self):
        """
        Rembourse le paiement si celui-ci a été effectué.

        Returns:
            bool: True si le remboursement a eu lieu, False sinon.
        """
        if self.statutPaiement == "Payé":
            self.statutPaiement = "Remboursé"
            return True
        return False

    def __str__(self):
        return (f"Paiement ID: {self.idPaiement}, Réservation: {self.idReservation}, "
                f"Montant: {self.montant:.2f}€, Statut: {self.statutPaiement}, "
                f"Date: {self.datePaiement if self.datePaiement else 'Non effectué'}")

# ===============================
# Classe : Siege
# ===============================

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
        """
         Réserve le siège si disponible.

        Returns:
            bool: True si réservation réussie, False sinon. 
        """
        if self.estDisponible():
            self.disponible = False
            return True
        return False
    
    def liberer(self):
        self.disponible = True
        
    def __str__(self):
        etat = "Disponible" if self.estDisponible() else "Réservé"
        return f"Siège {self.identificationSiege} ({etat}) - Catégorie {self.idCategorie}, Lieu {self.idLieu}"

# ===============================
# Classe : CategorieDeSiege
# ===============================

class CategorieDeSiege:
    def __init__(self, idCategorie, nomCategorie, prix):
        self.idCategorie = idCategorie
        self.nomCategorie = nomCategorie
        self.prix = prix
    
    def __str__(self):
        return f"[{self.idCategorie}] {self.nomCategorie} - {self.prix} "

# ===============================
# Classe : Newsletter
# ===============================

class Newsletter:
    def __init__(self, idAbonnement, emailClient, estActif=False):
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
