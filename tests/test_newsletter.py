import unittest
from package.newsletter import Newsletter

class TestNewsletter(unittest.TestCase):

    def setUp(self):
        self.newsletter = Newsletter(1, "user@example.com")

    def test_etat_initial(self):
        self.assertFalse(self.newsletter.estActif)# Vérifie que l'état initial est inactif

    def test_confirmation_abonnement(self):
        self.newsletter.confirmerAbonnement()
        self.assertTrue(self.newsletter.estActif)

    #
    def test_envoi_newsletter_actif(self):
        self.newsletter.confirmerAbonnement()# Confirmer l'abonnement avant l'envoi
        result = self.newsletter.envoyerNewsLetter("Ceci est un message test.")
        self.assertTrue(result)

    def test_envoi_newsletter_inactif(self):
        result = self.newsletter.envoyerNewsLetter("Message bloqué")# Essayer d'envoyer sans confirmer l'abonnement
        self.assertFalse(result)
