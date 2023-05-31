import asyncio
from azure.iot.device import IoTHubSession, MQTTError, MQTTConnectionFailedError
import random

CONNECTION_STRING = "HostName=jeremy02211033.azure-devices.net;DeviceId=jeremy02211033;SharedAccessKey=lCW0G9CVlAKcH6McfQUT0c1V0x+nFFfMXW/2pvXAHhw="
TOTAL_MESSAGES_SENT = 0
battery_level = 100.0
total_messages_failed = 0

async def main():
    global TOTAL_MESSAGES_SENT, battery_level, total_messages_failed
    print("Sending data to Azure")
    print("\n##### Sensor TCRT5000 #####\n")
    try:
        print("Connecting to IoT Hub...")
        async with IoTHubSession.from_connection_string(CONNECTION_STRING) as session:
            print("Connected to IoT Hub")
            while True:
                soybeansCollected = random.randint(3600, 4800)
                siloCapacity = random.randint(4800, 5000)
                siloOcuppationCalc = soybeansCollected / siloCapacity * 100
                
                json_msg = {
                    "messageId": TOTAL_MESSAGES_SENT,
                    "deviceId": 'jeremy02211033',
                    "soyBeansCollected": soybeansCollected,
                    "siloSituation": round(siloOcuppationCalc),
                    "battery": round(battery_level, 2)
                }
                
                if (random.randint(0, 100) < 3):
                    total_messages_failed += 1
                    print("Failure sending message. Messages failed: {}".format(total_messages_failed))
                else:
                    TOTAL_MESSAGES_SENT += 1
                    
                    print("Sending Message #{}...".format(TOTAL_MESSAGES_SENT))
                    await session.send_message("{}".format(json_msg))
                    print("Send Complete")
                    await asyncio.sleep(300)

                    battery_penalty = battery_level * 0.00005
                    battery_level -= battery_penalty
                    if battery_level <= 10:
                        print("\n************ ALERT ************")
                        print("Battery level is getting low: {:.2f}%".format(battery_level))
                        print("The dispositive will shutdown at 5%")
                        if battery_level <= 5:
                            print("Shutting down to preserve battery health, bye!")
                            break
                
    except MQTTError:
        # Connection has been lost.
        print("Dropped connection. Exiting")
    except MQTTConnectionFailedError:
        # Connection failed to be established.
        print("Could not connect. Exiting")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("User initiated exit. Exiting")
    finally:
        print("Sent {} messages in total".format(TOTAL_MESSAGES_SENT))
        print("{} messages failed in total".format(total_messages_failed))
