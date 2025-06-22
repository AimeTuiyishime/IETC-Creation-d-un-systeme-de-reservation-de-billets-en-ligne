import unittest
from package.package_class_additionnel import Paiement

class TestPaiement(unittest.TestCase):

    def test_initial_state(self):
        p = Paiement(1, 1001, 50.0)
        self.assertEqual(p.statutPaiement, "En attente")
        self.assertIsNone(p.datePaiement)

    def test_effectuer_paiement(self):
        p = Paiement(2, 1002, 75.0)
        result = p.effectuerPaiement()
        self.assertTrue(result)
        self.assertEqual(p.statutPaiement, "Payé")
        self.assertIsNotNone(p.datePaiement)

    def test_double_paiement(self):
        p = Paiement(3, 1003, 90.0)
        p.effectuerPaiement()
        result = p.effectuerPaiement()
        self.assertFalse(result)  # ne peut pas payer deux fois

    def test_rembourser(self):
        p = Paiement(4, 1004, 40.0)
        p.effectuerPaiement()
        result = p.rembourserPaiement()
        self.assertTrue(result)
        self.assertEqual(p.statutPaiement, "Remboursé")
