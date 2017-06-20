#!/usr/bin/env python
from datetime import datetime
import smtplib
import requests
import re
from smtplib import SMTP_SSL as SMTP
import logging, logging.handlers, sys
from email.mime.text import MIMEText
import json
import time


print ("Processing data from sensor units.")
time.sleep(5)
to_send = ""

with open('units.txt', "r") as fr:
    to_send = fr.read()
print("Reading from files ended successfully")
print (to_send)

r = requests.post('http://34.204.144.157/index.php', data=to_send)
time.sleep(3)
print ("\nthe response code is: " + str(r.status_code) + "\n")

if(int(r.status_code)==200):
	print("Sending the data to the server ended successfully" + "\n") 
else:
	print("data not sent" + "\n")


to_write = "\n" + str(datetime.now().strftime('%H:%M:%S %d-%m-%Y')) + "\n" + to_send

#print (to_write)

with open('db.txt', "a") as fw:
	fw.write(to_write)
	fw.write(" ")

time.sleep(3)
raw  = []
data = {'unit_id' : 0, 'sensor_id' : 0, 'sensor_data' : 0}
for line in to_send.splitlines():
        if(len(line) > 2):
                data['unit_id'], data['sensor_id'], data['sensor_data'] = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", line)
                print (data)
                raw.append(dict(data))


is_risked = []
temp = False
flame = False
smoke = False
lpg = False

subject = 'alaram '
for data in raw:
	if(int (data['sensor_id']) == 5 and float(data['sensor_data']) > 50 ): #temp
		temp == True
	if(int (data['sensor_id']) == 1 and int(data['sensor_data']) > 400 ): #flame
		flame = True
	if(int (data['sensor_id']) == 3 and int(data['sensor_data']) > 750 ): #smoke
		smoke = True
	if(int (data['sensor_id']) == 2 and int(data['sensor_data']) > 800 ): #lpg
		lpg = True
	
	if (temp or flame or smoke or lpg):	
		is_risked.append(dict(data))

	if (temp):
		subject = subject + ' temprature'

	if (flame):
		subject = subject + ' flame'

	if (smoke):
		subject = subject + ' smoke'

	if (lpg):
		subject = subject + ' lpg'

	temp = False
	flame = False
	smoke = False
	lpg = False


body = ""
send = True
time.sleep(5)
print ("\nunusual values:")
for data in is_risked:
	print (data)
	body = body + json.dumps(data) + "'\n"
if(body.isspace() or len(subject) < 8):
	print ("no unusual values detected")
	send = False

else:
        
		val_unit = "{\"type\":\"alarms\", \"values\": [1,"data['unit_id']"]}"
		print ("Setting is alarm = true")
		 = requests.post('http://34.204.144.157/api.php', data=val_unit)
		time.sleep(3)
		print ("\nthe response code is: " + str(res.status_code) + "\n")

		if(int(res.status_code)==200):
			print("Sending the data to the server ended successfully" + "\n") 
		else:
			print("data not sent" + "\n")



        print ("sending mails")
        try:
   
            to = "canarit.gfd@gmail.com" #Recipient's email address
            frm = "canarit.alarms@gmail.com" #Sender's email address
            pswd = "canarit2017" #Sender's password
            sub = subject         #Subject of email
            text = body                    #Message to send
            msg = MIMEText(text, 'plain')
            msg['Subject'] = sub
            msg['To'] = to
        except Exception as err:
            pass

        try:
            conn = SMTP("smtp.gmail.com")
            conn.login(frm, pswd)
            try: conn.sendmail(frm, to, msg.as_string())
            finally: conn.close()
        except Exception as exc:
            print(exc)
            sys.exit("Mail failed: {}".format(exc))

time.sleep(3)
if(send == True):
        print ("mail sent successfully")
with open('units.txt', "w"):
	pass

