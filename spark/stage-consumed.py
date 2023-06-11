import src.utils.utils as utils
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName('raw_stage')\
        .config("spark.sql.files.ignoreCorruptFiles", "true")\
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .enableHiveSupport()\
        .getOrCreate()
    
    last_filie = utils.get_recent_file('stagged-sprint-3')    
    df = spark.read.csv(f's3://stagged-sprint-3/{last_filie}', header=True)

    df_npk = df.select(df.n,df.p,df.k,df.date)
    df_npk = df_npk.withColumnRenamed('n','nitrogen')
    df_npk = df_npk.withColumnRenamed('p','phosphorus')
    df_npk = df_npk.withColumnRenamed('k','potassium')
    df_npk.write.csv(f"consumed/npk/{last_filie}.csv", header=True, mode="overwrite")
    df_npk.unpersist()

    df_bmp = df.select(df.temp,df.press,df.date)
    df_bmp = df_bmp.withColumnRenamed('temp','temperature')
    df_bmp = df_bmp.withColumnRenamed('press','pressure')
    df_bmp.write.csv(f"consumed/bmp/{last_filie}.csv", header=True, mode="overwrite")
    df_bmp.unpersist()

    df_anemometro = df.select(df.var,df.date)
    df_anemometro = df_anemometro.withColumnRenamed('var', 'air_speed')
    df_anemometro.write.csv(f"consumed/anemometro/{last_filie}.csv", header=True, mode="overwrite")
    df_anemometro.unpersist()

    df_dht = df.select(df.temp,df.humi,df.date)
    df_dht = df_dht.withColumnRenamed('temp','temperature')
    df_dht = df_dht.withColumnRenamed('humi','humidity')
    df_dht.write.csv(f"consumed/dht/{last_filie}.csv", header=True, mode="overwrite")
    df_dht.unpersist()

    df_tcrt = df.select(df.caps,df.qtdg)
    df_tcrt = df_tcrt.withColumnRenamed('caps','capacity')
    df_tcrt = df_tcrt.withColumnRenamed('qtdg','collected')
    df_tcrt.write.csv(f"consumed/tcrt/{last_filie}.csv", header=True, mode="overwrite")
    df_tcrt.unpersist()

    df_umigrain = df.select(df.umig,df.date)
    df_umigrain = df_umigrain.withColumnRenamed('umig','humidity_grain')
    df_umigrain.write.csv(f"consumed/umigrain/{last_filie}.csv", header=True, mode="overwrite")
    df_umigrain.unpersist()

if __name__ == "__main__":
    main()
    