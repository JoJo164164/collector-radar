from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///collector.db", echo=False)

Base = declarative_base()

# ======================
# 商品主表
# ======================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    price = Column(Float)
    platform = Column(String)
    url = Column(String, unique=True)
    image = Column(String)
    time = Column(String)

    # ⭐ 收藏功能
    favorite = Column(Boolean, default=False)


# ======================
# 價格歷史表
# ======================
class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    price = Column(Float)
    time = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
