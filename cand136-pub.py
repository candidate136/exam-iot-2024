'''
This script is created by candidate 136 to solve Task C.1 of the IoT exam of 2024.
The script will simulate an IoT sensor that measures humidity and publish the value to an MQTT broker.
This python script will publish to the Topic exam_Iot_2024, so that any subscriber to the topic will get the humidity value.
'''
# Import the rquired modules.
import paho.mqtt.client as mqtt
import json
import threading
import random

''''
The function takes one parameter(JSON)object and then connects to the MQTT broker with the client ID Flower.
Then publishes the value of humidty obtained from the JSON object to the Topic exam_Iot_2024.
'''
def send_humidity(value):
    my_client = mqtt.Client(client_id="Flower")                                            # Connect to the mqtt broker with client_id Flower
    my_client.username_pw_set("candidate136", "test123")                                   # The mqtt broker is protected with a username and apassword
    my_client.connect("10.5.0.5", 1883, 60)                                                # The ip address of the mqtt broker and the standard port to use
    my_client.publish("exam_Iot_2024", json.dumps(value))                                  # The topic and content to publish

'''
A Function that uses the Threading Timer.
It will execute the function at the predtermined interval.
'''
def run_function():
    thread = threading.Timer(10.0, run_function)                                           # The function will be executed every 10 seconds
    thread.start()                                                                         # This starts the timer
    humid = random.randint(25,35)                                                          # We are simulating reading the humidty by generating it randomly
    if humid > 28:                                                                         # Check if the humidity is higher than 28 
        json_value = {"humidity": humid}                                                   # We create a JSON object containing the hudity value
        send_humidity(json_value)                                                          # If the humidity is higher than 28, we publish the value to our MQTT broker  

'''This will call run_function() which then calls the send_humidty()'''
run_function()                                                             