from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import uuid
from fastapi.responses import RedirectResponse
from database import SessionLocal
from models import Link, User
from sqlalchemy.orm import Session
from auth import hash_password, verify_password, create_token

app = FastAPI()
db = {}

class UrlRequest(BaseModel):
    url: str
    
class UserRequest(BaseModel):
    email: str
    password: str
    
def get_db():
    db = SessionLocal() #open a session
    yield db #pause the session 
    db.close()
    
@app.post("/shorten")
def shorten_url(request: UrlRequest, db: Session = Depends(get_db)):
    shorten_code = str(uuid.uuid4())
    link = Link(long_url = request.url ,  short_code = shorten_code)
    db.add(link)
    db.commit()
    return{"shorten_code" : shorten_code}

@app.get("/{shorten_code}")
def redirect_url(shorten_code:str, db: Session = Depends(get_db)):
    output = db.query(Link).filter(Link.short_code == shorten_code).first()
    if output is None:
        raise HTTPException(status_code=404, detail='Short Code not found')
    return RedirectResponse(output.long_url)


@app.post("/signup")
def user_signup(request: UserRequest, db:Session=Depends(get_db)):
    hashed = hash_password(request.password).decode("utf-8")
    user = User(email = request.email, password = hashed)
    db.add(user)
    db.commit()
    return{"message": "User created successfully!"}

@app.post("/login")
def user_login(request: UserRequest, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='Email not found')
    
    if not verify_password(request.password, user.password.encode("utf-8")):
        raise HTTPException(status_code=404, detail="Incorrect Password")

    token = create_token(user.id)
    return {"token": token}
    
