import unittest
from package.siege import Siege

class TestSiege(unittest.TestCase):

    """Tests pour la classe Siege.(méthode qui initie la classe Siege)"""
    def setUp(self):
        self.siege = Siege(1, 101, 5, "A12")

    def test_etat_initial(self):
        self.assertTrue(self.siege.estDisponible())
        self.assertEqual(self.siege.identificationSiege, "A12")

    def test_reservation_reussie(self):
        result = self.siege.reserver()
        self.assertTrue(result)
        self.assertFalse(self.siege.estDisponible())

    def test_reservation_double(self):
        self.siege.reserver()
        result = self.siege.reserver()
        self.assertFalse(result)

    def test_liberation(self):
        self.siege.reserver()
        self.siege.liberer()
        self.assertTrue(self.siege.estDisponible())
