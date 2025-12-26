from fastapi import FastAPI
from app.routes.books import router as book_Router
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
from contextlib import asynccontextmanager
from pathlib import Path
from app.routes.recommendations import router as recommendations_router
import sys

@asynccontextmanager
async def load_recommendations(app: FastAPI):

    python_path = sys.executable

    spark = SparkSession.builder.appName("recommendations").master("local[*]").config("spark.pyspark.python", python_path).config("spark.pyspark.driver.python", python_path).getOrCreate()

    app.state.spark = spark

    saved_model = str(Path(__file__).parent.parent / "models" / "als_model")

    final_model = ALSModel.load(saved_model)

    app.state.model = final_model

    yield


app = FastAPI(lifespan=load_recommendations)
app.include_router(book_Router)
app.include_router(recommendations_router)



@app.get("/")
def root():

    return {"status": "good"}