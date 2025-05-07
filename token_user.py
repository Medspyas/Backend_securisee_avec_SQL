import os
from datetime import datetime, timedelta, timezone

import jwt

from config import JWT_ALGORITHM, JWT_EXPIRATION_SECONDS, SECRET_KEY, TOKEN_FILENAME

"""
    Ce fichier gère la création, la lecture des jetons (tokens)
    d'authentifications.
    Il permet de stocker localement les informations de session
    d'un utilisateur connecté,
    et de vérifier leur validité au lancement de l'application.

    Utilisé pour maintenir la session utilisateur entre deux exécutions.

"""


def create_token(user):
    expiration_time = datetime.now(timezone.utc) + timedelta(
        seconds=JWT_EXPIRATION_SECONDS
    )
    exp_timestamp = int(expiration_time.timestamp())

    infos = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value,
        "exp": exp_timestamp,
    }

    token = jwt.encode(infos, SECRET_KEY, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    with open(TOKEN_FILENAME, "w") as f:
        f.write(token)


def read_token():
    if not os.path.exists(TOKEN_FILENAME):
        return None, "missing"
    try:
        with open(TOKEN_FILENAME, "r") as f:
            token = f.read()
        infos = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return infos, "ok"

    except jwt.ExpiredSignatureError:
        return None, "expired"

    except jwt.InvalidTokenError:
        return None, "invalid"


def logout():
    print("Déconnexion réussie.")
