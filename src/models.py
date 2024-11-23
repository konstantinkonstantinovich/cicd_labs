from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from decimal import Decimal


class UnitEnum(str, Enum):
    KG = "kg"
    PIECES = "pcs"
    LITERS = "l"
    METERS = "m"
    PACK = "pack"


class Product(SQLModel, table=True):
    __tablename__ = "products"
    
    id: int = Field(primary_key=True)
    name: str = Field(default=None, max_length=255)
    price: Decimal = Field(default=None, max_digits=10, decimal_places=2)
    unit: UnitEnum = Field(default=None,)
    
    # Relationships
    sales: list["Sale"] = Relationship(back_populates="product")


class Client(SQLModel, table=True):
    __tablename__ = "clients"
    
    id: int = Field(primary_key=True)
    last_name: str = Field(default=None, max_length=255)
    first_name: str = Field(default=None, max_length=255)
    middle_name: str = Field(default=None, max_length=255)
    address: str = Field(default=None, max_length=255)
    phone: str = Field(default=None)
    email: str = Field(default=None, max_length=255)
    is_regular: bool = Field(default=False)
    
    # Relationships
    sales: list["Sale"] = Relationship(back_populates="client")


class Sale(SQLModel, table=True):
    __tablename__ = "sales"
    
    id: int = Field(primary_key=True)
    product_id: int = Field(default=None, foreign_key="products.id")
    client_id: int = Field(default=None, foreign_key="clients.id")
    sale_date: datetime = Field(default_factory=datetime.now)
    delivery_date: datetime = Field(default=None,)
    quantity: Decimal = Field(default=None, max_digits=10, decimal_places=3)
    
    # Relationships
    product: Product = Relationship(back_populates="sales")
    client: Client = Relationship(back_populates="sales")
