# Réunion d’état d’avancement du projet

**Date :** 22 juin 2025
**Lieu :** En ligne
**Participants : Aimé, Néhémie

---

## Ordre du jour

* Implémentation des classes additionnelles du projet
* Rédaction des tests unitaires
* Push & organisation du code sur GitHub
* Regroupement des classes dans un seul fichier
* Résolution de conflits et merge dans `develop`

---

## Éléments discutés

### 1. Implémentation des classes

* Création des classes : `Lieu`, `Paiement`, `CategorieDeSiege`, `Siege`, `Newsletter`.
* Ajout des méthodes principales avec gestion d’état et comportements métier.
* Ajout de la documentation sur chaque classe pour faciliter la relecture.

### 2. Regroupement et refactorisation

* Regroupement des classes dans un fichier unique `classe_additionnel.py` pour plus de clarté.
* Suppression du fichier obsolète `package_class_Nehemie.py`.
* Mise à jour des imports dans `main.py`.

### 3. Tests unitaires

* Création d’un dossier `tests/` contenant des fichiers de tests unitaires pour chaque classe.
* Utilisation du module `unittest` pour valider les comportements clés (réservation, disponibilité, paiements...).
* Exécution des tests avec succès

### 4. Git & GitHub

* Création de la branche `feature_stage`.
* Commit régulier des avancées.
* Push de toutes les modifications sur GitHub.
* Création et résolution d’un **pull request** avec un conflit résolu manuellement.
* Merge réussi de `feature_stage` et des autres branches du repos dans la branche `develop`.

---

## Points d'action

* Supprimer les fichiers temporaires ou obsolètes restants (`.pyc`, anciens fichiers de classes).
* Ajouter les captures d’écran et fichiers du diagramme dans un dossier `diagrammes/`.
* Mettre à jour le `README.md` général du projet avec :

  * Objectif
  * Technologies
  * Instructions d’installation
  * Diagramme UML

---

