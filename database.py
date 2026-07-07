from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./cipher.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Users table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="manager")  # "manager" or "investment_manager"
    asset_class = Column(String, nullable=True)  # Only for managers
    institution_name = Column(String, nullable=True)
    institution_location = Column(String, nullable=True)  # Only for investment managers
    job_title = Column(String, nullable=True)  # Only for investment managers
    phone_number = Column(String, nullable=True)  # Only for investment managers
    created_at = Column(DateTime, default=datetime.utcnow)
    submissions = relationship("Submission", back_populates="manager")

# Submissions table
class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"))
    total_invested = Column(Float, nullable=False)
    total_gained = Column(Float, nullable=False)
    total_lost = Column(Float, nullable=False)
    notes = Column(String)
    submitted = Column(Boolean, default=False)
    submitted_at = Column(DateTime)
    period = Column(String, nullable=False)
    manager = relationship("User", back_populates="submissions")

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()