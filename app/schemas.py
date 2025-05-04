# app/schemas.py
from pydantic import BaseModel

import datetime

# Define your Pydantic models. These models are used for data validation when receiving POST, PUT, etc requests.
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class AnimalBase(BaseModel):
    name: str
    owner: str
    #age can be int or None, with default value None
    # if None, it means age is optional
    birth: datetime.date | None = None
    weight: float | None = None

class AnimalCreate(AnimalBase):
    species: str  # common name of species

class AnimalUpdate(AnimalBase):
    species: str

class AnimalOut(AnimalBase):
    id: int
    species: str

class InventorySpeciesOut(BaseModel):
    id: int
    common_name: str

    class Config:
        orm_mode = True
