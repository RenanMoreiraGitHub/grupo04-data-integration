import os
import boto3
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

BUCKET = 'raw-soybean-gp4-sptech'

def get_recent_file(bucket_name):
    s3 = boto3.client('s3')
    arquivos = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    return max(arquivos, key=lambda x: x['LastModified'])['Key']


def main():
    chave_id = boto3.session.Session().get_credentials().access_key
    secret_id = boto3.session.Session().get_credentials().secret_key
    token = boto3.session.Session().get_credentials().token

    os.environ["AWS_ACCESS_KEY_ID"]=chave_id
    os.environ["AWS_SECRET_ACCESS_KEY"]=secret_id
    os.environ["AWS_SESSION_TOKEN"]=token
    os.environ["AWS_DEFAULT_REGION"]='us-east-1'

    spark = SparkSession.builder.appName('app_name') \
        .config("spark.jars.packages", "com.amazonaws:aws-java-sdk-bundle:1.11.271,org.apache.hadoop:hadoop-aws:3.1.2") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider") \
        .config("fs.s3a.access.key", chave_id)\
        .config("fs.s3a.secret.key", secret_id)\
        .config("fs.s3a.secret.session.token", token)\
        .enableHiveSupport() \
        .getOrCreate()
    
    last_filie = get_recent_file(BUCKET)
        
    s3 = boto3.resource('s3')
    try:
       s3.meta.client.download_file(BUCKET, last_filie,last_filie)
    except Exception as e:
        print(e)
        raise "ERROR GETTING OBJECT."

    with open(f'./{last_filie}', "r") as f:
        file_content = f.read()
        
    file_content = json.loads(file_content)

    schema = StructType([StructField("device_id", StringType(), nullable=True),
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
                         StructField("batery", DoubleType(), nullable=True),
                         StructField("setor", StringType(), nullable=True),
                         StructField("data_hora", StringType(), nullable=True)])
    
    data = [(file_content['device_id'], file_content['device_name'], 
             file_content['temperature'], file_content['pressure'], 
             file_content['air-speed'], file_content['n'], file_content['p'], 
             file_content['k'], file_content['humidity'], file_content['capacity'], 
             file_content['collected'], file_content['humidity_grain'],
             file_content['batery'], file_content['setor'], file_content['data_hora'])]

    rdd = spark.sparkContext.parallelize(data)

    df = spark.createDataFrame(rdd, schema=schema)    
    print(df.show(n=3))
       
    df = df.coalesce(1)
    df.write.parquet(f"s3a://stagged-soybean-gp4-sptech/sensors/", mode="overwrite")
    
if __name__ == "__main__":
    main()
    

