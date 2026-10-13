"""Spark DataFrame : API déclarative, optimisée par Spark."""
import sys
from pyspark.sql import SparkSession, functions as F

if __name__ == "__main__":
    spark = SparkSession.builder.appName("wordcount_df").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    comptes = (spark.read.text(sys.argv[1])
               .select(F.explode(F.split(F.col("value"), r"\s+")).alias("mot"))
               .where(F.col("mot") != "")
               .groupBy("mot").count()
               .collect())

    for ligne in sorted(comptes, key=lambda r: r["count"], reverse=True):
        print(f"{ligne['mot']} : {ligne['count']}")
    spark.stop()
