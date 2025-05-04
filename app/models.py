# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# Define your models here using SQLAlchemy ORM
# Each model corresponds to a table in the database
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "credentials"}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

class InventorySpecies(Base):
    __tablename__ = "species_inventory"
    __table_args__ = {"schema": "animals"}
    id = Column(Integer, primary_key=True, index=True)
    common_name = Column(String(100), unique=True, nullable=False)
    # This relationship allows you to access all animals of a species
    # through the species object. E.g., species.animals
    # This is a one-to-many relationship: one species can have many animals.
    animals = relationship("Animal", back_populates="species")

class Animal(Base):
    __tablename__ = "animals"
    __table_args__ = {"schema": "animals"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    # Foreign key to the inventory of species
    species_id = Column(Integer, ForeignKey("animals.species_inventory.id"))

    species = relationship("InventorySpecies", back_populates="animals")
