import paho.mqtt.client as mqtt
import time
#from random import randrange, uniform


mqttBroker = "mqtt.eclipseprojects.io"


client = mqtt.Client("Trigger_from_cnn")
client.connect(mqttBroker)

while(True):
  n = input("Enter number : ")
  #randNum = "Hey there! Connecting over internet..just 1 time"
  client.publish("Test2", n, qos = 1) #publish(topic, payload=None, qos=0, retain=False)
  print("Just published " + n + " to topic Test2")
  time.sleep(1)
  