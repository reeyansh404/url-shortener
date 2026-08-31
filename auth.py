import bcrypt
from jose import jwt 
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def create_token(user_id: int):
    data = {
        "sub": str(user_id),
        "exp": datetime.now() + timedelta(hours=24)
    }
    return jwt.encode(data, SECRET_KEY,algorithm = ALGORITHM)
    
def decode_tokens(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    