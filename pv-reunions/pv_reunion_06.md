# Réunion d’état d’avancement du projet

**Date :** 21 juin 2025
**Lieu :** En ligne
**Participants :** Aimé, Néhémie

---

## Ordre du jour

* Implémentation des classes définies dans l’issue `feat(stage)`
* Rédaction et exécution de tests unitaires
* Suivi de l’intégration via Git
* Préparation au merge de la branche `feature_stage`

---

## Éléments discutés

### 1. Implémentation des classes métier

Les classes suivantes ont été implémentées conformément à l’issue :

* `CategorieDeSiege` : gestion des types de sièges et de leur tarification.
* `Siege` : gestion de la disponibilité des places.
* `Newsletter` : gestion des abonnements et envois de messages.
* Toutes ces classes ont été ajoutées au dépôt dans la structure `package/`.

### 2. Tests unitaires

* Création du dossier `tests/` pour centraliser tous les fichiers de test.
* Rédaction de tests pour chaque classe créée (`test_paiement.py`, `test_lieu.py`, etc.).
* Utilisation du module `unittest`.
* Correction de certaines erreurs logiques détectées pendant les tests (ex : erreur sur l’annulation de réservation dans la classe `Lieu`).

### 3. Gestion Git et organisation du code

* Push régulier des fichiers dans la branche `feature_stage`.
* Création du fichier `class_additionnel.py` regroupant toutes les classes en un seul module.
* Suppression de l’ancien fichier `package_class_Nehemie.py`.
* Mise à jour des imports dans `main.py`.
* Ajout du fichier `.gitignore` pour ignorer les fichiers `.pyc`.

### 4. Pull Request et résolution de conflits

* Création d’un Pull Request vers la branche `develop`.
* Conflit détecté dans `main.py` lors du merge.
* Résolution manuelle via l’éditeur en ligne GitHub.
* Pull Request validé et merge effectué avec succès.

---

## Points d'action

* Supprimer les fichiers obsolètes après merge si ce n’est pas encore fait.
* Poursuivre avec l'intégration dans l’interface graphique si besoin.
* Continuer les tests à chaque modification de classe.

---




