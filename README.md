# 🎟️ Projet de Réservation de Billets

## 🎯 Objectif du projet

Ce projet a pour but de développer une application de réservation de billets pour des événements (concerts, spectacles, etc.) en modélisant les interactions entre clients, événements, sièges, paiements et autres entités via la programmation orientée objet en Python.

---

## 🧱 Architecture générale

Le projet repose sur les classes suivantes :

- `Client`
- `Réservation`
- `Billet`
- `Événement`
- `Lieu`
- `Siège`
- `CategorieDeSiege`
- `Paiement`
- `Newsletter`

Toutes les relations sont décrites dans le diagramme de classes UML (voir dossier `diagrammes/`).

---

## 🛠️ Fonctionnalités principales

- Création d’un compte client
- Réservation d’un ou plusieurs billets pour un événement
- Choix du siège en fonction de la catégorie
- Paiement sécurisé
- Abonnement à une newsletter

---

## 🧪 Tests

Les classes métier sont testées via des fichiers `unittest` placés dans le dossier `tests/`.

Les tests couvrent les comportements principaux : réservation, paiement, annulation, disponibilité des sièges, etc.

Les tests peuvent être lancés avec :

```bash
python -m unittest discover tests
```

---

## ⚙️ Technologies utilisées

- Python 3.x
- Paradigme orienté objet (POO)
- Interface graphique (Tkinter)
- Git & GitHub pour la collaboration et le versionnement

---

## 📂 Structure du projet

```
.
.
├── main.py
├── README.md
├── requirements.txt
├── package/
│   ├── __init__.py
│   ├── package_lass_additionnel.py           # Toutes les classes métier regroupées (lieu, siège,etc)
│   ├── GUI.py                         # Interface graphique (Tkinter)
│   ├── package_classe_base.py         # Classes client, réservation regroupées
│   ├── donées_event.json
│   ├── donées_clients.json
│   ├── donées_configuration_lieux.json
├── tests unitaire/
│   ├── __init__.py
│   ├── test_lieu.py
│   ├── test_newsletter.py
│   ├── test_paiement.py
│   ├── test_siege.py
│   └── ...
└── diagrammes_classe
|    └── Diagramme_classe.pdf           # Diagramme UML des classes
├── pv-reunions/
│   ├── pv_reunion_01.md
│   ├── pv_reunion_02.md
│   └── ...


```

---

## 📦 Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/AimeTuiyishime/IETC-Creation-d-un-systeme-de-reservation-de-billets-en-ligne.git
```

2. (Optionnel mais recommandé) Créer un environnement virtuel :

```bash
python -m venv venv
```

3. **Activer l’environnement virtuel :**

- **Sous Windows :**
```cmd
venv\Scripts\activate
```

- **Sous macOS / Linux :**
```bash
source venv/bin/activate
```

---

## ▶️ Lancement du projet

```bash
python main.py
```

Cela ouvrira l’interface graphique du système de réservation.

---

---


## 🔐 Informations de connexion (comptes de test)

Utiliser les comptes enregistrés dans `package/données_clients.json` pour accéder à l'application lors des tests :

| Nom d’utilisateur | Mot de passe | Email            |
|-------------------|--------------|------------------|
| user1             | user1        | user1@test.com   |
| user2             | user2        | user2@test.com   |

## 👥 Équipe projet

- **Grobloc (Aimé)** 
- **El-Nehmo (Néhémie)** 

---



