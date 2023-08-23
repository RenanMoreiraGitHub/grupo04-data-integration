from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from logging import basicConfig, info, INFO

basicConfig(level=INFO)

class MysqlConnection:

    def __init__(self, user: str, passwd: str, host: str, port: str = '3306') -> None:
        self.USER= user
        self.PASSWD= passwd
        self.HOST= host
        self.PORT= port
        self.SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{self.USER}:{self.PASSWD}@{self.HOST}:{self.PORT}/soybean"

    def connect(self) -> None:
        info(f'Connecting to {self.HOST}...')
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL, echo=False, pool_pre_ping=True)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        info(f'Connected to {self.HOST} sucessfully!')
    
    def insert_dataframe(
            self, 
            df: pd.DataFrame, 
            table: str, 
            schema: str, 
            if_exists: str = 'append', 
            index: bool = False
    ) -> None:
        info(f'Inserting dataframe into table={table} and schema={schema}...')
        df.to_sql(name=table, schema=schema, con=self.engine, if_exists=if_exists, index=index, )
        info(f'Inserted dataframe into table={table} and schema={schema} sucessfully!')

    def read_sql(self, query: str) -> pd.DataFrame:
        info('Reading sql...')
        df = pd.read_sql_query(sql=text(query), con=self.engine.connect())
        return df

    def disconnect(self) -> None:
        info(f'Disconnecting from {self.HOST}...')
        self.engine.dispose()
