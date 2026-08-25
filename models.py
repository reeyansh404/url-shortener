from database import Base
from sqlalchemy import Column, Integer, String

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key= True)
    long_url = Column(String)
    short_code = Column(String)
    
class User(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key = True)
    email = Column(String)
    password = Column(String)
    