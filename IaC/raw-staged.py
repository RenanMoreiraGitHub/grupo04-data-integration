import boto3
import json
import pandas as pd
import awswrangler as wr

BUCKET = 'raw-soybean-gp4-sptech'

def get_recent_file(bucket_name):
    s3 = boto3.client('s3')
    arquivos = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    return max(arquivos, key=lambda x: x['LastModified'])['Key']

def main():
    print('INFO: Getting recent files')
    last_file = get_recent_file(BUCKET)
        
    s3 = boto3.resource('s3')
    try:
       s3.meta.client.download_file(BUCKET, last_file,last_file)
    except Exception as e:
        print(e)
        raise "ERROR GETTING OBJECT."
    
    with open(f'./{last_file}', "r") as f:
        file_content = f.read()
        
    print('INFO: Creating dataframe')
    file_content = json.loads(file_content)
    df = pd.DataFrame([file_content])
    print(df.head(n=3))

    wr.s3.to_parquet(
        df=df,
        path="s3a://stagged-soybean-gp4-sptech/sensors/", 
        mode="overwrite"
    )

if __name__ == '__main__':
    main()