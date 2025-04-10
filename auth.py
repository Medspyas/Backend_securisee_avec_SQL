from models import User
from database import SessionLocal


email = "test@mail.com"

mot_de_passe = "1234"


def authentication_user(email,  mot_de_passe):
    db = SessionLocal()
    try:
        user  = db.query(User).filter(User.email == email).first()
   
        if not user:
            return"Identifiant inccorect"
        
            
        if  user.password != mot_de_passe:
            return "Mot de passe Incorrect"       
            
        return user
    finally:
        db.close()


  
