import src.utils.utils as utils
from pyspark.sql import SparkSession
import pyspark.sql.functions as sf

def main():
    spark = SparkSession.builder.appName('raw_stage')\
        .config("spark.sql.files.ignoreCorruptFiles", "true")\
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .enableHiveSupport()\
        .getOrCreate()
    
    last_filie = utils.get_recent_file('stagged-soybean-gp4-sptech')    
    df = spark.read.csv(f's3://stagged-soybean-gp4-sptech/{last_filie}', header=True)
    df = df.withColumn('temperature', )

    df_npk = df.select(df.device_id,df.n,df.p,df.k,df.setor)
    df_npk = df_npk.withColumnRenamed('n','nitrogen')
    df_npk = df_npk.withColumnRenamed('p','phosphorus')
    df_npk = df_npk.withColumnRenamed('k','potassium')
    df_npk.write.csv(f"s3://consumed-soybean-gp4-sptech/npk/{last_filie}.csv", header=True, mode="overwrite")
    df_npk.unpersist()

    df_bmp = df.select(df.device_id,df.temperature,df.pressure,df.setor)
    df_bmp.write.csv(f"s3://consumed-soybean-gp4-sptech/bmp/{last_filie}.csv", header=True, mode="overwrite")
    df_bmp.unpersist()

    df_anemometro = df.select(df.device_id,sf.col('air-speed'),df.setor)
    df_anemometro.write.csv(f"s3://consumed-soybean-gp4-sptech/anemometro/{last_filie}.csv", header=True, mode="overwrite")
    df_anemometro.unpersist()

    df_dht = df.select(df.device_id,df.temperature,df.humidity,df.setor)
    df_dht.write.csv(f"s3://consumed-soybean-gp4-sptech/dht/{last_filie}.csv", header=True, mode="overwrite")
    df_dht.unpersist()

    df_tcrt = df.select(df.device_id,df.capacity,df.collected, df.setor)
    df_tcrt.write.csv(f"s3://consumed-soybean-gp4-sptech/tcrt/{last_filie}.csv", header=True, mode="overwrite")
    df_tcrt.unpersist()

    df_umigrain = df.select(df.device_id,df.humidity_grain, df.setor)
    df_umigrain.write.csv(f"s3://consumed-soybean-gp4-sptech/umigrain/{last_filie}.csv", header=True, mode="overwrite")
    df_umigrain.unpersist()

if __name__ == "__main__":
    main()
    
