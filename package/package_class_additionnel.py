from datetime import datetime
from typing import List
     
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
    """Représente un siège spécifique. Utilisé pour la configuration initiale
       et potentiellement pour l'état d'exécution (runtime)."""
    def __init__(self, idSiege: str, identificationSiege: str, disponible: bool = True):
        self.idSiege = idSiege # Identifiant unique du siège (ex: "SCA-A1")
        self.identificationSiege = identificationSiege # Nom lisible (ex: "A1")
        self.disponible = disponible # True si le siège est disponible, False sinon
        
    def estDisponible(self) -> bool:
        return self.disponible
    
    def reserver(self) -> bool:
        """
        Réserve le siège s'il est disponible.
        Returns:
            bool: True si la réservation a réussi, False sinon.
        """
        if self.estDisponible():
            self.disponible = False
            return True
        return False
    
    def liberer(self):
        """Libère le siège."""
        self.disponible = True
        
    def __str__(self) -> str:
        etat = "Disponible" if self.estDisponible() else "Réservé"
        return f"Siège {self.identificationSiege} (ID: {self.idSiege}, {etat})"

# ===============================
# Classe : CategorieSiege
# ===============================
class CategorieSiege:
    """Représente la configuration d'une catégorie de sièges au sein d'un lieu."""
    def __init__(self, idCategorieSiege: str, nomCategorie: str, prix: float, sieges: List[Siege]):
        self.idCategorieSiege = idCategorieSiege # Ex: "SCA-STD"
        self.nomCategorie = nomCategorie # Ex: "Standard"
        self.prix = prix
        self.sieges: List[Siege] = sieges # Liste des objets Siege de cette catégorie

    def __str__(self) -> str:
        return f"Catégorie: {self.nomCategorie} ({self.idCategorieSiege}), Prix: {self.prix}€, Sièges: {len(self.sieges)}"

# ===============================
# Classe : Lieu
# ===============================
class Lieu:
    """Représente la configuration complète d'un lieu, y compris ses catégories de sièges."""
    def __init__(self, nomLieu: str, adresse: str, capaciteTotaleIndicative: int, categories: List[CategorieSiege]):
        self.nomLieu = nomLieu
        self.adresse = adresse
        self.capaciteTotaleIndicative = capaciteTotaleIndicative
        self.categories: List[CategorieSiege] = categories

    def __str__(self) -> str:
        return f"Lieu: {self.nomLieu}, Adresse: {self.adresse}, Catégories: {len(self.categories)}"

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
