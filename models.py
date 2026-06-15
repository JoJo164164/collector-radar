from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String, unique=True)
    price = Column(String)
    image = Column(String)
