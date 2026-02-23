# 🔐 Coffre-Fort de Mots de Passe (Password Manager)

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-success.svg)
![Cryptography](https://img.shields.io/badge/Security-Fernet_AES128-orange.svg)
![Architecture](https://img.shields.io/badge/Architecture-MVC-purple.svg)

Un gestionnaire de mots de passe de bureau sécurisé, moderne et entièrement hors-ligne, conçu avec Python.

Ce projet a été développé avec une **architecture logicielle stricte (MVC)** et met en œuvre des standards de sécurité reconnus pour la protection des données sensibles.

---

## ✨ Fonctionnalités clés

- **Maître du coffre** : Sécurisation de l'ensemble de l'application via un mot de passe maître unique (hashé avec sel).
- **Chiffrement fort** : Tous les mots de passe enregistrés sont chiffrés en base de données (Fernet / AES-128).
- **Générateur intégré** : Création de mots de passe cryptographiquement sûrs et configurables (longueur, caractères, symboles).
- **Indicateur de force** : Évaluation visuelle en temps réel de la complexité des mots de passe.
- **Interface UI Moderne** : Rendu "Dark Mode" de type Dashlane/KeePassXC grâce à la librairie `CustomTkinter`.
- **Gestion presse-papiers** : Copie des identifiants et mots de passe d'un simple clic pour faciliter la navigation.

---

## 🏗️ Architecture et Choix Techniques

Ce projet a été construit comme une application maintenable et évolutive, en séparant rigoureusement la logique métier, l'accès aux données, et l'interface utilisateur.

### 1. Architecture MVC (Model-View-Controller)
Plutôt que d'avoir un "code spaghetti" où l'interface et la base de données se mélangent, j'ai implémenté le pattern MVC :
- **Models (`models/`)** : Gèrent les données brutes. Ils ne savent rien de l'interface.
  - `database.py` gère le CRUD SQLite.
  - `crypto.py` gère le chiffrement/déchiffrement bruts.
  - `password_generator.py` contient la logique de création de mots de passe.
- **Views (`views/`)** : Gèrent uniquement l'affichage (CustomTkinter). Elles ne manipulent pas directement la base de données, mais envoient des requêtes aux Controllers.
- **Controllers (`controllers/`)** : Le chef d'orchestre. Ils reçoivent les actions de l'utilisateur venant des Views, appellent les Models pour traiter la donnée, et renvoient le résultat.

> *Pourquoi ce choix ?* L'architecture MVC permet des tests unitaires beaucoup plus simples, et rend possible le changement total d'interface (par exemple, passer sur une interface Web ou Mobile) sans avoir à réécrire la moindre ligne de code liée à la sécurité ou à la base de données.

### 2. Sécurité & Chiffrement
La sécurité a été le cœur de la réflexion sur ce projet.

- **Dérivation de clé (PBKDF2)** : Le mot de passe maître n'est *jamais* stocké. À la création, on génère un sel aléatoire de 32 octets, puis on applique l'algorithme PBKDF2 avec SHA-256 sur 480 000 itérations. C'est ce **Hash** qui est stocké.
- **Protection des données** : Pour chiffrer les champs sensibles, on utilise la spécification **Fernet** de la bibliothèque `cryptography` (qui implémente AES-128 en mode CBC, avec signature HMAC-SHA256).
- **Génération aléatoire (Secrets)** : Le générateur de mot de passe n'utilise *pas* le module basique `random` de Python (qui est prévisible car basé sur l'horloge système), mais le module `secrets` du système d'exploitation, garantissant une entropie cryptographiquement sûre.

### 3. Base de données
Le choix s'est porté sur **SQLite3** :
- *Serverless* : Aucune installation de serveur nécessaire, parfait pour une application Desktop hors-ligne et pour une montée en compétence sans but lucratif.
- Les données restent totalement sur la machine de l'utilisateur (le fichier `passwords.db`), garantissant la souveraineté des données.

### 4. Interface Graphique (UI/UX)
J'ai choisi de remplacer le vieux module natif `Tkinter` (qui a un aspect très daté "Windows 95") par **CustomTkinter** :
- Support natif des thèmes sombres (Dark Mode) et des couleurs d'accentuation (ici, une vibe verte *Dashlane-like*).
- Angles arrondis et design épuré offrant une expérience utilisateur professionnelle, rassurante et dans l'air du temps.

---

## 🚀 Installation & Lancement

**Prérequis :** Python 3.10 ou supérieur.

1. Clonez ce dépôt sur votre machine.
2. Basculez dans le dossier du projet :
   ```bash
   cd Password_Manager
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancez l'application :
   ```bash
   python main.py
   ```

*(Lors du premier lancement, l'application vous demandera de créer un Mot de Passe Maître, qui générera automatiquement le fichier base de données `passwords.db`)*

---

## 🛠️ Stack Technique

- **Langage principal** : Python 3
- **Base de données** : SQLite3
- **UI Framework** : CustomTkinter
- **Librairies de sécurité** : `cryptography`, `hashlib`, `secrets`
- **Utilitaires** : `pyperclip` (gestion du presse-papier)

---

*Projet réalisé dans le cadre d'une montée en compétences sur le langage Python, la sécurité logicielle et la structuration MVC.*
