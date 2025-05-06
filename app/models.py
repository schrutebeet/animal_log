# app/models.py
from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
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
    animal = relationship("Animal", back_populates="species")

class Animal(Base):
    __tablename__ = "animals"
    __table_args__ = {"schema": "animals"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner = Column(String(100), nullable=False)
    birth = Column(Date, nullable=True)
    weight = Column(Float, nullable=False)
    # Foreign key to the inventory of species
    species_id = Column(Integer, ForeignKey("animals.species_inventory.id"))

    species = relationship("InventorySpecies", back_populates="animal")
    appointments = relationship("Appointments", back_populates="animal")
    vaccinations = relationship('Vaccination', back_populates='animal')

class Appointments(Base):
    __tablename__ = "appointments"
    __table_args__ = {"schema": "animals"}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animals.animals.id"), nullable=False)
    veterinarian = Column(String(100), ForeignKey("credentials.users.username"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    description = Column(String(255), nullable=True)

    animal = relationship("Animal", back_populates="appointments")

class Vaccination(Base):
    __tablename__ = "vaccinations"
    __table_args__ = {"schema": "animals"}
    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.animals.id'), nullable=False)
    vaccine_name = Column(String(100), nullable=False)
    date_administered = Column(Date, nullable=False)
    expiry_date = Column(Date)
    notes = Column(String(255))

    animal = relationship('Animal', back_populates='vaccinations')
