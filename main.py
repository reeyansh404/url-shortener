from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from fastapi.responses import RedirectResponse

app = FastAPI()
db = {}

class UrlRequest(BaseModel):
    url: str
    
@app.post("/shorten")
def shorten_url(request: UrlRequest):
    shorten_code = str(uuid.uuid4())
    db[shorten_code] = request.url
    return {"shorten_code":shorten_code}

@app.get("/{shorten_code}")
def redirect_url(shorten_code:str):
    return RedirectResponse(db[shorten_code])