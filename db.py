from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Import Base from your models.py

# Update the DATABASE_URL with your PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:first@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Tables created successfully.")
