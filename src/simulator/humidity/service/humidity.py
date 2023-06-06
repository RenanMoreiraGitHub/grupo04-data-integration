from azure.iot.device import IoTHubDeviceClient
from time import sleep
from os import getenv
from log.exceptions import EmptyBatteryEnergy, IotHubSentMessageError
from random import randint
from logging import info

def sensor_humidity(
        Humidity,
        sleep_rule: int = 0
) -> None:
    client = IoTHubDeviceClient.create_from_connection_string(getenv('CONNECTION_STR'))
    battery = 100.00
    try:
        while True:
            if battery <= 0:
                raise EmptyBatteryEnergy(f"Bateria {battery}%, shutting down!")
            if randint(0, 100) < 3:
                raise IotHubSentMessageError(f"Fail to sent message to iot hub!")

            humidity_generator = Humidity()
            hum = humidity_generator.catch_humidity_str()
            message = f'{hum} | {round(battery, 3)}%'
            info(f'Sending message to iothub: {message}')
            client.send_message(message)
            battery -= 0.005
            sleep(sleep_rule)
    except Exception as e:
        raise e
