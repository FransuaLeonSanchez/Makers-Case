from sqlalchemy import Column, Integer, String, Float, Boolean, Enum as SQLEnum, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

Base = declarative_base()

class ProductCategory(str, Enum):
    COMPUTADORAS = "COMPUTADORAS"
    LAPTOPS = "LAPTOPS"
    TABLETS = "TABLETS"
    CELULARES = "CELULARES"
    ACCESORIOS = "ACCESORIOS"
    PERIFERICOS = "PERIFERICOS"
    MONITORES = "MONITORES"
    IMPRESORAS = "IMPRESORAS"

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    model = Column(String)
    category = Column(SQLEnum(ProductCategory))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)
    specifications = Column(Text)
    is_active = Column(Boolean, default=True)

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String)
    product_brand = Column(String)
    price = Column(Float)
    quantity = Column(Integer, default=1)
    customer_info = Column(String)  # Puede ser email o teléfono
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String, default="pending")  # pending, confirmed, cancelled

class ProductCreate(BaseModel):
    name: str
    brand: str
    model: str
    category: ProductCategory
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: str
    specifications: str
    
class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    category: ProductCategory
    price: float
    stock: int
    description: str
    specifications: str
    is_active: bool
    
    class Config:
        from_attributes = True 