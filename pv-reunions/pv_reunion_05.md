# Réunion d’état d’avancement du projet

**Date :** 14 juin 2025
**Lieu :** En ligne
**Participants :** Aimé, Néhémie

---

## Ordre du jour

* Création des issues GitHub
* Répartition des classes à implémenter
* Planification des tâches de développement

---

## Éléments discutés

### 1. Création des issues

* Mise en place de plusieurs issues sur GitHub pour organiser le travail en tâches précises.
* Chaque issue correspond à un groupe fonctionnel ou à une fonctionnalité à développer.
* Exemple : `feat(stage) Ajout des classes pour la gestion des salles et paiements`.

### 2. Répartition des classes à implémenter

* Les classes nécessaires au système de réservation ont été identifiées :

  * `Lieu` : gérer les informations sur le lieu d’un événement.
  * `CategorieDeSiege` : modéliser les différentes catégories de sièges et leur tarification.
  * `Siege` : gérer les disponibilités des sièges.
  * `Paiement` : gérer les paiements et leur état.
  * `Newsletter` : gérer les abonnements et envois d’informations.
  * Répartition des responsabilités entre les membres 


### 3. Planification du travail

* Travail à réaliser dans une branche dédiée (`feature_stage`, `feature_clase_base`, etc).
* Chaque classe sera testée individuellement (prévu dans des fichiers de test séparés).
* Une fois toutes les classes terminées et testées, elles seront regroupées dans un fichier commun pour faciliter l’intégration (`classe_additionnel.py`).

---

## Points d'action

* Les tests unitaires seront rédigés en parallèle ou après la finalisation des classes.
* Création d’un pull request une fois les tâches terminées pour un merge dans `develop`.

---

