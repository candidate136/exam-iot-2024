'''
This script is forked from the  https://github.com/suryamurugan/MQTT-to-MYSQL-DB---Python- repo and depends on the Python modules paho-mqtt and mysql-connector-python
I have changed it and used it to solve Task C.1 of the IoT Exam.
This python script will subscribe to the Topic exam_Iot_2024 and get the humidity value from the Mosquitto MQTT broker.
The Script wil then store the humidity value to a Mysql database on a databse called iot and the table flower_sensor.
'''
# Import the needed modules
import mysql.connector
import paho.mqtt.client as mqtt
import json
import datetime

#Here we connect to the Mtsql database running on a Docker container at IP address 10.5.0.6
mydb = mysql.connector.connect(
  host="10.5.0.6",																			# The Ip address of the Mysql database
  user="root",																				# We are using the root user to connect to the database
  passwd="cand136",																			# The password is my exam candidate number 136
  database="iot",																			# The database is called iot
  collation="utf8mb4_unicode_ci",															# This specifies the character set used for storing text data. We get an error if this character set is not used
  charset="utf8mb4"
)

mycursor = mydb.cursor()

#ON_CONNECT print the output on the console/terminal
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
#Inserts the humidity value obtained from the Topic exam_Iot_2024 into the database iot on in the table flower_sensor
	if msg.topic =='exam_Iot_2024':				 											# Checking the Topic
		print(msg.payload.decode("utf-8"))		 											# Justing printin the payload to the terminal/console 
		d=json.loads(msg.payload.decode("utf-8"))											# Converting the payload to JSON
		humidity = d.get("humidity")														# Get the humidity
		ts = datetime.datetime.now()														# Create a timestamp
		sql = "INSERT INTO flower_sensor(id,ts,humidity) VALUES (NULL,%s,%s)"				# Create the SQL query to Insert into the database into the table flower_sensor the time and the humidity value
		val = (ts,humidity)													
		print("sql is ",sql)																# Print the SQL query
		print("val is ",val)																# Print the values that were inserted into the database
		mycursor.execute(sql, val)															# Execute the SQL query
		mydb.commit()																		# 
		print(mycursor.rowcount, "record inserted.","Watering the flower" )										# Print the number of records inserted into the database
	else:
		print(msg.payload.decode("utf-8"))

#ON_ SUBSCRIBE
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


#ON_LOG
#def on_log(mqttc, obj, level, string):
#    print(string)

#We will connect to our Mosquitto MQTT broker with the client ID Flower2 and subscribe to the Topic exam_Iot_2024
mqttc = mqtt.Client(client_id="Flower2")
mqttc.on_message = on_message 					 											# Calls the message function
mqttc.on_connect = on_connect 					 											# Calls the connect function
mqttc.on_subscribe = on_subscribe 				 											# Calls the subscribe function
mqttc.username_pw_set("candidate136", "test123") 											# The MQTT broker is protected with a usermae and a password
mqttc.connect("10.5.0.5", 1883, 60)				 											# We specifying the IP address of the Mosquitto MQTT broker
mqttc.subscribe("exam_Iot_2024", 0)				 											# We are specifying the Topic we are subscribing to
mqttc.loop_forever()							 											# This will continue running until we stop it manually



