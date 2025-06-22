import unittest
import sys
import os
import datetime

# Ajoute le répertoire parent au sys.path pour permettre l'import du package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from package.package_class_base import Reservation, Billet, Evenement

class TestReservation(unittest.TestCase):

    def setUp(self):
        """Initialise les objets nécessaires pour les tests."""
        self.evenement1 = Evenement(id_event=1, nom="Concert Pop", date="2025-01-15 19:00", lieu="Zenith", description="Concert Pop", places=50, prix=30.0)
        self.evenement2 = Evenement(id_event=2, nom="Festival Jazz", date="2025-03-20 15:00", lieu="Parc Floral", description="Festival de Jazz en plein air", places=0, prix=25.0) # Pas de places
        self.reservation = Reservation(idReservation=1, idClient=1, dateReservation=datetime.datetime.now())
        Reservation._prochain_id_billet = 1 # Réinitialiser pour la prédictibilité des ID de billets

    def test_initialisation_reservation(self):
        """Teste l'initialisation correcte d'une réservation."""
        self.assertEqual(self.reservation.idReservation, 1)
        self.assertEqual(self.reservation.idClient, 1)
        self.assertIsInstance(self.reservation.dateReservation, datetime.datetime)
        self.assertEqual(self.reservation.montantTotal, 0.0)
        self.assertEqual(self.reservation.billets, [])

    def test_ajouter_billet_succes(self):
        """Teste l'ajout réussi d'un billet à la réservation."""
        self.assertTrue(self.reservation.ajouterBillet(self.evenement1, 1))
        self.assertEqual(len(self.reservation.billets), 1)
        self.assertEqual(self.reservation.montantTotal, self.evenement1.prix)
        self.assertEqual(self.reservation.billets[0].id_billet, 1)
        self.assertEqual(self.reservation.billets[0].id_event, self.evenement1.id_event)
        self.assertEqual(self.reservation.billets[0].prix, self.evenement1.prix)
        self.assertEqual(self.evenement1.places_disponibles, 49) # 50 - 1

    def test_ajouter_billet_plusieurs_succes(self):
        """Teste l'ajout réussi de plusieurs billets."""
        self.assertTrue(self.reservation.ajouterBillet(self.evenement1, 3))
        self.assertEqual(len(self.reservation.billets), 3)
        self.assertEqual(self.reservation.montantTotal, self.evenement1.prix * 3)
        self.assertEqual(self.evenement1.places_disponibles, 47) # 50 - 3
        # Vérifier les ID des billets
        self.assertEqual(self.reservation.billets[0].id_billet, 1)
        self.assertEqual(self.reservation.billets[1].id_billet, 2)
        self.assertEqual(self.reservation.billets[2].id_billet, 3)


    def test_ajouter_billet_pas_assez_de_places(self):
        """Teste l'ajout de billets quand il n'y a pas assez de places."""
        self.assertFalse(self.reservation.ajouterBillet(self.evenement1, 100)) # Demande plus que disponible
        self.assertEqual(len(self.reservation.billets), 0)
        self.assertEqual(self.reservation.montantTotal, 0.0)
        self.assertEqual(self.evenement1.places_disponibles, 50) # Inchangé

    def test_ajouter_billet_evenement_sans_places(self):
        """Teste l'ajout de billets pour un événement qui n'a plus de places (places=0)."""
        self.assertFalse(self.reservation.ajouterBillet(self.evenement2, 1))
        self.assertEqual(len(self.reservation.billets), 0)
        self.assertEqual(self.reservation.montantTotal, 0.0)
        self.assertEqual(self.evenement2.places_disponibles, 0) # Inchangé

    def test_ajouter_billet_echec_reservation_places_evenement(self):
        """
        Teste le cas où l'événement ne peut pas réserver de places
        (simulé en modifiant temporairement la méthode reserver_places de l'événement).
        """
        original_reserver_places = self.evenement1.reserver_places
        self.evenement1.reserver_places = lambda quantite: False # Simule l'échec
        
        self.assertFalse(self.reservation.ajouterBillet(self.evenement1, 1))
        self.assertEqual(len(self.reservation.billets), 0)
        self.assertEqual(self.reservation.montantTotal, 0.0)
        self.assertEqual(self.evenement1.places_disponibles, 50) # Inchangé

        self.evenement1.reserver_places = original_reserver_places # Restaurer la méthode originale

    def test_confirmer_reservation(self):
        """Teste la méthode confirmerReservation."""
        # La méthode actuelle ne fait rien, donc on vérifie juste qu'elle s'exécute sans erreur.
        try:
            self.reservation.confirmerReservation()
        except Exception as e:
            self.fail(f"confirmerReservation a levé une exception inattendue: {e}")

    def test_annuler_reservation_succes(self):
        """Teste l'annulation réussie d'une réservation avec des billets."""
        self.reservation.ajouterBillet(self.evenement1, 2)
        self.assertEqual(self.evenement1.places_disponibles, 48)
        self.assertEqual(len(self.reservation.billets), 2)
        self.assertNotEqual(self.reservation.montantTotal, 0.0)

        # Créer une liste d'événements pour la passer à annulerReservation
        evenements_data = [self.evenement1, self.evenement2]
        
        self.assertTrue(self.reservation.annulerReservation(evenements_data))
        self.assertEqual(len(self.reservation.billets), 0)
        self.assertEqual(self.reservation.montantTotal, 0.0)
        self.assertEqual(self.evenement1.places_disponibles, 50) # 48 + 2

    def test_annuler_reservation_sans_billets(self):
        """Teste l'annulation d'une réservation qui ne contient aucun billet."""
        evenements_data = [self.evenement1, self.evenement2]
        self.assertFalse(self.reservation.annulerReservation(evenements_data)) # Devrait retourner False car pas de billets
        self.assertEqual(len(self.reservation.billets), 0)
        self.assertEqual(self.reservation.montantTotal, 0.0)

    def test_annuler_reservation_evenement_non_trouve(self):
        """
        Teste l'annulation d'une réservation où l'événement associé aux billets n'est pas trouvé.
        Les places ne devraient pas être remises à disposition dans ce cas spécifique,
        mais la réservation devrait quand même être vidée.
        """
        # Ajout d'un billet pour un événement fictif qui ne sera pas dans la liste evenements_data
        billet_fictif = Billet(id_billet=100, id_event=999, id_reservation=self.reservation.idReservation, prix=10.0)
        self.reservation.billets.append(billet_fictif)
        self.reservation.montantTotal = 10.0
        
        initial_places_evenement1 = self.evenement1.places_disponibles
        
        evenements_data_sans_event_concerne = [self.evenement1] # Ne contient pas l'événement avec id_event=999
        
        self.assertTrue(self.reservation.annulerReservation(evenements_data_sans_event_concerne))
        self.assertEqual(len(self.reservation.billets), 0)
        self.assertEqual(self.reservation.montantTotal, 0.0)
        # Vérifier que les places de evenement1 n'ont pas changé car le billet était pour un autre événement
        self.assertEqual(self.evenement1.places_disponibles, initial_places_evenement1)

if __name__ == '__main__':
    unittest.main()
