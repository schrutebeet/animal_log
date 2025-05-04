import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app import models
from app.database import get_db
from app.utilities.utils import login_required

router = APIRouter(prefix="/appointments")
templates = Jinja2Templates(directory="app/templates")

@router.get("/search", response_class=HTMLResponse)
def search_animal_get(request: Request, name: str | None = None, db: Session = Depends(get_db)):
    # Show search form; if 'name' query param is provided, perform search
    if not login_required(request):
        return RedirectResponse("/login")
    animals = None
    if name:
        # Search by partial match (case-insensitive)
        animals = db.query(models.Animal).filter(models.Animal.name.ilike(f"%{name}%")).all()
    return templates.TemplateResponse("retrieve_animal.html", {"request": request, "animals": animals, "router_name": "/appointments"})

@router.get("/manage/{animal_id}", response_class=HTMLResponse)
def manage_appointments_get(request: Request, animal_id: int, db: Session = Depends(get_db)):
    # Show appointments management page
    if not login_required(request):
        return RedirectResponse("/login")
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        return RedirectResponse("/animals/search")
    specific_appointment = db.query(models.Appointments).filter(models.Appointments.animal_id == animal_id).all()
    return templates.TemplateResponse("manage_appointments.html", {"request": request, "animal": animal})
    
@router.post("/manage/{animal_id}", response_class=HTMLResponse)
def manage_appointments_post(
    request: Request,
    animal_id: int,
    veterinarian: str = Form(...),
    date: datetime.date = Form(...),
    time: datetime.time = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):   
    new_appointment = models.Appointments(
        animal_id=animal_id,
        veterinarian=veterinarian,
        date=date,
        time=time,
        description=description
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    
    return RedirectResponse(f"/appointments/manage/{animal_id}", status_code=303)


def get_appointments_by_animal_id(db: Session, animal_id: int) -> dict[datetime.date, str]:
    # Fetch appointments for a specific animal
    # Get appointments in the next 6 months
    today = datetime.date.today()
    in_six_months = today + datetime.timedelta(days=180)
    appointments = db.query(models.Appointments).filter(
        models.Appointments.animal_id == animal_id,
        models.Appointments.date >= today,
        models.Appointments.date <= in_six_months
    ).all()

    appointments = {a.date.isoformat(): a.description for a in appointments}

    return appointments