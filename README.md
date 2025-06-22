# Projet de Réservation de Billets

## Objectif du projet

Ce projet a pour but de développer une application de réservation de billets pour des événements (concerts, spectacles, etc.) en modélisant les interactions entre clients, événements, sièges, paiements et autres entités via la programmation orientée objet en Python.

## Architecture générale

Le projet repose sur les classes suivantes :

- Client  
- Réservation  
- Billet  
- Événement  
- Lieu  
- Siège  
- CatégorieDeSiège  
- Paiement  
- Newsletter  

Toutes les relations sont décrites dans le diagramme de classes en UML (voir dossier diagramme).

## Fonctionnalités principales

- Créer un compte client  
- Réserver un ou plusieurs billets pour un événement  
- Choisir un siège en fonction de la catégorie  
- Effectuer un paiement  
- S'inscrire à une newsletter si besoin  

## Technologies utilisées

- Python 3.x  
- Paradigme orienté objet (POO)

## Équipe projet

- Grobloc (Aime)  
- El-Nehmo (Nehemie)

mise à jour le 22/06/2025 par Grobloc:

L'application offre une interface utilisateur graphique (GUI) développée avec `tkinter` permettant les actions suivantes :

-   **Authentification des utilisateurs**: Connexion sécurisée pour les clients enregistrés. Les données utilisateurs sont chargées depuis `données.json`.
-   **Consultation des événements**: Les utilisateurs peuvent visualiser la liste des événements disponibles (chargés depuis `données_event.json`), consulter leurs détails (date, lieu, description, prix) et voir le nombre de places restantes en temps réel.
-   **Réservation de billets**:
    -   Sélection d'un événement et du nombre de billets souhaités.
    -   Vérification de la disponibilité des places avant la confirmation.
    -   Association de la réservation au client connecté.
-   **Gestion des réservations**:
    -   Visualisation des billets et réservations actives pour l'utilisateur connecté.
    -   Annulation de réservations, ce qui met à jour dynamiquement le nombre de places disponibles pour l'événement concerné.
    -   **Persistance des réservations par session**: Les réservations d'un utilisateur restent accessibles s'il se déconnecte puis se reconnecte au cours de la même session d'utilisation de l'application.

Fonctionnalités prévues (partiellement ou non encore implémentées dans la GUI actuelle) :
-   Choix spécifique des sièges par catégorie.
-   Processus de paiement.
-   Abonnement à la Newsletter