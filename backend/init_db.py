"""
Script to initialize the database and create all tables
Run this once to set up the database schema
"""
from app.db.base import Base
from app.db.session import engine
from sqlalchemy import text, inspect
from app import models  

# Check if tables already exist
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

# Create all tables only if they don't exist
if not existing_tables:
    Base.metadata.create_all(bind=engine)
    
    # Reset sequences to 1 only on first creation
    with engine.connect() as connection:
        connection.execute(text("ALTER SEQUENCE movies_id_seq RESTART WITH 1"))
        connection.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        connection.execute(text("ALTER SEQUENCE reviews_id_seq RESTART WITH 1"))
        connection.execute(text("ALTER SEQUENCE watchlists_id_seq RESTART WITH 1"))
        connection.commit()
    
    print("Database tables created successfully!")
    print("Sequences reset to 1")
else:
    print("Database tables already exist - skipping creation")

