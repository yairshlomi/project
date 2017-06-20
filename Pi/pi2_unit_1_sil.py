#!/usr/bin/env python
from __future__ import division
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys
import requests
import json

GPIO.setwarnings(False) 

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
#radio.printDetails()
# radio.startListening()

r = requests.get('https://34.204.144.157/api.php?type=local_fd_get_silenced')
array = r.json()
data = json.loads(array)
tosil = ""
while (data.unit_id = 1 and is_silenced = 1):
    tosil = tosil + sensor_type_id

if (len (tosil) < 2):
    sys.exit(0)


message = list("tosil")

while len(message) <  32:
    message.append(0)

print ("Sending sample request to unit 1: ")
def send_arduino_request():
    start = time.time()
    radio.write(message)
    #print '%s' % .join(map(str, message))
    #print("Sent the message: {}".format(message))
    radio.startListening()

    while not radio.available(0):
        time.sleep(1 / 100)
        if time.time() - start > 2:
            print("...")
            break

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    #print(receivedMessage)
    #print("Received: {}".format(receivedMessage))

    #print("Translating the receivedMessage into unicode characters")
    string = ""
    for n in receivedMessage:
    # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)
    #print("Out received message decodes to: {}".format(string))

    radio.stopListening()
    
    return string

print ("waiting for response")
i = 0 
while True:
    data1 = send_arduino_request()
        i+=1
    if (i==30):

        sys.exit()

sys.exit()  
