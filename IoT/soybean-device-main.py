import random
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
from anemometro import Anemometro
from bmp180 import BPM180
from npk import NPK
from dht11 import DHT11
from tcrt5000 import TCRT5000
from umigrain import Umigrain
from datetime import datetime
from mysql_connection import MysqlConnection
from dotenv import load_dotenv
from os import getenv
import pandas as pd

load_dotenv()

# logging.getLogger("AWSIoTPythonSDK.core").setLevel(logging.DEBUG)

# Add these lines before the AWSIoTMQTTClient configuration
# Set the logging level to DEBUG

with open("certificados/outputs.json", "r") as file:
    data = json.load(file)

with open("certificados/AmazonRootCA1.pem", "w") as output_file:
    output_file.write(data["ca"]["value"])

with open("certificados/private_key.pem.key", "w") as output_file:
    output_file.write(data["key"]["value"])

with open("certificados/certificate.pem.crt", "w") as output_file:
    output_file.write(data["cert"]["value"])


endpoint = data["iot_endpoint"]["value"]
root_ca_path = "certificados/AmazonRootCA1.pem"
private_key_path = "certificados/private_key.pem.key"
certificate_path = "certificados/certificate.pem.crt"
client_id = "iotconsole-db28081b-7473-4584-87cc-87bb2992f12e"


# Create an AWS IoT MQTT client
mqtt_client = AWSIoTMQTTClient(client_id)
mqtt_client.configureEndpoint(endpoint, 8883)
mqtt_client.configureCredentials(root_ca_path, private_key_path, certificate_path)

# Connect to AWS IoT Core
mqtt_client.connect()
bpm = BPM180()
anemometro = Anemometro()
npk = NPK()
dht = DHT11()
tcrt = TCRT5000()
umigrain = Umigrain()


def simulate_data():
    temperature_mean = bpm.generate_temperature_mean()
    pressure_mean = bpm.generate_pressure_mean()
    air_speed_mean = anemometro.generate_speed_air_mean()

    count = 60
    while (
        bpm.get_batery() > 0
        and anemometro.get_batery() > 0
        and npk.get_batery() > 0
        and dht.get_batery() > 0
        and tcrt.get_batery() > 0
    ):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if count < 1:
            # after 60 times change the mean randomly
            temperature_mean = bpm.generate_temperature_mean()
            pressure_mean = bpm.generate_pressure_mean()
            air_speed_mean = anemometro.generate_speed_air_mean()
            count = 60

        temperature = bpm.simulate_temperature(temperature_mean)
        pressure = bpm.simulate_pressure(pressure_mean)
        air_speed = anemometro.simulate_speed_air(air_speed_mean)
        n, p, k = npk.simulate_npk()
        humidity = dht.simulate_humidity()
        capacity = tcrt.simulate_silo_capacity()
        collected = tcrt.simulate_soybeans_collected()
        humidity_grain = umigrain.simulate_humidity()
        setor = random.randint(1, 4)
        data = {
            "device_id": client_id,
            "device_name": "soybean-device",
            "temperature": temperature,
            "pressure": pressure,
            "air-speed": air_speed,
            "n": n,
            "p": p,
            "k": k,
            "humidity": humidity,
            "capacity": capacity,
            "collected": collected,
            "humidity_grain": humidity_grain,
            "setor": setor,
            "batery": bpm.batery,
            "data_hora": data_hora,
        }

        payload = json.dumps(data)
        topic = "thing_soybean"  

        mqtt_client.publish(topic, payload, 1)
        print(f"Published: {payload}")
        time.sleep(0.3)
        return data


# try:
#     mysql_connection = MysqlConnection(
#         getenv("USER_BD"), getenv("PASS_BD"), getenv("HOST_BD")
#     )
#     mysql_connection.connect()
while True:
    data = simulate_data()
    df = pd.DataFrame([data])
    df = df.round(2)
    #         mysql_connection.insert_dataframe(df, "dados_sensor", "soybean", index=False)

    # except KeyboardInterrupt:
    #     mysql_connection.disconnect()

    # Disconnect from AWS IoT Core
    mqtt_client.disconnect()
