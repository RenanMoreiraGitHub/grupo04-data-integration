import boto3
import awswrangler as wr


def get_recent_file(bucket_name):
    s3 = boto3.client('s3')
    arquivos = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    return max(arquivos, key=lambda x: x['LastModified'])['Key']

def main(event, context):
    print('INFO: Getting recent files')
    last_filie = get_recent_file('stagged-soybean-grp4-sptech')
    df = wr.s3.read_parquet(f's3://stagged-soybean-grp4-sptech/{last_filie}')
    df = df.round(2)

    print('INFO: Creating NPK table')
    df_npk = df[['device_id','device_name','n','p','k','setor','data_hora']]
    df_npk = df_npk.rename(columns={'n':'nitrogen',
                                    'p':'phosphorus',
                                    'k':'potassium'})
    wr.s3.to_parquet(df=df_npk,
                     path="s3://consumed-soybean-grp4-sptech/npk/", 
                     mode="overwrite",
                     dataset=True)
    del df_npk
    

    print('INFO: Creating BMP table')
    df_bmp = df[['device_id','device_name','temperature','pressure','setor','data_hora']]
    wr.s3.to_parquet(df=df_bmp,
                    path="s3://consumed-soybean-grp4-sptech/bmp/", 
                    mode="overwrite",
                    dataset=True)
    del df_bmp

    print('INFO: Creating ANEMOMETRO table')
    df_anemometro = df[['device_id','device_name','air-speed','setor','data_hora']]
    wr.s3.to_parquet(df=df_anemometro,
                     path="s3://consumed-soybean-grp4-sptech/anemometro/", 
                     mode="overwrite",
                     dataset=True)
    del df_anemometro

    print('INFO: Creating DHT table')
    df_dht = df[['device_id','device_name','temperature','humidity','setor','data_hora']]
    wr.s3.to_parquet(df=df_dht,
                     path="s3://consumed-soybean-grp4-sptech/dht/", 
                     mode="overwrite",
                     dataset=True)
    del df_dht

    print('INFO: Creating TCRT table')
    df_tcrt = df[['device_id','device_name','capacity','collected','setor','data_hora']]
    wr.s3.to_parquet(df=df_tcrt,
                     path="s3://consumed-soybean-grp4-sptech/tcrt/", 
                     mode="overwrite",
                     dataset=True)
    del df_tcrt

    print('INFO: Creating UMIGRAIN table')
    df_umigrain = df[['device_id','device_name','humidity_grain','setor','data_hora']]
    wr.s3.to_parquet(df=df_umigrain,
                     path="s3://consumed-soybean-grp4-sptech/umigrain/", 
                     mode="overwrite",
                     dataset=True)
    del df_umigrain
