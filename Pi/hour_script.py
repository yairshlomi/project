#!/usr/bin/env python

from smtplib import SMTP_SSL as SMTP
import logging, logging.handlers, sys
from email.mime.text import MIMEText
import re
import math

#createv class for packets (1 packet includes the values of each sensor from unit 1 and unit 2, combined with packet id and the time it was sent)
class Packet:

	def __init__(self):
		pass
   	
	unit_1_temp = 0
	unit_1_flame = 0
	unit_1_gas = 0
	unit_1_lpg = 0
	unit_2_temp = 0
	unit_2_flame = 0
	unit_2_gas = 0
	unit_2_lpg = 0
	minute = 0
	packet_id = 0

	def set_unit_1_temp(self, unit_1_temp_new):
		self.unit_1_temp = unit_1_temp_new
	def get_unit_1_temp(self):
		return self.unit_1_temp

	def set_unit_1_flame(self, unit_1_flame_new):
		self.unit_1_flame = unit_1_flame_new
	def get_unit_1_flame(self):
		return self.unit_1_flame

	def set_unit_1_smoke(self, unit_1_smoke_new):
		self.unit_1_smoke = unit_1_smoke_new
	def get_unit_1_smoke(self):
		return self.unit_1_smoke

	def set_unit_1_lpg(self, unit_1_lpg_new):
		self.unit_1_lpg = unit_1_lpg_new
	def get_unit_1_lpg(self):
		return self.unit_1_lpg

	def set_unit_2_temp(self, unit_2_temp_new):
		self.unit_2_temp = unit_2_temp_new
	def get_unit_2_temp(self):
		return self.unit_2_temp

	def set_unit_2_flame(self, unit_2_flame_new):
		self.unit_2_flame = unit_2_flame_new
	def get_unit_2_flame(self):
		return self.unit_2_flame

	def set_unit_2_smoke(self, unit_2_smoke_new):
		self.unit_2_smoke = unit_2_smoke_new
	def get_unit_2_smoke(self):
		return self.unit_2_smoke

	def set_unit_2_lpg(self, unit_2_lpg_new):
		self.unit_2_lpg = unit_2_lpg_new
	def get_unit_2_lpg(self):
		return self.unit_2_lpg

	def set_packet_minute(self, packet_minute):
		self.minute = packet_minute
	def get_packet_minute(self):
		return self.minute

	def set_packet_id(self, packet_id_new):
		self.packet_id = packet_id_new
	def get_packet_id(self):
		return self.packet_id

	def __str__(self):
		return ("the id of the packet is: " + str(self.get_packet_id())) + '\n' + ("the minute of the packet is: " + str(self.get_packet_minute())) + '\n' + ("unit 1 temprature sensor value = " + str(self.get_unit_1_temp())) + '\n' + ("unit 1 flame sensor value = " + str(self.get_unit_1_flame())) + '\n' + ("unit 1 smoke sensor value = " + str(self.get_unit_1_smoke())) + '\n' + ("unit 1 lpg sensor value = " + str(self.get_unit_1_lpg())) + '\n' + ("unit 2 temprature sensor value = " + str(self.get_unit_2_temp())) + '\n' + ("unit 2 flame sensor value = " + str(self.get_unit_2_flame())) + '\n' + ("unit 2 smoke sensor value = " + str(self.get_unit_2_smoke())) + '\n' + ("unit 2 lpg sensor value = " + str(self.get_unit_2_lpg()))





units_data_raw = []
units_data_string = []
data_sets = []

row_counter = 0
packet_counter = 0
data = ""
temp = Packet()
minute_int = 0
#open the DB file (not the SQL DB), read from it line by line and store it in the packet class objects
with open('db.txt', "r") as fr:
	for line in iter(fr):
		data = line
		if (data[0].isnumeric()):
			minute = data[3:5]
			#print (minute)
			temp.set_packet_minute(int(minute))
		elif (len(data) > 4):
			if (row_counter < 10) :
				data_string = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", line)
				row_counter += 1
				print (data_string)				                          
				if (int (data_string[0]) == 1):
					if (int (data_string[1]) == 1):
						temp.set_unit_1_flame(int(data_string[2]))
					if (int (data_string[1]) == 2):
						temp.set_unit_1_lpg(int(data_string[2]))
					if (int (data_string[1]) == 3):
						temp.set_unit_1_smoke(int(data_string[2]))
					if (int (data_string[1]) == 5):
						temp.set_unit_1_temp(float(data_string[2]))

				if (int (data_string[0]) == 2):
					if (int (data_string[1]) == 1):
						temp.set_unit_2_flame(int(data_string[2]))
					if (int (data_string[1]) == 2):
						temp.set_unit_2_lpg(int(data_string[2]))
					if (int (data_string[1]) == 3):
						temp.set_unit_2_smoke(int(data_string[2]))
					if (int (data_string[1]) == 5):
						temp.set_unit_2_temp(float(data_string[2]))

				if (row_counter == 10):
					#print (temp)
					packet_counter += 1
					temp.set_packet_id(packet_counter)
					row_counter = 0
					data_sets.append(temp)
					temp = Packet()

			
for data_line in data_sets:
	print (data_line)
	print("")

#calc the expectancy of all the readings in the last hour

temp_expectancy_1 = 0
flame_expectancy_1 = 0
smoke_expectancy_1 = 0
lpg_expectancy_1 = 0
temp_expectancy_2 = 0
flame_expectancy_2 = 0
smoke_expectancy_2 = 0
lpg_expectancy_2 = 0
size = len (data_sets)


