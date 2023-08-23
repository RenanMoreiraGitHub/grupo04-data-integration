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

# Add these lines before the AWSIoTMQTTClient configuration
# Set the logging level to DEBUG
logging.getLogger("AWSIoTPythonSDK.core").setLevel(logging.DEBUG)


# AWS IoT Core settings
endpoint = "a2rloye1ylwgx9-ats.iot.us-east-1.amazonaws.com"
root_ca_path = "/home/rodrigo/Documentos/faculdade/keys/AmazonRootCA1.pem"
private_key_path = "/home/rodrigo/Documentos/faculdade/keys/49bc3211976ba1763f1045514423f28b823e218f3967e8873860eed0bf38601c-private.pem.key"
certificate_path = "/home/rodrigo/Documentos/faculdade/keys/49bc3211976ba1763f1045514423f28b823e218f3967e8873860eed0bf38601c-certificate.pem.crt"
client_id = "iotconsole-c140d8e7-8f3f-495f-b657-31f4eb6ba7f8"

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
    while bpm.get_batery() > 0 and anemometro.get_batery() > 0 and npk.get_batery() > 0\
      and dht.get_batery() > 0 and tcrt.get_batery() > 0:
        
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if count < 1:
            #after 60 times change the mean randomly
            temperature_mean = bpm.generate_temperature_mean()
            pressure_mean = bpm.generate_pressure_mean()
            air_speed_mean = anemometro.generate_speed_air_mean()
            count = 60
        
        temperature = bpm.simulate_temperature(temperature_mean)
        pressure = bpm.simulate_pressure(pressure_mean)
        air_speed = anemometro.simulate_speed_air(air_speed_mean)
        n, p, k = npk.simulate_npk()
        humidity =  dht.simulate_humidity()
        capacity = tcrt.simulate_silo_capacity()
        collected = tcrt.simulate_soybeans_collected()
        humidity_grain = umigrain.simulate_humidity()

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
            "batery": bpm.batery,
            "data_hora": data_hora
        }
        
        payload = json.dumps(data)
        topic = "soybean-device"  # Replace with your topic name

        # Publish the temperature data
        mqtt_client.publish(topic, payload, 1)
        print(f"Published: {payload}")
        time.sleep(5)

try:
    while True:
        simulate_data()
except KeyboardInterrupt:
    pass

# Disconnect from AWS IoT Core
mqtt_client.disconnect()
