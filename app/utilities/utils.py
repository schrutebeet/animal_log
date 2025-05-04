from datetime import date
from fastapi import Request, Form

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
