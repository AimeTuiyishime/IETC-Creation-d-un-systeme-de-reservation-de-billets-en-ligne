import unittest
import sys
import os

# Ajoute le répertoire parent au sys.path pour permettre l'import du package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from package.package_class_base import Client, Reservation, Evenement
import datetime

class TestClient(unittest.TestCase):

    def setUp(self):
        """Initialise les objets nécessaires pour les tests."""
        self.client1 = Client(idClient=1, nom="Test User", email="test@example.com", mdp="password")
        self.evenement1 = Evenement(id_event=1, nom="Concert Rock", date="2024-12-25 20:00", lieu="Stade de France", description="Un concert exceptionnel", places=100, prix=50.0)
        self.reservation1 = Reservation(idReservation=1, idClient=1, dateReservation=datetime.datetime.now())

    def test_initialisation_client(self):
        """Teste l'initialisation correcte d'un client."""
        self.assertEqual(self.client1.idClient, 1)
        self.assertEqual(self.client1.nom, "Test User")
        self.assertEqual(self.client1.email, "test@example.com")
        self.assertEqual(self.client1.mdp, "password")
        self.assertEqual(self.client1.reservations, [])

    def test_effectuer_reservation(self):
        """Teste l'ajout d'une réservation à la liste des réservations du client."""
        self.client1.effectuerReservation(self.reservation1)
        self.assertIn(self.reservation1, self.client1.reservations)
        self.assertEqual(len(self.client1.reservations), 1)

        # Ajout d'une deuxième réservation pour vérifier
        reservation2 = Reservation(idReservation=2, idClient=1, dateReservation=datetime.datetime.now())
        self.client1.effectuerReservation(reservation2)
        self.assertIn(reservation2, self.client1.reservations)
        self.assertEqual(len(self.client1.reservations), 2)

if __name__ == '__main__':
    unittest.main()
