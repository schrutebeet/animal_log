# app/animals.py
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

# Defines what will be a set of routes under the /animals prefix
router = APIRouter(prefix="/animals")
# Initializes the template engine for rendering HTML files located in app/templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/search/autocomplete")
def species_autocomplete(query: str = Query(...), db: Session = Depends(get_db)):
    # Return a JSON list of matching species for autocomplete
    results = db.query(models.InventorySpecies).filter(models.InventorySpecies.common_name.ilike(f"%{query}%")).all()
    names = [r.common_name for r in results]
    return JSONResponse(content=names)

def login_required(request: Request):
    # Helper to ensure user is logged in
    if not request.session.get("user"):
        return False
    return True

@router.get("/new", response_class=HTMLResponse)
def register_animal_get(request: Request):
    # Show animal registration form
    if not login_required(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("register_animal.html", {"request": request})

@router.post("/new", response_class=HTMLResponse)
def register_animal_post(
    request: Request,
    name: str = Form(...),
    owner: str = Form(...),
    species: str = Form(...),
    age: int = Form(default=None),
    weight: float = Form(default=None),
    db: Session = Depends(get_db)
):
    if not login_required(request):
        return RedirectResponse("/login")
    # Find or create species entry
    species_obj = db.query(models.InventorySpecies).filter(models.InventorySpecies.common_name.ilike(species)).first()
    if not species_obj:
        # Create new species if not found
        species_obj = models.InventorySpecies(common_name=species)
        db.add(species_obj)
        db.commit()
        db.refresh(species_obj)
    # Create Animal record
    animal = models.Animal(
        name=name,
        owner=owner,
        age=age,
        weight=weight,
        species_id=species_obj.id
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)
    # Redirect to detail view of the new animal
    return RedirectResponse(f"/animals/{animal.id}", status_code=303)

@router.get("/search", response_class=HTMLResponse)
def search_animal_get(request: Request, name: str | None = None, db: Session = Depends(get_db)):
    # Show search form; if 'name' query param is provided, perform search
    if not login_required(request):
        return RedirectResponse("/login")
    animals = None
    if name:
        # Search by partial match (case-insensitive)
        animals = db.query(models.Animal).filter(models.Animal.name.ilike(f"%{name}%")).all()
    return templates.TemplateResponse("retrieve_animal.html", {"request": request, "animals": animals})

@router.get("/{animal_id}", response_class=HTMLResponse)
def animal_detail(request: Request, animal_id: int, db: Session = Depends(get_db)):
    # Display animal details
    if not login_required(request):
        return RedirectResponse("/login")
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        return HTMLResponse(request.app.template_response("retrieve_animal.html", {"request": request, "error": "Animal not found"}))
    return templates.TemplateResponse("animal_detail.html", {"request": request, "animal": animal})

@router.get("/{animal_id}/edit", response_class=HTMLResponse)
def edit_animal_get(request: Request, animal_id: int, db: Session = Depends(get_db)):
    # Show edit form pre-filled with animal data
    if not login_required(request):
        return RedirectResponse("/login")
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        return RedirectResponse("/animals/search")
    return templates.TemplateResponse("edit_animal.html", {"request": request, "animal": animal})

@router.post("/{animal_id}/edit", response_class=HTMLResponse)
def edit_animal_post(
    request: Request,
    animal_id: int,
    name: str = Form(...),
    owner: str = Form(...),
    species: str = Form(...),
    age: int = Form(default=None),
    weight: float = Form(default=None),
    db: Session = Depends(get_db)
):
    # Handle updates to the animal record
    if not login_required(request):
        return RedirectResponse("/login")
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        return RedirectResponse("/animals/search")
    # Update fields
    animal.name = name
    animal.owner = owner
    animal.age = age
    animal.weight = weight
    # Update species if changed (find or create)
    species_obj = db.query(models.InventorySpecies).filter(models.InventorySpecies.common_name.ilike(species)).first()
    if not species_obj:
        species_obj = models.InventorySpecies(common_name=species)
        db.add(species_obj)
        db.commit()
        db.refresh(species_obj)
    animal.species_id = species_obj.id
    db.commit()
    return RedirectResponse(f"/animals/{animal.id}", status_code=303)
