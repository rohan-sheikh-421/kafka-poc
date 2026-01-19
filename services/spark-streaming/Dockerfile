FROM apache/spark:3.5.0

WORKDIR /app

COPY app/ /app/

CMD ["spark-submit", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.3", \
     "/app/spark_kafka_reader.py"]
