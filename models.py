from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key= True)
    long_url = Column(String)
    short_code = Column(String)
    user_id = Column(Integer, ForeignKey("userdata.id"))
    clicks = Column(Integer, default=0)
    
class User(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key = True)
    email = Column(String)
    password = Column(String)
    