import boto3
import json
import pandas as pd
import awswrangler as wr

BUCKET = "raw-soybean-bucket"


def get_recent_file(bucket_name):
    s3 = boto3.client("s3")
    arquivos = s3.list_objects_v2(Bucket=bucket_name)["Contents"]
    return max(arquivos, key=lambda x: x["LastModified"])["Key"]


def main(event, context):
    print("INFO: Getting recent files")
    last_file = get_recent_file(BUCKET)

    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=BUCKET, Key=last_file)
    file_content = response["Body"].read().decode("utf-8")

    print("INFO: Creating dataframe")
    file_content = json.loads(file_content)
    df = pd.DataFrame([file_content])
    df = df.round(2)
    print(df.head(n=3))

    wr.s3.to_parquet(
        df=df, path="s3://staged-soybean-bucket/sensors/", mode="append", dataset=True
    )
