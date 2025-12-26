from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Books
from app.schemas import BookResponse
from typing import List



router = APIRouter(prefix="/books", tags=["books"])



@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):

    books = db.query(Books).all()

    if not books:
        raise HTTPException(status_code=404, detail="Error: No Books Found")
    
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):


    book = db.query(Books).filter(Books.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Error: Book Not Found")

    
    return book



