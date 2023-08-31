import boto3
import os
import src.utils.utils as utils
import pyspark.sql.functions as sf
from pyspark.sql import SparkSession

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
    
    last_filie = utils.get_recent_file('stagged-soybean-gp4-sptech')
       
    df = spark.read.parquet(f's3a://stagged-soybean-gp4-sptech/{last_filie}', header=True)

    df_npk = df.select(df.device_id,df.n,df.p,df.k,df.setor)
    df_npk = df_npk.withColumnRenamed('n','nitrogen')
    df_npk = df_npk.withColumnRenamed('p','phosphorus')
    df_npk = df_npk.withColumnRenamed('k','potassium')
    df_npk.write.parquet(f"s3a://consumed-soybean-gp4-sptech/npk/", mode="overwrite")
    df_npk.unpersist()

    df_bmp = df.select(df.device_id,df.temperature,df.pressure,df.setor)
    df_bmp.write.parquet(f"s3a://consumed-soybean-gp4-sptech/bmp/", mode="overwrite")
    df_bmp.unpersist()

    df_anemometro = df.select(df.device_id,sf.col('air-speed'),df.setor)
    df_anemometro.write.parquet(f"s3a://consumed-soybean-gp4-sptech/anemometro/", mode="overwrite")
    df_anemometro.unpersist()

    df_dht = df.select(df.device_id,df.temperature,df.humidity,df.setor)
    df_dht.write.parquet(f"s3a://consumed-soybean-gp4-sptech/dht/", mode="overwrite")
    df_dht.unpersist()

    df_tcrt = df.select(df.device_id,df.capacity,df.collected, df.setor)
    df_tcrt.write.parquet(f"s3a://consumed-soybean-gp4-sptech/tcrt/", mode="overwrite")
    df_tcrt.unpersist()

    df_umigrain = df.select(df.device_id,df.humidity_grain, df.setor)
    df_umigrain.write.parquet(f"s3a://consumed-soybean-gp4-sptech/umigrain/", mode="overwrite")
    df_umigrain.unpersist()

if __name__ == "__main__":
    main()
    
