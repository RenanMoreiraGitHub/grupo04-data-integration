# az iot hub monitor-events --hub-name aula01-teste --device-id humidity-device

from os import getenv
from database.model.mysql_connection import MysqlConnection
from simulator.humidity.model.humidity import Humidity
from simulator.humidity.service.humidity import sensor_humidity
from log.log import setup_log

from dotenv import load_dotenv; load_dotenv()
setup_log()

mysql = MysqlConnection(user=getenv('BD_USER'), 
                        passwd=getenv('BD_PASS'),
                        host=getenv('BD_HOST'))

sensor_humidity(Humidity, sleep_rule=2)
