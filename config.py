import os

from dotenv import load_dotenv

"""
   Ce fichier centralise la configuration du projet.
    Il charge les variables d'environnement définies dans le fichier '.env',
    notamment les informations de connexion à la base de données (MySQL)
    et la clés DSN de Sentry.
    Ces variables ensuite utilisées dans d'autres modules
    comme 'database.py' ou 'sentry_sdk'.
"""

load_dotenv()


DATABASE_USER = os.getenv("DATABASE_USER")

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")

DATABASE_NAME = os.getenv("DATABASE_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

TOKEN_FILENAME = os.getenv("TOKEN_FILENAME")

JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS"))

DSN_KEY = os.getenv("DSN_KEY")
