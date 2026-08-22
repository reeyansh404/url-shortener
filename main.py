from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import uuid
from fastapi.responses import RedirectResponse
from database import SessionLocal
from models import Link
from sqlalchemy.orm import Session

app = FastAPI()
db = {}

class UrlRequest(BaseModel):
    url: str
    
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

    


    
