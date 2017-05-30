from datetime import datetime
import smtplib
import requests
import re
from smtplib import SMTP_SSL as SMTP
import logging, logging.handlers, sys
from email.mime.text import MIMEText
import json


to_send = ""

with open('units.txt', "r") as fr:
    to_send = fr.read()
print("i got the files")
print (to_send)

r = requests.post('http://34.204.144.157/index.php', data=to_send)
print (r.status_code)

to_write = str(datetime.now().strftime('%H:%M:%S %d-%m-%Y')) + "\n" + to_send

print (to_write)

with open('db.txt', "a") as fw:
    fw.write(to_write)

raw  = []
data = {'unit_id' : 0, 'sensor_id' : 0, 'sensor_data' : 0}
for line in to_send.splitlines():
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
	if(int (data['sensor_id']) == 1 and int(data['sensor_data']) < 250 ): #flame
		flame = True
	if(int (data['sensor_id']) == 3 and int(data['sensor_data']) > 500 ): #smoke
		smoke = True
	if(int (data['sensor_id']) == 2 and int(data['sensor_data']) > 500 ): #lpg
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
	
print ("\nunusual values:")
for data in is_risked:
	print (data)
	body = body + json.dumps(data) + "'\n"


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

print ("mail sent successfully")
with open('units.txt', "w"):
	pass

