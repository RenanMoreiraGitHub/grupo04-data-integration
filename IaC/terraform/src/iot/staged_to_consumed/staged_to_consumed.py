import boto3
import awswrangler as wr
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from logging import basicConfig, info, INFO

load_dotenv()


basicConfig(level=INFO)


class MysqlConnection:
    def __init__(self, user: str, passwd: str, host: str, port: str = "3306") -> None:
        self.USER = user
        self.PASSWD = passwd
        self.HOST = host
        self.PORT = port
        self.SQLALCHEMY_DATABASE_URL = (
            f"mysql+pymysql://{self.USER}:{self.PASSWD}@{self.HOST}:{self.PORT}/soybean"
        )

    def connect(self) -> None:
        info(f"Connecting to {self.HOST}...")
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL, echo=False, pool_pre_ping=True
        )
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        info(f"Connected to {self.HOST} sucessfully!")

    def insert_dataframe(
        self,
        df: pd.DataFrame,
        table: str,
        schema: str,
        if_exists: str = "append",
        index: bool = False,
    ) -> None:
        info(f"Inserting dataframe into table={table} and schema={schema}...")
        df.to_sql(
            name=table,
            schema=schema,
            con=self.engine,
            if_exists=if_exists,
            index=index,
        )
        info(f"Inserted dataframe into table={table} and schema={schema} sucessfully!")

    def read_sql(self, query: str) -> pd.DataFrame:
        info("Reading sql...")
        df = pd.read_sql_query(sql=text(query), con=self.engine.connect())
        return df

    def disconnect(self) -> None:
        info(f"Disconnecting from {self.HOST}...")
        self.engine.dispose()


def get_recent_file(bucket_name):
    s3 = boto3.client("s3")
    arquivos = s3.list_objects_v2(Bucket=bucket_name)["Contents"]
    return max(arquivos, key=lambda x: x["LastModified"])["Key"]


def main(event, context):
    print("INFO: Getting recent files")
    last_filie = get_recent_file("staged-soybean-bucket")
    df = wr.s3.read_parquet(f"s3://staged-soybean-bucket/{last_filie}")
    df = df.round(2)
    mysql_db = MysqlConnection(getenv("USER_BD"), getenv("PASS_BD"), getenv("HOST_BD"))
    mysql_db.connect()
    mysql_db.insert_dataframe(df, "dados_sensor", "soybean", index=False)
    mysql_db.disconnect()

    print("INFO: Creating NPK table")
    df_npk = df[["device_id", "device_name", "n", "p", "k", "setor", "data_hora"]]
    df_npk = df_npk.rename(
        columns={"n": "nitrogen", "p": "phosphorus", "k": "potassium"}
    )
    wr.s3.to_parquet(
        df=df_npk,
        path="s3://consumed-soybean-bucket/npk/",
        mode="append",
        dataset=True,
    )
    del df_npk

    print("INFO: Creating BMP table")
    df_bmp = df[
        ["device_id", "device_name", "temperature", "pressure", "setor", "data_hora"]
    ]
    wr.s3.to_parquet(
        df=df_bmp,
        path="s3://consumed-soybean-bucket/bmp/",
        mode="append",
        dataset=True,
    )
    del df_bmp

    print("INFO: Creating ANEMOMETRO table")
    df_anemometro = df[["device_id", "device_name", "air-speed", "setor", "data_hora"]]
    wr.s3.to_parquet(
        df=df_anemometro,
        path="s3://consumed-soybean-bucket/anemometro/",
        mode="append",
        dataset=True,
    )
    del df_anemometro

    print("INFO: Creating DHT table")
    df_dht = df[
        ["device_id", "device_name", "temperature", "humidity", "setor", "data_hora"]
    ]
    wr.s3.to_parquet(
        df=df_dht,
        path="s3://consumed-soybean-bucket/dht/",
        mode="append",
        dataset=True,
    )
    del df_dht

    print("INFO: Creating TCRT table")
    df_tcrt = df[
        ["device_id", "device_name", "capacity", "collected", "setor", "data_hora"]
    ]
    wr.s3.to_parquet(
        df=df_tcrt,
        path="s3://consumed-soybean-bucket/tcrt/",
        mode="append",
        dataset=True,
    )
    del df_tcrt

    print("INFO: Creating UMIGRAIN table")
    df_umigrain = df[
        ["device_id", "device_name", "humidity_grain", "setor", "data_hora"]
    ]
    wr.s3.to_parquet(
        df=df_umigrain,
        path="s3://consumed-soybean-bucket/umigrain/",
        mode="append",
        dataset=True,
    )
    del df_umigrain
