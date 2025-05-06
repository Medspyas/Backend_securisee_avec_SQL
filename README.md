# CRM sécurisée, SQL - Installation et Configuration 

## Présentation du projet

Ce projet est une application CRM  développé en Python permerttant de :

- Gérer des utilisateurs internes (commerciaux, support, gestion),

- Créer et modifier des contrats, clients et évènements,

- Planifier et suivre des évènements liés aux contrats.

L'application s'exécute en ligne de commande et utilise une base donnée MySQl pour stocker les informations.     

## Installation


- Avant toute procédure vérifier que votre connexion internet est activée et aussi vérifier que vous avez installer python sur votre machine ("https://www.python.org")

- Installez git sur votre appareil sur le site "https://git-scm.com/download/win", vérifiez que git est correctement installé en tapant sur le terminal de votre machine git --version, s'il- est correctement
 
installé alors une version de git sera affiché.

- Ensuite, tapez "git clone https://github.com/Medspyas/Backend_securisee_avec_SQL" pour copier le repository de l'application sur votre appareil (placez-vous dans un répertoire spécifique que vous aurais créé au préalable.).

- Dans le dossier où vous avez cloné le projet, créez un environnement virtuel pour utiliser les bonnes versions des dépendances nécessaires à l'application.

- Tapez la commande python -m venv "le nom de votre environnement" dans le cas général, on le nomme "venv".

- Activer l'environnement virtuel : Pour windows : Executez la commande "venv/Sripts/activate". Pour macOS/Linux : Exécutez la commande "source venv/bin/activate".

- Installez les dépendances, tapez la commande "pip install -r requirements.txt".



# Utilisation

Pour utiliser l' application, suivez les étapes ci-dessous : 


1. **Initialisation de la base de données.**

**a. Préparer la base données MySQL**
Avant de lancer l'application, il faut configurer l'accés à la base de données.
Assurez-vous que MySQL est installé sur votre machine.
Créez une database pour ce programme (ex : epic_events)
Créez un utilisateur dedié et donnez lui les droits sur cette database.

**b. Configurer le fichier .env**
Configurer un fichier .env à la racine du projet avec les informations de connexion que vous aurais créer.

**c. Lier la base de données auw models du programme**
Initialisez les tables dans la base de données.
vous pouvez taper cette commande:
"from database import Base, engine
 import models.models 
 Base.metadata.create_all(bind=engine)"


2. **Lancer l'application.**
Lancez le fichier principal pour accéder au menu de gestion du CRM avec la commande "python -m view.cli"