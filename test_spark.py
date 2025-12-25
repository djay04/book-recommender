from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("SparkTest").master("local[*]").getOrCreate()

print(f'Spark version: {spark.version}')
print(f'Spark is running!')

data = [("Alice", 34), ("Bob", 45), ("Charlie", 29)]
df = spark.createDataFrame(data, ["Name", "Age"])
df.show()

spark.stop()