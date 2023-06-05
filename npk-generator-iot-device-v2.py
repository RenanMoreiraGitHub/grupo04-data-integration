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
    
    global bateria
    bateria = 100.000

    global nivel_fertil

    # Olá Aluno(a), substitua o valor da string abaixo pela chave de conexão do dispositivo criado no IoT Hub
    conn_str = "HostName=npkgenerator.azure-devices.net;DeviceId=sensor-npk;SharedAccessKey=JFbeMDsWPCLhqj+omqy8EWf5kkaW6Ft7xEXBLgUHhNw="
    conn_str_edu = "HostName=eduardo02211010.azure-devices.net;DeviceId=eduardo02211010;SharedAccessKey=PWxESNEFrbU4+x0b6AgTY7SrTHE5pqvU12NHGMrz4Qc="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    device_client_edu = IoTHubDeviceClient.create_from_connection_string(conn_str_edu)

    print("Envio de dados para a Azure\n")
    print("================================== SENSOR NPK ==================================")
    try:
        # Connect the client.
        device_client.connect()
        device_client_edu.connect()

        i = 0
        while True:
            i+= 1
            bateria -= 0.005
            dado_n = random.randint(60, 251)
            dado_k = random.randint(50, 301)

            if dado_n >= 150:
                dado_p = random.randint(40, 61);
                dado_k = random.randint(200, 301);
                nivel_fertil =  "Fértil"
            elif (dado_n >= 120 and dado_n < 150):
                dado_p = random.randint(20, 41);
                dado_k = random.randint(150, 201)
                nivel_fertil = "Média a alta fertilidade"
            elif (dado_n >= 90 and dado_n < 120):
                dado_p = random.randint(10, 21);
                dado_k = random.randint(100, 151);
                nivel_fertil = "Médio de fertilidade"
            else:
                nivel_fertil = "Falta de fertilizantes"

            if(random.randint(0, 100) < 3):
                print("Erro de envio...")
            else:
                payload = {"ID": i, "N": dado_n, "P": dado_p, "K": dado_k, "Fertilidade": nivel_fertil, "Bateria": math.floor(bateria)}
                payload = Message(str(payload))
                payload.custom_properties["fertilidade"] = "Falta de fertilizantes" if nivel_fertil == "Falta de fertilizantes" else "no"
                payload.message_id = uuid.uuid4()
                payload.correlation_id = "correlation-1234"
                payload.content_encoding = "utf-8"
                payload.content_type = "application/json"
                print("sending message #" + str(i) + ": body: " + str(payload) + ", Alert: " + str(payload.custom_properties["fertilidade"]))
                device_client.send_message(payload)
                device_client_edu.send_message(payload)
                time.sleep(5)
    except KeyboardInterrupt:
        print("User initiated exit")
    except Exception:
        print("Unexpected exception!")
        raise
    finally:
        device_client.shutdown()
        device_client_edu.shutdown()


if __name__ == "__main__":
    main()
