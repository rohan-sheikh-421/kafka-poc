# services/spark-streaming/app/spark_kafka_reader.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from schemas import order_schema
from config import KAFKA_BOOTSTRAP_SERVERS, ORDER_TOPIC

spark = (
    SparkSession.builder
    .appName("OrderKafkaStreaming")
    .getOrCreate()
)

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", ORDER_TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)

parsed = (
    df.selectExpr("CAST(value AS STRING)")
      .select(from_json(col("value"), order_schema).alias("data"))
      .select("data.*")
)

query = (
    parsed.writeStream
    .format("console")
    .outputMode("append")
    .start()
)

query.awaitTermination()