for i in range(1,size):
	temp_expectancy_1 += math.pow((data_sets[i].get_unit_1_temp() - data_sets[i-1].get_unit_1_temp()), 2)
	flame_expectancy_1 += math.pow((data_sets[i].get_unit_1_flame() - data_sets[i-1].get_unit_1_flame()), 2)
	smoke_expectancy_1 += math.pow((data_sets[i].get_unit_1_smoke() - data_sets[i-1].get_unit_1_smoke()), 2)
	lpg_expectancy_1 += math.pow((data_sets[i].get_unit_1_lpg() - data_sets[i-1].get_unit_1_lpg()), 2)
	temp_expectancy_2 += math.pow((data_sets[i].get_unit_2_temp() - data_sets[i-1].get_unit_2_temp()), 2)
	flame_expectancy_2 += math.pow((data_sets[i].get_unit_2_flame() - data_sets[i-1].get_unit_2_flame()), 2)
	smoke_expectancy_2 += math.pow((data_sets[i].get_unit_2_smoke() - data_sets[i-1].get_unit_2_smoke()), 2)
	lpg_expectancy_2 += math.pow((data_sets[i].get_unit_2_lpg() - data_sets[i-1].get_unit_2_lpg()), 2)


temp_difference_1 = 0
flame_difference_1 = 0
smoke_difference_1 = 0
lpg_difference_1 = 0
temp_difference_2 = 0
flame_difference_2 = 0
smoke_difference_2 = 0
lpg_difference_2 = 0


#calc the differnces and the standard deviation of all the readings in the last hour
temp_difference_1 = (data_sets[size-1].get_unit_1_temp() - data_sets[0].get_unit_1_temp())
flame_difference_1 = (data_sets[size-1].get_unit_1_flame() - data_sets[0].get_unit_1_flame())
smoke_difference_1 = (data_sets[size-1].get_unit_1_smoke() - data_sets[0].get_unit_1_smoke())
lpg_difference_1 = (data_sets[size-1].get_unit_1_lpg() - data_sets[0].get_unit_1_lpg())
temp_difference_2 =(data_sets[size-1].get_unit_2_temp() - data_sets[0].get_unit_2_temp())
flame_difference_2 = (data_sets[size-1].get_unit_2_flame() - data_sets[0].get_unit_2_flame())
smoke_difference_2 = (data_sets[size-1].get_unit_2_smoke() - data_sets[0].get_unit_2_smoke())
lpg_difference_2 = (data_sets[size-1].get_unit_2_lpg() - data_sets[0].get_unit_2_lpg())

temp_std_dev_1 = int(math.sqrt(temp_expectancy_1/size))
flame_std_dev_1 = int(math.sqrt(flame_expectancy_1/size))
smoke_std_dev_1 = int(math.sqrt(smoke_expectancy_1/size))
lpg_std_dev_1 = int(math.sqrt(lpg_expectancy_1/size))
temp_std_dev_2 = int(math.sqrt(temp_expectancy_2/size))
flame_std_dev_2 = int(math.sqrt(flame_expectancy_2/size))
smoke_std_dev_2 = int(math.sqrt(smoke_expectancy_2/size))
lpg_std_dev_2 = int(math.sqrt(lpg_expectancy_2/size))


print ("the the difference of unit 1 temprature is : " + str(int(temp_difference_1)) + ", with standard deviation of " + str(temp_std_dev_1))
print ("the the difference of unit 1 flame is : " + str(int(flame_difference_1)) + ", with standard deviation of " + str(flame_std_dev_1))
print ("the the difference of unit 1 smoke is : " + str(int(smoke_difference_1)) + ", with standard deviation of " + str(smoke_std_dev_1))
print ("the the difference of unit 1 lpg is : " + str(int(lpg_difference_1)) + ", with standard deviation of " + str(lpg_std_dev_1))
print ("the the difference of unit 2 temprature is : " + str(int(temp_difference_2)) + ", with standard deviation of " + str(temp_std_dev_2))
print ("the the difference of unit 2 flame is : " + str(int(flame_difference_2)) + ", with standard deviation of " + str(flame_std_dev_2))
print ("the the difference of unit 2 smoke is : " + str(int(smoke_difference_2)) + ", with standard deviation of " + str(smoke_std_dev_2))
print ("the the difference of unit 2 lpg is : " + str(int(lpg_difference_2)) + ", with standard deviation of " + str(lpg_std_dev_2))


#if there is unusual value (if the standard deviation is too big) send mail.
subject = "Unusual values detected"
body = " "
if (temp_difference_1 > 12 and temp_std_dev_1 < 4):
	body = body + "Unusual temprature values detected at unit 1\n"

if (flame_difference_1 < (-100) and flame_std_dev_1 < 50):
	body = body + "Unusual flame values detected at unit 1\n"

if (smoke_difference_1 > 300 and smoke_std_dev_1 < 50):
	body = body + "Unusual smoke values detected at unit 1\n"

if (lpg_difference_1 > 300 and lpg_std_dev_1 < 50):
	body = body + "Unusual lpg values detected at unit 1\n"

if (temp_difference_2 > 12 and temp_std_dev_2 < 4):
	body = body + "Unusual temprature values detected at unit 2\n"

if (flame_difference_2 < (-100) and flame_std_dev_2 < 50):
	body = body + "Unusual flame values detected at unit 2\n"

if (smoke_difference_2 > 300 and smoke_std_dev_2 < 50):
	body = body + "Unusual smoke values detected at unit 2\n"

if (lpg_difference_2 > 300 and lpg_std_dev_2 < 50):
	body = body + "Unusual lpg values detected at unit 2\n"

if (body.isspace()):
	print ("no unusual values detected")

else: 
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
		try: 
			conn.sendmail(frm, to, msg.as_string())
			print ("mail sent successfully")
		finally: conn.close()
	except Exception as exc:
		print(exc)
		sys.exit("Mail failed: {}".format(exc))
