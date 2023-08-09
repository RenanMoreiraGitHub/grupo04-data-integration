import boto3
import re
import src.utils.utils as utils
import pyspark.sql.functions as sf
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
from pyspark.sql.functions import from_json

BUCKET = 'raw-soybean-gp4-sptech'

def main():
    spark = SparkSession.builder.appName('raw_stage')\
            .config("spark.sql.files.ignoreCorruptFiles", "true")\
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .enableHiveSupport()\
            .getOrCreate()
    
    last_filie = utils.get_recent_file(BUCKET)
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(BUCKET).download_file(last_filie, last_filie)
    except:
        raise "ERROR GETTING OBJECT."

    with open(f'./{last_filie}', "r") as f:
        file_content = f.read()
    
    schema = StructType([StructField("DeviceId", IntegerType(), nullable=True),
                         StructField("N", IntegerType(), nullable=True),
                         StructField("P", IntegerType(), nullable=True),
                         StructField("K", IntegerType(), nullable=True),
                         StructField("temp", DoubleType(), nullable=True),
                         StructField("humi", DoubleType(), nullable=True),
                         StructField("var", DoubleType(), nullable=True),
                         StructField("press", DoubleType(), nullable=True),
                         StructField("caps", IntegerType(), nullable=True),
                         StructField("qtdg", IntegerType(), nullable=True),
                         StructField("umig", DoubleType(), nullable=True),
                         StructField("batery", DoubleType(), nullable=True),
                         StructField("tema", StringType(), nullable=True)])
    
    df = spark.createDataFrame(file_content, StringType())
    df = df.select(from_json(df.value, schema).alias("data")).select("data.*")
    df = df.withColumn("Date", sf.lit(datetime.now().date()).cast(DateType()))
    
    print(df.show(n=3))

    last_filie = last_filie.replace(".json", "")
    df.write.csv(f"s3://stagged-soybean-gp4-sptech/{last_filie}.csv", header=True, mode="overwrite")

if __name__ == "__main__":
    main()
    