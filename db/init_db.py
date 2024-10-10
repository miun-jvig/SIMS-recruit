from db.db import engine
from db.db_base import Base

# Create tables in db if it is not already made
Base.metadata.create_all(bind=engine)
