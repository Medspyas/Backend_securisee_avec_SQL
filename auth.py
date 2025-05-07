from database import SessionLocal
from models.models import User
from utils import check_password

"""
    Cette fonction gère l'authentification des utilisateurs de la plateforme CRM.
    Il vérifie les identifiants fournis (email et mot de passe),
    et retourne les informations de l'utilisateur en cas de succès.
"""


def authentication_user(email, mot_de_passe):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None, "Identifiant inccorect"

        if not check_password(mot_de_passe, user.password):
            return None, "Mot de passe Incorrect"

        return user, None
    finally:
        db.close()
