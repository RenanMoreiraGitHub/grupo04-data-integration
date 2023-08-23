import boto3
from pprint import pp
import re
import src.utils.utils as utils
import pyspark.sql.functions as sf
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
from pyspark.sql.functions import from_json

boto3.setup_default_session(profile_name='faculdade')

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
        s3.meta.client.download_file(BUCKET, last_filie,last_filie)
    except Exception as e:
        print(e)
        raise "ERROR GETTING OBJECT."

    with open(f'./{last_filie}', "r") as f:
        file_content = f.read()
    
    import json
    file_content = json.loads(file_content)

    print((file_content))

    schema = StructType([StructField("device_id", StringType(), nullable=False),
                         StructField("device_name", StringType(), nullable=True),
                         StructField("temperature", DoubleType(), nullable=True),
                         StructField("pressure", DoubleType(), nullable=True),
                         StructField("air-speed", DoubleType(), nullable=True),
                         StructField("n", IntegerType(), nullable=True),
                         StructField("p", IntegerType(), nullable=True),
                         StructField("k", IntegerType(), nullable=True),
                         StructField("humidity", DoubleType(), nullable=True),
                         StructField("capacity", DoubleType(), nullable=True),
                         StructField("collected", DoubleType(), nullable=True),
                         StructField("humidity_grain", DoubleType(), nullable=True),
                         StructField("batery", DoubleType(), nullable=True)])
    
    data = [(file_content['device_id'], file_content['device_name'], 
             file_content['temperature'], file_content['pressure'], 
             file_content['air-speed'], file_content['n'], file_content['p'], 
             file_content['k'], file_content['humidity'], file_content['capacity'], 
             file_content['collected'], file_content['humidity_grain'],
             file_content['batery'])]

    # Crie um RDD a partir da lista de tuplas
    rdd = spark.sparkContext.parallelize(data)

    df = spark.createDataFrame(rdd, schema=schema)    
    print(df.show(n=3))
       
    last_filie = last_filie.replace(".json", "")
    df.write.csv(f"s3a://stagged-soybean-gp4-sptech/{last_filie}.csv", header=True, mode="overwrite")
 
if __name__ == "__main__":
    main()
    

