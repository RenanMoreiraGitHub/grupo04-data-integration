import random
import time
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
import math
import uuid


def main():

    global bateria
    bateria = 100.000

    global nivel_fertil

    # Olá Aluno(a), substitua o valor da string abaixo pela chave de conexão do dispositivo criado no IoT Hub
    conn_str = "HostName=rodrigo02211059.azure-devices.net;DeviceId=rodrigo02211059;SharedAccessKey=TeFXE3MBh+7GdJxfrcVW6bvVMCPXIjYGWUoWEaUTpR8="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    print("Envio de dados para a Azure\n")
    print("================================== SENSOR DHT11 ==================================")
    try:
        # Connect the client.
        device_client.connect()

        i = 0
        while True:
            i += 1
            bateria -= 0.005

            temperature = random.randint(20, 30)
            humidity = random.randint(50, 55)

            if(random.randint(0, 100) < 3):
                print("Erro de envio...")
            else:
                payload = {"ID": i, "temperature": temperature,
                           "humidity": humidity, "Bateria": math.floor(bateria)}
                payload = Message(str(payload))
                payload.custom_properties["temperature"] = "Temperatura alta" if temperature >= 27 else "Temperatura normal"
                payload.message_id = uuid.uuid4()
                payload.correlation_id = "correlation-1234"
                payload.content_encoding = "utf-8"
                payload.content_type = "application/json"
                print("sending message #" + str(i) + ": body: " + str(payload) +
                      ", Alert: " + str(payload.custom_properties["temperature"]))
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
