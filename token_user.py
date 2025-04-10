import jwt
from config import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_SECONDS, TOKEN_FILENAME
from datetime import datetime, timedelta, timezone
import os

def create_token(user):
    expiration_time = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRATION_SECONDS)
    infos = {
    "user_id": user.id,
    "email": user.email,
    "rôle": user.role.value,
    "exp": int(expiration_time.timestamp())
    }

    token = jwt.encode(infos, SECRET_KEY, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    with open(TOKEN_FILENAME, 'w') as f:
        f.write(token)
    
    

def read_token():
    if not os.path.exists('.jwt_token'):
        return None
    try:
        with open(TOKEN_FILENAME, 'r') as f:
            token = f.read()
        infos = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return infos
    
    except jwt.ExpiredSignatureError:
        return None
    
    except jwt.InvalidTokenError:
        return None
    