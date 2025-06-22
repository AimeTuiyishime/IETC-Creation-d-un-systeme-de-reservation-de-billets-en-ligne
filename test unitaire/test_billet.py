import unittest
import sys
import os

# Ajoute le répertoire parent au sys.path pour permettre l'import du package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from package.package_class_base import Billet

class TestBillet(unittest.TestCase):

    def setUp(self):
        """Initialise un objet Billet pour les tests."""
        self.billet = Billet(
            id_billet=101,
            id_event=202,
            id_reservation=303,
            prix=75.25
        )

    def test_initialisation_billet(self):
        """Teste l'initialisation correcte d'un billet."""
        self.assertEqual(self.billet.id_billet, 101)
        self.assertEqual(self.billet.id_event, 202)
        self.assertEqual(self.billet.id_reservation, 303)
        self.assertEqual(self.billet.prix, 75.25)

    def test_afficher_details_billet(self):
        """Teste la méthode afficher_details_billet."""
        nom_evenement_test = "Premiere Mondiale du Film X"
        details = self.billet.afficher_details_billet(nom_evenement_test)
        
        expected_details = f"Billet ID: 101 ({nom_evenement_test}) - Résa. ID: 303 - Prix: 75.25 €"
        self.assertEqual(details, expected_details)

    def test_afficher_details_billet_nom_evenement_vide(self):
        """Teste la méthode afficher_details_billet avec un nom d'événement vide."""
        nom_evenement_test = ""
        details = self.billet.afficher_details_billet(nom_evenement_test)
        
        expected_details = f"Billet ID: 101 () - Résa. ID: 303 - Prix: 75.25 €"
        self.assertEqual(details, expected_details)

    def test_afficher_details_billet_prix_zero(self):
        """Teste la méthode afficher_details_billet avec un prix de zéro."""
        billet_prix_zero = Billet(id_billet=102, id_event=203, id_reservation=304, prix=0.0)
        nom_evenement_test = "Événement Gratuit"
        details = billet_prix_zero.afficher_details_billet(nom_evenement_test)
        
        expected_details = f"Billet ID: 102 ({nom_evenement_test}) - Résa. ID: 304 - Prix: 0.0 €"
        self.assertEqual(details, expected_details)

if __name__ == '__main__':
    unittest.main()
