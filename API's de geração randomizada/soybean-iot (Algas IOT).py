# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
import random
import math
import uuid
import time

def main():
    
    global battery_level
    battery_level = 100.0

    # Olá Aluno(a), substitua o valor da string abaixo pela chave de conexão do dispositivo criado no IoT Hub
    conn_str = "HostName=jeremy02211033.azure-devices.net;DeviceId=jeremy02211033;SharedAccessKey=lCW0G9CVlAKcH6McfQUT0c1V0x+nFFfMXW/2pvXAHhw="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    print("Sending data to Azure")
    print("\n##### Sensor TCRT5000 #####\n")
    try:
        # Connect the client.
        device_client.connect()

        i = 0
        while True:
            i+= 1
            battery_penalty = battery_level * 0.00005
            battery_level -= battery_penalty
            
            soybeansCollected = random.randint(3600, 4800)
            siloCapacity = random.randint(4800, 5000)
            siloOcuppationCalc = soybeansCollected / siloCapacity * 100

            if (random.randint(0, 100) < 3):
                    print("Failure sending message.")
            else:
                payload = {"ID": i, "soybeansCollected": soybeansCollected, "siloCapacity": round(siloCapacity),  "battery_level": math.floor(battery_level)}
                payload = Message(str(payload))
                payload.custom_properties["silo-warning"] = "Alerta de capacidade" if siloOcuppationCalc > 90 else "no"
                payload.message_id = uuid.uuid4()
                payload.correlation_id = "correlation-1234"
                payload.content_encoding = "utf-8"
                payload.content_type = "application/json"
                print("sending message #" + str(i) + ": body: " + str(payload) + ", Alert: " + str(payload.custom_properties["silo-warning"]))
                device_client.send_message(payload)
                time.sleep(2)
    except KeyboardInterrupt:
        print("User initiated exit")
    except Exception:
        print("Unexpected exception!")
        raise
    finally:
        device_client.shutdown()


if __name__ == "__main__":
    main()