from  sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = "postgresql://bookuser:bookpass@localhost:5433/book_recommender"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


# Provide a database session to api endpoints, then automatically clean it up
def get_db():
    
    db = SessionLocal()

    try:
        # Give it to endpoint that needs it
        yield db
    finally:
        # Always close connection, even if there's an error
        db.close()