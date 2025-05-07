from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USER

"""
    Ce fichier configure la connexion à la base de données MySQL via SQLAlchemy.
    il définit :
        - l'engine de connexion à partir des variables d'environnement (.env)
        - la session locale (Sessionlocal) utilisée les managers
        (client, contract, event, gestion)
        - la base déclarative (Base) utilisée pour les modèles ORM.
    Utilisé dans tout le projet pour interagir avec la base de données.
"""

DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}/{DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
