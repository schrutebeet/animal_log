vet_inventory_app/
├── app/
│   ├── main.py             # Application entry point (sets up app, routers, templates, etc.)
│   ├── database.py         # Database connection (SQLAlchemy engine, session)
│   ├── models.py           # SQLAlchemy ORM models (User, InventorySpecies, Animal)
│   ├── schemas.py          # Pydantic schemas for request/response models
│   ├── auth.py             # Authentication routes (signup, login, logout)
│   ├── animals.py          # Animal routes (register, search, detail, edit, autocomplete)
│   ├── templates/          # Jinja2 templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── landing.html
│   │   ├── register_animal.html
│   │   ├── retrieve_animal.html
│   │   ├── animal_detail.html
│   │   └── edit_animal.html
│   └── static/             # (Optional additional static assets; Tailwind is via CDN)
│       └── (images/css if needed)
└── requirements.txt        # Required Python packages (fastapi, sqlalchemy, etc.)
