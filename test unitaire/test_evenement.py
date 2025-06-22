import unittest
import sys
import os

# Ajoute le répertoire parent au sys.path pour permettre l'import du package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from package.package_class_base import Evenement

class TestEvenement(unittest.TestCase):

    def setUp(self):
        """Initialise un objet Evenement pour les tests."""
        self.evenement = Evenement(
            id_event=1,
            nom="Concert de Test",
            date="2024-07-28 20:00",
            lieu="Salle de Test",
            description="Un événement pour les tests unitaires.",
            places=100,
            prix=25.50
        )

    def test_initialisation_evenement(self):
        """Teste l'initialisation correcte d'un événement."""
        self.assertEqual(self.evenement.id_event, 1)
        self.assertEqual(self.evenement.nom, "Concert de Test")
        self.assertEqual(self.evenement.date, "2024-07-28 20:00")
        self.assertEqual(self.evenement.lieu, "Salle de Test")
        self.assertEqual(self.evenement.description, "Un événement pour les tests unitaires.")
        self.assertEqual(self.evenement.places_disponibles, 100)
        self.assertEqual(self.evenement.prix, 25.50)

    def test_afficher_details(self):
        """Teste la méthode afficher_details."""
        details = self.evenement.afficher_details()
        self.assertIn("Nom: Concert de Test", details)
        self.assertIn("Date: 2024-07-28 20:00", details)
        self.assertIn("Lieu: Salle de Test", details)
        self.assertIn("Description: Un événement pour les tests unitaires.", details)
        self.assertIn("Prix: 25.5 €", details) # Notez le formatage du prix
        self.assertIn("Places disponibles: 100", details)

    def test_verifier_disponibilite_places_suffisantes(self):
        """Teste la vérification de disponibilité avec suffisamment de places."""
        self.assertTrue(self.evenement.verifier_disponibilite_places(50))
        self.assertTrue(self.evenement.verifier_disponibilite_places(100))

    def test_verifier_disponibilite_places_insuffisantes(self):
        """Teste la vérification de disponibilité avec un nombre de places insuffisant."""
        self.assertFalse(self.evenement.verifier_disponibilite_places(101))

    def test_verifier_disponibilite_places_exactement_zero(self):
        """Teste la vérification de disponibilité quand on demande 0 places (devrait être vrai)."""
        self.assertTrue(self.evenement.verifier_disponibilite_places(0))

    def test_verifier_disponibilite_places_negatives(self):
        """Teste la vérification de disponibilité avec un nombre de places négatif (devrait être vrai car >= )."""
        self.assertTrue(self.evenement.verifier_disponibilite_places(-5))


    def test_reserver_places_succes(self):
        """Teste la réservation réussie de places."""
        self.assertTrue(self.evenement.reserver_places(30))
        self.assertEqual(self.evenement.places_disponibles, 70) # 100 - 30

    def test_reserver_places_exactement_disponibles(self):
        """Teste la réservation de toutes les places disponibles."""
        self.assertTrue(self.evenement.reserver_places(100))
        self.assertEqual(self.evenement.places_disponibles, 0)

    def test_reserver_places_echec_pas_assez_de_places(self):
        """Teste l'échec de la réservation par manque de places."""
        self.assertFalse(self.evenement.reserver_places(150))
        self.assertEqual(self.evenement.places_disponibles, 100) # Inchangé

    def test_reserver_zero_places(self):
        """Teste la réservation de zéro place."""
        self.assertTrue(self.evenement.reserver_places(0)) # Devrait réussir et ne rien changer
        self.assertEqual(self.evenement.places_disponibles, 100)

    def test_annuler_places_reservees(self):
        """Teste l'annulation de places réservées."""
        self.evenement.reserver_places(40) # Places = 60
        self.assertEqual(self.evenement.places_disponibles, 60)
        
        self.evenement.annuler_places_reservees(20)
        self.assertEqual(self.evenement.places_disponibles, 80) # 60 + 20

    def test_annuler_plus_de_places_que_reservees_initialement(self):
        """Teste l'annulation qui augmente les places au-delà du total initial (comportement actuel)."""
        self.evenement.reserver_places(50) # Places = 50
        self.evenement.annuler_places_reservees(60) # Places = 50 + 60 = 110
        self.assertEqual(self.evenement.places_disponibles, 110)
        # Ce test met en évidence que la logique actuelle ne vérifie pas par rapport à un "total initial"
        # mais ajoute simplement au nombre de places disponibles.

    def test_annuler_zero_places(self):
        """Teste l'annulation de zéro place."""
        initial_places = self.evenement.places_disponibles
        self.evenement.annuler_places_reservees(0)
        self.assertEqual(self.evenement.places_disponibles, initial_places)


if __name__ == '__main__':
    unittest.main()
