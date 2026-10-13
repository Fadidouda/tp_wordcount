"""Spark RDD : transposition directe du modèle MapReduce."""
import sys
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("wordcount_rdd").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    comptes = (spark.sparkContext.textFile(sys.argv[1])
               .flatMap(lambda ligne: ligne.split())   # map : une ligne -> ses mots
               .map(lambda mot: (mot, 1))               # paires (mot, 1)
               .reduceByKey(lambda a, b: a + b)         # combine local + shuffle + reduce
               .collect())

    for mot, nb in sorted(comptes, key=lambda x: x[1], reverse=True):
        print(f"{mot} : {nb}")
    spark.stop()
