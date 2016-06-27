# import libraries
import sys
import os
import time
import datetime

# set flag variables
yearflag = False
monthflag = False
dayflag = False
uet = 0

# prompt for date
while (yearflag == False):
	os.system('clear')
	year = int(raw_input("Enter desired year as an integer value between 2010 and 2016: "))
	if (year >= 2010 and year <= 2016):
		yearflag = True
		y = str(year)

while (monthflag == False):
	os.system('clear')
	month = int(raw_input("Enter desired month as an integer value between 1 and 12: "))
	if (month >= 1 and month <= 12):
		monthflag = True
		if (month < 10):
			m = '0' + str(month)
		else:
			m = str(month)

while (dayflag == False):
	os.system('clear')
	day = int(raw_input("Enter desired day as an integer value between 1 and 31: "))
	if (day >= 1 and day <= 31):
		dayflag = True
		if (day < 10):
			d = '0' + str(day)
		else:
			d = str(day)

# convert date to unix timestamp (4pm)
s = d + '/' + m + '/' + y
t = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
uet = int(t) + 32400

# print date to screen
os.system('clear')
print "Collecting data for " + m + '/' + d + '/' + y
print ' '

# update start time for ripe
f = open("start_time.txt", "w")
f.write(str(uet))
f.close()

	# run script syscalls
"""
try:
	# run ripe collector (this one will increment day by day using unix epoch time, for reference see start_time.txt)
	print "Working Ripe"
	os.system("python ripe.py")
except:
	print "No Ripe data for this day"
	print " "
"""

ark_params = "python arkparse.py " + d + ' ' + m + ' ' + y
try:
	print "Working Ark"
	os.system(ark_params)
except:
	print "No Ripe data for this day"
	print " "

"""
try:
	os.system("python mlab.py")
except:
	print "No Ripe data for this day"
	print " "


try:
	os.system("python iplane_trace.py")
except:
	print "No Ripe data for this day"
	print " "
"""