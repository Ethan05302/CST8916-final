
import time
import json
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Connection string for the IoT Hub device (replace with your own before running)
CONNECTION_STRING = "HostName=rideaucanalhub.azure-devices.net;DeviceId=simulator001;SharedAccessKey=3lTyct56ExxFS+GXBnvDcJqVniXJn++zvY9Q1p5MgFk="

# Simulated locations on the Rideau Canal Skateway
LOCATIONS = ["Dow's Lake", "Fifth Avenue", "NAC"]

# Create a client to connect to the Azure IoT Hub
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# Generate mock sensor data for a given location
def generate_sensor_data(location):
    return {
        "location": location,
        "iceThickness": random.randint(10, 35),
        "surfaceTemperature": random.uniform(-15, 5),
        "snowAccumulation": random.randint(0, 30),
        "externalTemperature": random.uniform(-20, 5),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

# Main function to send sensor data continuously every 10 seconds
def main():
    print("Starting simulator... Press Ctrl+C to stop.")
    try:
        while True:
            for location in LOCATIONS:
                data = generate_sensor_data(location)
                message = Message(json.dumps(data))
                client.send_message(message)
                print(f"Sent from {location}: {data}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.shutdown()

# Entry point of the script
if __name__ == '__main__':
    main()
