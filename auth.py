from models.models import User
from database import SessionLocal
from utils import check_password



def authentication_user(email,  mot_de_passe):
    db = SessionLocal()
    try:
        user  = db.query(User).filter(User.email == email).first()
   
        if not user:
            return None , "Identifiant inccorect"
        
            
        if not check_password(mot_de_passe, user.password):
            return None, "Mot de passe Incorrect"       
            
        return user, None
    finally:
        db.close()


  
