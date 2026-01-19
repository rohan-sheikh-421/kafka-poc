from pyspark.sql.types import StructType, StringType, IntegerType

order_schema = (
    StructType()
    .add("order_id", StringType())
    .add("product_id", StringType())
    .add("quantity", IntegerType())
    .add("status", StringType())
)
