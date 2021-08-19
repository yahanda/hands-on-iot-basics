# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import datetime

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "{IOTHUB_DEVICE_CONNECTION_STRING}"

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"Start_time": "{start_time}", "End_time": "{end_time}", "Work": "{work}", "Line_num": "{line_num}", "Lot_num": "{lot_num}", "Serial_num": {serial_num}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    #client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING, websockets=True)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        serial = 0
        lot = 0
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            lot += 1
            for i in range(1, 13):
                serial += 1
                # Build the message with simulated telemetry values.
                start_time = datetime.datetime.now()
                time.sleep(random.randint(1, 10))
                end_time = datetime.datetime.now()
                work = "WORK" + str(i).zfill(2)
                line_num = "LINE001"
                lot_num = "LOT" + str(lot).zfill(3)
                serial_num = serial
                msg_txt_formatted = MSG_TXT.format(start_time=start_time, end_time=end_time, work=work, line_num=line_num, lot_num=lot_num, serial_num=serial_num)
                message = Message(msg_txt_formatted)

                # Send the message.
                print( "Sending message: {}".format(message) )
                client.send_message(message)
                print ( "Message successfully sent" )

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()