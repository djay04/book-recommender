from fastapi import APIRouter, Depends, HTTPException
from app.models import Users, Ratings, Books
from app.schemas import RecommendationResponse
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List, Dict
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALSModel
from fastapi import Request
from pyspark.sql.functions import col, explode



router = APIRouter(prefix="/recommendations", tags=["ratings"])



@router.get("/{user_id}", response_model=List[RecommendationResponse])
def get_recommendations(user_id: int, request: Request, db: Session = Depends(get_db)):

    exists = db.query(Users).filter(Users.user_id == user_id).first()

    if not exists:
        raise HTTPException(status_code=404, detail="Error: Could not find user")
    
    model = request.app.state.model

    spark = request.app.state.spark

    data = [(user_id,)]
    columns = ["user_id"]

    spark_df = spark.createDataFrame(data, columns)
    user_recs = model.recommendForUserSubset(spark_df, 10)

    exploded = user_recs.select(explode(col("recommendations")).alias("rec"))

    extracted = exploded.select(
        col("rec.book_id").alias("book_id"),
        col("rec.rating").alias("predicted_ratings")
    )

    recs_list = extracted.collect()

    book_ids = [row.book_id for row in recs_list]


    books_from_db = db.query(Books).filter(Books.book_id.in_(book_ids)).all()

    books_to_ratings = {row.book_id: row.predicted_ratings for row in recs_list}
    
    recommendations = []

    for book in books_from_db:
        predicted_rating = books_to_ratings[book.book_id]

        rec = RecommendationResponse(
            book_id = book.book_id,
            title = book.title,
            authors = book.authors,
            predicted_rating = predicted_rating,
            image_url = book.image_url
        )

        recommendations.append(rec)

    return recommendations



    
    




