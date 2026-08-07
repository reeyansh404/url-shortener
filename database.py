from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("postgresql://localhost/url_shortener")

SessionLocal = sessionmaker(bind = engine)

class Base(DeclarativeBase):
    pass

import models
Base.metadata.create_all(engine)