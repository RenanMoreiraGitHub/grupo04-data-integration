from pandas import DataFrame
from datetime import datetime
from pytz import timezone
from random import uniform

class Humidity:

    def __init__(self) -> None:
        self.__data: dict = {}
        self.__data['humidity'] = self.catch_humidity()
        self.__data['date'] = self.catch_date()

    def catch_humidity(self) -> float:
        humidity = round(uniform(12.0, 20), 1)
        return humidity
    
    def catch_humidity_str(self) -> str:
        humidity = round(uniform(12.0, 20), 1)
        return str(humidity)
    
    def catch_date(self) -> datetime:
        now = datetime.now(timezone('America/Sao_Paulo'))
        return now

    def get_data(self) -> DataFrame:
        df = DataFrame(self.__data, index=['data'])
        return df
