import paho.mqtt.client as mqtt 
import time 
import pyfirmata 
import time 



board = pyfirmata.Arduino("COM4") #for arduino board

#configuring pins for sensors
red_led = board.get_pin('d:6:o') #digital pin 6
green_led = board.get_pin('d:7:o')#digital pin 7
gas_sen =  board.get_pin('a:0:i')#analog input 0
rain_sens = board.get_pin('a:1:i')#analog input 1


#functions to trigger
def red_on(): 
    red_led.write(1) 
    print("Red ON")
    return

def red_off():
    red_led.write(0)
    print("Red OFF")
    return

def green_on():
    green_led.write(1)
    print ("Green on")
    return

def green_off():
    green_led.write(0)
    print("Green OFF")


def get_rainval():
    rainval = rain_sens.read()
    print(rainval)
    return 


func_map = { '1' : red_on, '2' : red_off, '3' : green_on, '4' : green_off, '5 ':  get_rainval}

def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    print("Trigger : ", str(message.payload.decode("utf-8")))
    func_map[m]()
    
    #print("Topic : ", message.topic)
    #print("Qos : ", message.qos)

it = pyfirmata.util.Iterator(board)
it.start()

mqttBroker = "mqtt.eclipseprojects.io"

client = mqtt.Client("sensor_area")
client.connect(mqttBroker) #connect(host, port=1883, keepalive=60, bind_address="")

client.loop_start()

client.subscribe("Test2",1) #subscribe(topic, qos=0)
client.on_message = on_message

time.sleep(30)
client.loop_stop()