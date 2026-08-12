from sqlalchemy import JSON, Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, default="pending")
    version = Column(Integer, default=1)
    
    items = Column(JSON, nullable=False)