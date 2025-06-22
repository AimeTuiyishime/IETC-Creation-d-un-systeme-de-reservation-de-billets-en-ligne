import unittest
from package.package_class_additionnel import Lieu

class TestLieu(unittest.TestCase):

    def setUp(self):
        self.lieu = Lieu(1, "Salle Polyvalente", "123 Rue des Événements", 100)

    def test_initial_values(self):
        self.assertEqual(self.lieu.capacite, 100)
        self.assertEqual(self.lieu.nombrePlacesDisponiblesInitial, 100)
        self.assertEqual(self.lieu.nombrePlacesRestantes, 100)

    def test_reservation_valide(self):
        result = self.lieu.reserver_places(10)
        self.assertTrue(result)
        self.assertEqual(self.lieu.nombrePlacesRestantes, 90)

    def test_reservation_excedentaire(self):
        result = self.lieu.reserver_places(150)
        self.assertFalse(result)
        self.assertEqual(self.lieu.nombrePlacesRestantes, 100)

    def test_annulation_valide(self):
        self.lieu.reserver_places(10)
        result = self.lieu.annuler_reservation(5)
        self.assertTrue(result)
        self.assertEqual(self.lieu.nombrePlacesRestantes, 95)

    def test_annulation_excedentaire(self):
        self.lieu.reserver_places(10) 
        result = self.lieu.annuler_reservation(5)
        self.assertTrue(result)

        result = self.lieu.annuler_reservation(100)
        self.assertFalse(result)
