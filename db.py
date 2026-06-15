from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///collector.db", echo=False)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    price = Column(Float)
    platform = Column(String)
    url = Column(String, unique=True)
    image = Column(String)
    time = Column(String)
    created_at = Column(DateTime, default=datetime.now)
favorite = Column(Boolean, default=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
