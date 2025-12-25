from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)

class Books(Base):

    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = Column(String)
    average_rating = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    isbn = Column(String, nullable=True)

class Ratings(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    rating = Column(Integer)