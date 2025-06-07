# Réunion d’état d’avancement du projet

**Date :** 7 juin 2025  
**Lieu :** En ligne 
**Participants :** Aimé, Néhémie

---

## Ordre du jour

- Analyse intermédiaire du projet
- Diagramme de classe : retour sur la version actuelle
- Organisation des branches Git
- Réorganisation du dépôt et des fichiers
- Prochaines étapes

---

## Éléments discutés

### 1. Structure du dépôt Git
- Maintien de `main` comme branche de production stable.
- Proposition d’introduire une branche intermédiaire pour les pré-intégrations.
- Création de branches selon les issues.

### 2. Organisation du projet Python
- Réorganisation du code selon une structure en dossiers :
  - `ui/` : pour la gestion de l’interface
  - `services/` : pour la logique métier
  - `tools/` : pour les fonctions utilitaires
  - `repositories/` : pour les classes d’accès aux données

### 3. Diagramme de classes
- Le diagramme sera transformé en **version horizontale** pour plus de clarté.
- Chaque version du diagramme doit être conservée dans un dossier dédié.

### 4. README.md
- À compléter avec :
  - Objectif du projet
  - Contraintes techniques
  - Technologies utilisées
  - Instructions d'installation
  - Diagramme UML

---

## Points d'action

- Ajouter un dossier `diagrammes/` avec l’historique des versions UML
- Réorganiser les fichiers existants selon les nouveaux dossiers
- Finaliser le `README.md`
- Étudier TicketMaster pour comprendre la logique de réservation professionnelle
- Mettre en place les nouvelles branches de travail

