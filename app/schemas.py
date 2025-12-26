from pydantic import BaseModel


# Need to define response models (what data structure  the api returns)



class BookResponse(BaseModel):

    book_id: int
    title: str
    authors: str
    average_rating: float
    image_url: str


    class Config:
        # Allows SQLAlchemy models to work with pydantic
        from_attributes = True

class RecommendationResponse(BaseModel):

    book_id: int
    title: str
    authors: str
    predicted_rating: float
    image_url: str

    class Config:
        # Allows SQLAlchemy models to work with pydantic
        from_attributes = True
