from datetime import date
from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app import models
from app.database import get_db

def calculate_age(birth_date):
    today = date.today()
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    if today.day < birth_date.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12
    return years, months

def login_required(request: Request):
    # Helper to ensure user is logged in
    if not request.session.get("user"):
        return False
    return True

def execute_previous_security_checks(request: Request, db: Session, animal_id: int):
    # Check if the user is logged in and if the animal exists
    if not login_required(request):
        return RedirectResponse("/login")
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        return RedirectResponse("/animals/search")
    return animal