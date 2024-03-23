from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = Session(engine)
