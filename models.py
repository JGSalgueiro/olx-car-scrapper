from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config

Base = declarative_base()

class CarListing(Base):
    __tablename__ = 'car_listings'
    
    id = Column(Integer, primary_key=True)
    olx_id = Column(String(50), unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    price = Column(Float)
    currency = Column(String(10), default='EUR')
    location = Column(String(200))
    description = Column(Text)
    seller_name = Column(String(200))
    seller_type = Column(String(50))  # private, dealer
    car_brand = Column(String(100))
    car_model = Column(String(100))
    year = Column(Integer)
    mileage = Column(Integer)
    fuel_type = Column(String(50))
    transmission = Column(String(50))
    engine_size = Column(String(50))
    color = Column(String(100))
    url = Column(String(1000), nullable=False)
    image_urls = Column(Text)  # JSON string of image URLs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<CarListing(id={self.id}, title='{self.title}', price={self.price})>"

# Database setup
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 