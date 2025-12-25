import sys
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

sys.path.append(str(Path(__file__).parent.parent))

DATABASE_URL = "jdbc:postgresql://localhost:5433/book_recommender"
DB_PROPERTIES = {
    "user": "bookuser",
    "password": "bookpass",
    "driver": "org.postgresql.Driver"
}

def create_spark_session():

    spark = SparkSession.builder.appName("book_recommender").master("local[*]").config("spark.jars.packages", "org.postgresql:postgresql:42.6.0").getOrCreate()

    return spark

def load_ratings(spark):

    return spark.read.jdbc(url=DATABASE_URL, table="ratings", properties=DB_PROPERTIES)

def train_als_model(ratings_df):

    train_df, test_df = ratings_df.randomSplit([0.8,0.2], seed=42)

    als = ALS(
        userCol="user_id",
        itemCol="book_id",
        ratingCol="rating",
        rank=20,
        maxIter=20,
        regParam=0.01,
        coldStartStrategy="drop"
    )

    model = als.fit(train_df)
    predictions = model.transform(test_df)

    evaluator = RegressionEvaluator(predictionCol="prediction",  labelCol="rating", metricName="rmse")

    rmse = evaluator.evaluate(predictions)

    print(f'Rmse: {rmse}')


    return model

def save_model(model):

    model_path = Path(__file__).parent.parent / "models" / "als_model"
    
    model.save(str(model_path))






if __name__ == "__main__":

    print("Starting model training...")

    spark = create_spark_session()
    ratings_df = load_ratings(spark)

    model = train_als_model(ratings_df)

    save_model(model)

    ratings_df.show(5)

    spark.stop()