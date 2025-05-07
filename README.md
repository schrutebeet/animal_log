# Animal Log :dog::cat:

Animal Log is a web-based application designed to manage veterinary records, including animal registration, appointment scheduling, and species inventory. It is built using FastAPI, SQLAlchemy, and Jinja2 for a robust and user-friendly experience.

## Features

- **User authentication**: Secure user registration and login using hashed passwords.
- **Animal management**:
  - Register new animals with details like name, owner, species, birth date, and weight.
  - Edit existing animal records.
  - Search for animals by name.
  - View detailed animal records, including age and weight.
  - View and manage vaccines and their due dates.
- **Species inventory**:
  - Autocomplete functionality for species names during animal registration and editing.
  - Automatically add new species to the inventory if not already present.
- **Appointment management**:
  - Schedule appointments for animals with veterinarians.
  - View upcoming appointments for the next six months in a calendar format.
- **Dynamic HTML templates**: Responsive and user-friendly UI built with Jinja2 and Tailwind CSS.

## Project structure

```bash
animal_log/ 
├── app/ 
│ ├── animals.py # Routes for animal management 
│ ├── appointments.py # Routes for appointment management 
│ ├── auth.py # Routes for user authentication 
│ ├── database.py # Database connection and session management 
│ ├── main.py # Application entry point 
│ ├── models.py # SQLAlchemy ORM models 
│ ├── schemas.py # Pydantic models for data validation 
│ ├── templates/ # HTML templates for the UI 
│ ├── utilities/ 
│ │ └── utils.py # Utility functions 
│ └── static/ # Static files (CSS, JS, images) 
├── credentials.py # Database credentials (excluded from version control) 
├── pyproject.toml # Project dependencies and metadata 
├── poetry.lock # Dependency lock file 
├── README.md # Project documentation 
└── .gitignore # Git ignore rules
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/animal_log.git
   cd animal_log

2. **Set up a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**: Install dependencies using Poetry:
```bash
poetry install
```

4. **Configure database**: Create a credentials.py file in the root directory with the following content:
```bash
username = "your_db_username"
password = "your_db_password"
host = "your_db_host"
database = "your_db_name"
poetry install
```

5. **Run the application**: Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

6. **Access the application**: Open your browser and navigate to whatever url your server points to (usually http://127.0.0.1:8000).


 ## Usage

- **Sign up**: Create a new user account at /signup.
- **Log in**: Log in to access the dashboard at /login.
- **Animal management**:
    - Register a new animal at `/animals/new`.
    - Search for animals at `/animals/search`.
    - View animal details at `/animals/{animal_id}`.
    - Edit animal records at `/animals/{animal_id}/edit`.
- **Appointment management**:
    - Schedule appointments at `/appointments/manage/{animal_id}`.
    - View upcoming appointments in the animal detail page.


## Technologies used

- **Backend**: FastAPI, SQLAlchemy
- **Frontend**: Jinja2, Tailwind CSS
- **Database**: PostgreSQL
- **Authentication**: Passlib with bcrypt
- **Session Management**: Starlette's SessionMiddleware

## Future development
### Improve current UI design
- **Improve colors**: Improve colors in general, i.e., for buttons, bars, calendars, etc. 

### Animal managment enhancements
- **Medical history timeline**: Show past appointments, diagnoses, treatments, and notes in a vertical timeline or collapsible list.
- **File uploads for animals**: Allow uploading PDFs/images (e.g. x-rays, lab results, adoption papers).

### Appointments and calendar features
- **Click on dates for appointments** (maybe): Make calendar days clickable to open a modal/form to schedule an appointment directly.
- **Recurring appointments**: Allow setting a recurring check-up schedule (e.g., every 3 weeks).
- **Colored icons by type**: Use different colors or icons for vaccination, grooming, surgery, etc.
- **Appointment filtering**: Add filters to view appointments by type, vet, or urgency.

### Notifications and reminders
- **Email reminders**: Notify owners automatically a few days before upcoming appointments.
- **In-app alerts**: Banner or drop-down alerts for upcoming appointments, overdue checkups, etc.

### Search and usability
- **Animal search and filtering**: Allow users to search/filter animals not only by name, but also by owner, species, age range, etc.

### Reporting and analytics
- **Appointment statistics dashboard**: View graphs of number/type of appointments per month, no-shows, common species, etc.
- **Vet workload overview**: Which vet is booked how often, upcoming schedules's deistributions, etc (only for admin users).

### User Roles and permissions
 - **Admin, vet and other roles**: Differentiate between different roles, both database and app-wise.
