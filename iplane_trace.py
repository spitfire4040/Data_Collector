# import headers
import sys
import os
import urllib
import gzip


# initialize variables
hop = 1
flag = False
src = ''
dst = ''

# iterate through 30 days
for x in range(1, 31):

	print "Day ", x

	# initialize variables
	trace = []
	all_traces = []
	all_ips = []
	unique_traces = set()
	unique_ips = set()	

	# fix number for date
	if x < 10:
		day = '0' + str(x)
	else:
		day = str(x)

	# open nodelist
	f = open("nodelist.txt", "r")

	# iterate through each line in nodelist
	for line in f:

		try:

			# retrieve file
			urllib.urlretrieve("http://iplane.cs.washington.edu/data/iplane_logs/2016/04/" + day + "/" + line, "temp.gz")

			print "http://iplane.cs.washington.edu/data/iplane_logs/2016/04/" + day + "/" + line

			# open in and out files for .gz processing
			with gzip.open("temp.gz", "rb") as in_file:
				s = in_file.read()

			with open("temp.out", "w") as out_file:
				out_file.write(s)

			# call c code to stream file to text > temp.txt
			os.system("./a.out temp.out > temp.txt")

			# build list of traces for each day
			infile = open("temp.txt", "r")

			# iterate through lines of f
			for line in infile:
				line = line.split()

				# if 'destination', write and reset
				if (line[0] == "destination:"):
					dst = line[1]

					# add to ip lists
					all_ips.append(dst)
					unique_ips.add(dst)

					# get rid of empty line
					if trace != None:

						# add to trace lists
						all_traces.append(''.join(trace))
						unique_traces.add(''.join(trace))

					# reset lists and flag
					trace = []
					hop = 1
					flag = False
				else:
					if line[1] == "0.0.0.0":
						addr = '0'

					else:
						addr = line[1]					

					# print src:dst on first pass
					if (flag == False):
						trace.append(addr + ':' + dst + ' ')
						trace.append(addr + '-' + str(hop) + ' ')
						flag = True
						hop += 1

					else:
						trace.append(addr + '-' + str(hop) + ' ')

						# add to ip lists
						all_ips.append(addr)
						unique_ips.add(addr)

						# increment hop		
						hop += 1
		except:
			print "No Such File"
			print ' '



	# close nodelist				
	f.close()


	# open all_trace file
	with open("/home/jthom/iPlane/Data/all_traces_" + day + ".txt", "w") as f:

		# write list to file
		for item in all_traces:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open all_ip file
	with open("/home/jthom/iPlane/Data/all_ips_" + day + ".txt", "w") as f:

		# write list to file
		for item in all_ips:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_trace file
	with open("/home/jthom/iPlane/Data/unique_traces_" + day + ".txt", "w") as f:

		# write list to file
		for item in unique_traces:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_ip file
	with open("/home/jthom/iPlane/Data/unique_ips_" + day + ".txt", "w") as f:

		# write list to file
		for item in unique_ips:
			if not item:
				pass
			else:
				f.write(item + '\n')