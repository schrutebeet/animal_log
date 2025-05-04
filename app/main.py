# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app.database import engine, Base
from app.models import User, InventorySpecies, Animal
from app.auth import router as auth_router
from app.animals import router as animal_router

#App initialization
app = FastAPI()

# Create database tables on startup (for demonstration; in prod use migrations)
Base.metadata.create_all(bind=engine)

# Middleawres are useful to save session data in cookies
# and to use them in the app. E.g., shopping cart, language, dark mode...
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY_HERE")

# Tells FastAPI to serve files like CSS, logos, etc., from the folder app/static when a request is made to /static/
app.mount("/static", StaticFiles(directory=r"app\static"), name="static")

# Set up Jinja2 templates directory. Used to render dynamic HTML pages.
templates = Jinja2Templates(directory=r"app\templates")

# Include other routes besides the main one ("/").
# Essentially, we are adding the routes defined in auth.py and animals.py to the main app.
app.include_router(auth_router)
app.include_router(animal_router)

# Defines a route for "/" (the homepage).
@app.get("/", response_class=templates.TemplateResponse)
def landing(request: Request):
    # If the user is not logged in already (known thanks to the middleware), redirect to the login page.
    if not request.session.get("user"):
        # Use RedirectResponse to use **another route** that you already have.
        return RedirectResponse("/login")
    # Otherwise, render the landing page with the user data.
    #Use templates.TemplateResponse to render the HTML page (final output of the route).
    #What are the arguments to this method below?
    # 1. The name of the HTML file to render (in the templates folder).
    # 2. A dictionary with the objects that the HTML fille will need. IMPORTANT: The key "request" is mandatory, as it is used by FastAPI to render the HTML page.
    # 2 bis. The key "user" is used in the HTML file like "{{ user }}".
    return templates.TemplateResponse("landing.html", {"request": request, "user": request.session.get("user")})
