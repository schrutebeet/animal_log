# Animal Logger :dog::tiger:

Animal Logger is a Python-based application designed to manage and log information about animals. It provides a graphical user interface (GUI) built with `customtkinter` for user interaction, and it integrates with a PostgreSQL database for storing and retrieving animal-related data.


## Features

- **Login System**: A secure login page that validates user credentials against a database.
- **Dashboard**: A user-friendly dashboard with navigation options for managing records.
- **Animal Management**: Add, view, and manage animal records categorized by classes (e.g., mammals, birds, reptiles).
- **Database Integration**: Uses SQLAlchemy for database interactions, including dynamic model creation and data insertion.
- **Customizable UI**: The application uses `customtkinter` for a modern and customizable interface.
- **Logging**: Comprehensive logging for debugging and monitoring.


## Project Structure
animal-logger/ 
├── animal_logger/ 
│ ├── opt/ 
│ │ └── img/ # Contains images used in the UI 
│ ├── src/ 
│ │ ├── animals/ # Animal-related classes (e.g., BaseAnimal, Mammal) 
│ │ ├── db/ # Database utilities and connection setup 
│ │ ├── frames/ # GUI frames (e.g., LoginPage, Dashboard, AddAnimal) 
│ │ ├── main.py # Entry point of the application 
│ └── __init__.py 
├── config/ 
│ ├── app_config.yaml # Application-specific configurations 
│ ├── db_config.yaml # Database connection configurations 
│ ├── config.py # Configuration loader 
│ ├── log_config.py # Logging configuration 
│ └── __init__.py 
├── tests/ # Placeholder for unit tests 
├── .gitignore # Git ignore rules 
├── poetry.lock # Poetry lock file for dependencies 
├── pyproject.toml # Poetry configuration file 
└── README.md # Project documentation


## Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- Poetry (for dependency management)

### Steps

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd animal-logger
   poetry install
   # Set up environment variables for database credentials 
   export USERNAME=<your-db-username>
   export PASSWORD=<your-db-password>
   export LOGS_PATH=<path-to-log-directory>
   # Run the application
   poetry run python animal_logger/src/main.py
   ```

## Usage
**Login**: Enter your username and password to log in.
**Dashboard**: Navigate through the sidebar to manage animal records.
**Add Animal**: Use the "Create record" button to add new animal entries.

## Usage
**Login**: Enter your username and password to log in.
**Dashboard**: Navigate through the sidebar to manage animal records.
**Add Animal**: Use the "Create record" button to add new animal entries.
