from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    platform = Column(String)
    url = Column(String, unique=True)
    image = Column(String)
    time = Column(String)
    favorite = Column(Boolean, default=False)
