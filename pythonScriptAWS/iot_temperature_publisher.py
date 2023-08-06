import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging

# Add these lines before the AWSIoTMQTTClient configuration
# Set the logging level to DEBUG
logging.getLogger("AWSIoTPythonSDK.core").setLevel(logging.DEBUG)


# AWS IoT Core settings
endpoint = "a2rloye1ylwgx9-ats.iot.us-east-1.amazonaws.com"
root_ca_path = "AmazonRootCA1.pem"
private_key_path = "49bc3211976ba1763f1045514423f28b823e218f3967e8873860eed0bf38601c-private.pem.key"
certificate_path = "49bc3211976ba1763f1045514423f28b823e218f3967e8873860eed0bf38601c-certificate.pem.crt"
client_id = "iotconsole-c140d8e7-8f3f-495f-b657-31f4eb6ba7f8"

# Create an AWS IoT MQTT client
mqtt_client = AWSIoTMQTTClient(client_id)
mqtt_client.configureEndpoint(endpoint, 8883)
mqtt_client.configureCredentials(root_ca_path, private_key_path, certificate_path)

# Connect to AWS IoT Core
mqtt_client.connect()

def send_temperature_data(temperature):
    data = {
        "device_id": client_id,
        "temperature": temperature
    }
    payload = json.dumps(data)
    topic = "soybean-device"  # Replace with your topic name

    # Publish the temperature data
    mqtt_client.publish(topic, payload, 1)
    print(f"Published: {payload}")

try:
    while True:
        # Simulate reading temperature data from a sensor
        temperature = 25.0  # Replace with your actual sensor reading

        send_temperature_data(temperature)

        time.sleep(5)  # Send data every 5 seconds
except KeyboardInterrupt:
    pass

# Disconnect from AWS IoT Core
mqtt_client.disconnect()
