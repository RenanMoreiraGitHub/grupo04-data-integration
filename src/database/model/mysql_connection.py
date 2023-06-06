from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from dotenv import load_dotenv
from logging import basicConfig, info, INFO

basicConfig(level=INFO)
load_dotenv()

class MysqlConnection:

    def __init__(self, user: str, passwd: str, host: str, port: str = '3306') -> None:
        self.USER= user
        self.PASSWD= passwd
        self.HOST= host
        self.PORT= port
        self.SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{self.USER}:{self.PASSWD}@{self.HOST}:{self.PORT}/simulator_iot"

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
            schema: str = 'simulator_iot', 
            if_exists: str = 'append', 
            index: bool = False
    ) -> None:
        info(df.to_dict())
        df.to_sql(name=table, schema=schema, con=self.engine, if_exists=if_exists, index=index, )

    def disconnect(self) -> None:
        info(f'Disconnecting database...')
        self.engine.dispose()
        info(f'Disconnected database sucessfully!')
