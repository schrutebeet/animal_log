from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.config import Config


# used to create a database engine
# the engine manages the database connection.
# The echo=True argument is optional and is often used for debugging purposes (turned off)
engine = create_engine(Config.get_info()['db_url'])

# used to create a models (tables) based on an object-oriented approach
Base = declarative_base()

# Manages information about the database schema
metadata = MetaData()

# used to manage database sessions for your application
SessionLocal = sessionmaker(bind=engine)