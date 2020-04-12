import pyspark.sql.functions as func
from pyspark.sql import SparkSession
from pyspark.sql.window import Window

N = 5
movies_file = "hdfs:///user/zeppelin/sparkDF/input/movies.csv"
ratings_file = "hdfs:///user/zeppelin/sparkDF/input/ratings.csv"
output_dir = "hdfs:///user/zeppelin/sparkDF/output"
spark = SparkSession.builder.appName("pyspark-topN-movies(DF)").getOrCreate()


def blank_as_null(x):
    return func.when(func.col(x) != "", func.col(x)).otherwise(None)


movies_df = spark.read.format("csv").options(header="true").load(movies_file)
ratings_df = spark.read.format("csv").options(header="true").load(ratings_file)

movies_normalized_df = movies_df.select(
    movies_df.movieId,
    func.regexp_extract(
        movies_df.title, '(.+)[ ]+[(](\\d{4})[)]', 1).alias('title'),
    func.regexp_extract(
        movies_df.title, '(.+)[ ]+[(](\\d{4})[)]', 2).alias('year'),
    func.explode(
        func.split(movies_df.genres, '\\|')).alias('genre')) \
    .withColumn(
    "title", blank_as_null("title")) \
    .withColumn(
    "year", blank_as_null("year")) \
    .dropna()

ratings_normalized_df = ratings_df.groupBy("movieId") \
    .agg({"rating": "mean"}) \
    .withColumnRenamed("avg(rating)", "avg_rating")
ratings_normalized_df = ratings_normalized_df.withColumn(
    "avg_rating",
    func.round(ratings_normalized_df.avg_rating, 2)
)

joined_df = movies_normalized_df.join(ratings_normalized_df, "movieId",
                                      "inner") \
    .select("genre", "title", "year", "avg_rating")

window = Window.partitionBy(joined_df.genre).orderBy(
    joined_df.avg_rating.desc())

csv_df = joined_df.withColumn("rank", func.row_number().over(window))
csv_df = csv_df.filter(csv_df.rank <= N) \
    .sort("genre", "avg_rating", ascending=[1, 0]) \
    .drop("rank")

csv_df.repartition(1).write.csv(path=output_dir,
                                mode="overwrite",
                                sep=",",
                                header=True)
