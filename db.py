from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///collector.db")
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

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
