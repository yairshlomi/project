#!/usr/bin/env python
from __future__ import division
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys
#import requests

#set the communication
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

#send sample request to the arduino
message = list("SAMPLE")

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
units_list=[0,0,0,0,0,0]
i = 0 

#try to send the data to the arduino 30 times. if there is no answer - abort
while True:
    data1 = send_arduino_request()
    if (len(data1) == 0 or data1[0] == '0'):
        i+=1
        print("...")

    elif (data1):
        units_list[0], units_list[1], units_list[2], units_list[3], units_list[4], units_list[5], temp1 = data1.split(" ")
	print("Response received from unit 1\n")
        break
    if (i==30):
        print ("communication faild")
        sys.exit()

   
        


intlist = [int(i) for i in units_list]

intlist[1] = intlist[1]/(100*1.0)
        
float("{0:.2f}".format(intlist[1]))

#write the received data to a file
print ("The data received from unit 1 is: ")
print(str(units_list))
print('\n')

write_to_file = "[\n[1,1,%d],\n[1,2,%d],\n[1,3,%d],\n[1,4,%d],\n[1,5,%f],\n" % (intlist[3], intlist[5], intlist[4], intlist[2], intlist[1])
	
with open ('units.txt', 'a') as f:
    f.write(write_to_file)


sys.exit()  
