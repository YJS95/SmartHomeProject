import paho.mqtt.client as mqtt
import Adafruit_DHT
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)


sensor = Adafruit_DHT.DHT11

pin = '4'


    

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))

#led 제어
def on_message(client, userdata, msg):
    rcvmsg = str(msg.payload.decode("utf-8"))
    print(rcvmsg)
    if rcvmsg == '1':
        GPIO.output(17, GPIO.HIGH)
    elif rcvmsg == '2':
        GPIO.output(17, GPIO.LOW)

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

#내 ip주소로 변경 
client.connect('192.168.0.11', 1883)
client.subscribe('led')
client.loop_start()

#온습도 센서 제어
while True:

    humi, temp = Adafruit_DHT.read_retry(sensor, pin)

    if humi is not None and temp is not None:
        print(temp, humi)
    else:
        print("failed to get reading. try again!")

    message = "{\"temp\":%s,\"humi\":%s}" % (temp, humi)
    client.publish('dht11',message)

    time.sleep(1)

client.loop_forever()

