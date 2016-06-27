# import files
import sys
import os
import urllib
import tarfile
import re
import shutil

# iterate through all 30 days
for w in range(1, 3):
	# initialize lists and sets
	ip_all = []
	trace_all = []
	ip_unique = set()
	trace_unique = set()
	edgeList = set()

	# open files (works in layers)
	with open("/home/jay/M-Lab/april_" + str(w)) as url_list:
		for url in url_list:
			urllib.urlretrieve(url, "/home/jay/M-Lab/temp.tgz")
			tfile = tarfile.open("/home/jay/M-Lab/temp.tgz", "r:gz")
			tfile.extractall()
			for l1_filename in os.listdir("/home/jay/M-Lab/2016"):
				for l2_filename in os.listdir("/home/jay/M-Lab/2016/"+l1_filename):
					for l3_filename in os.listdir("/home/jay/M-Lab/2016/" + l1_filename+'/' + l2_filename):
						for l4_filename in os.listdir("/home/jay/M-Lab/2016/" + l1_filename+'/' + l2_filename + '/' + l3_filename):
							with open("/home/jay/M-Lab/2016/" + l1_filename +'/' + l2_filename + '/' + l3_filename + '/' + l4_filename, 'r') as f:

								# set variables, flags
								flag = 0
								hop = 1
								trace = []

								# iterate through inner file
								for line in f:

									# divide line into pieces
									line = line.split()

									# iterate through line to find line numbers
									for x in range(0, 31):
										try:
											# parse out src/dst on first pass
											if line[0] == 'traceroute' and flag == 0:
												flag = 1

												# src
												src = line[1]
												src = src.strip('[()')									
												src = src.split(':')
												src = src[0]

												# dst
												dst = line[3]
												dst = dst.strip('()],')
												dst = dst.split(':')
												dst = dst[0]

												# save src/dst
												ip_all.append(src + '\n')
												ip_all.append(dst + '\n')
												ip_unique.add(src + '\n')
												ip_unique.add(dst + '\n')

												# append to head of trace
												trace.append(src + ':' + dst)

											# catch each hop and strip extra characters
											if line[0] == str(x):
												if line[4] != None:
													address = line[4]
													address = address.strip('()')
													if ')' in address:
														head, sep, tail = address.separate(')')
														address = head

													# save ip's to appropriate list
													ip_all.append(address + '\n')
													ip_unique.add(address + '\n')

													# build string												
													trace.append(address + '-' + str(hop))

													# increment hop count
													hop += 1
										except:
											pass												

								# convert trace to string
								trace = ' '.join(trace)
								trace_all.append(trace + '\n')

								# append string to running list
							
								trace_unique.add(trace + '\n')

			# delete downloaded files each time
			if os.path.exists("/home/jay/M-Lab/2016"):
				shutil.rmtree("/home/jay/M-Lab/2016")

			if os.path.exists("/home/jay/M-Lab/temp.tgz"):
				os.remove("/home/jay/M-Lab/temp.tgz")

	# write data to files
	outfile = open("april_" + str(w) + "_all_ip", "w")
	for item in ip_all:
		outfile.write(item)
	outfile.close()

	outfile = open("april_" + str(w) + "_all_trace", "w")
	for item in trace_all:
		outfile.write(item)
	outfile.close()

	outfile = open("april_" + str(w) + "_unique_ip", "w")
	for item in ip_unique:
		outfile.write(item)
	outfile.close()

	outfile = open("april_" + str(w) + "_unique_trace", "w")
	for item in trace_unique:
		outfile.write(item)
	outfile.close()

	# get edges from unique trace list
	f = open("april_" + str(w) + "_unique_trace", "r")
	for item in f:

		# set list so it will reset
		trace = []

		# split trace and push to list
		for item in item.split():
			if ':' in item:
				pass
			else:
				item = item.split('-')
				trace.append(item[0])

		# find length of list
		length = len(trace)

		# set iterator variable so it will reset
		i = 0

		# iterate through trace list for pairs
		while i < length - 1:
			first = trace[i]
			second = trace[i+1]

			# add to edgeList set (unique values only)
			edgeList.add(str(first) + ' ' + str(second))
			i += 1


	# write edgeList to file
	out = open("april_" + str(w) + "_edge", "w")
	for item in edgeList:
		out.write(item + '\n')

	# close file
	f.close()
	out.close()

	# write stats
	outfile = open("april_" + str(w) + "_stats", "w")
	outfile.write("Total IP: " + str(len(ip_all)) + '\n')
	outfile.write("Unique IP: " + str(len(ip_unique)) + '\n')
	outfile.write("Total Trace: " + str(len(trace_all)) + '\n')
	outfile.write("Unique Trace: " + str(len(trace_unique)) + '\n')
	outfile.write("Unique Edge: " + str(len(edgeList)) + '\n')
	outfile.close()

	# clear lists
	del ip_all
	del trace_all
	del ip_unique
	del trace_unique
	del edgeList