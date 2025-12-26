# Book Recommendation System

A machine learning-powered book recommendation API built with FastAPI, PostgreSQL, and Apache Spark.

## Features
- **Collaborative filtering** using Spark MLlib ALS algorithm
- **10,000 books** from Goodreads dataset
- **100,000 user ratings** for model training
- **REST API** serving personalized recommendations

## Tech Stack
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL (Docker)
- **ML**: Apache Spark (ALS collaborative filtering)
- **ORM**: SQLAlchemy

## API Endpoints
- `GET /books` - List all books (paginated)
- `GET /books/{book_id}` - Get book details
- `GET /recommendations/{user_id}` - Get top 10 personalized recommendations

## Model Performance
- **RMSE**: 1.37 on test set
- **Training data**: 80,000 ratings (80% split)
- **Test data**: 20,000 ratings (20% split)

## Local Setup
```bash
# Start database
docker-compose up -d postgres

# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn app.main:app --reload
```

## Example Response
```json
GET /recommendations/1
[
  {
    "book_id": 1031,
    "title": "A Moveable Feast",
    "authors": "Ernest Hemingway",
    "predicted_rating": 5.45,
    "image_url": "https://..."
  }
]
```