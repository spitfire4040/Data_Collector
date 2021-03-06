# import files
import sys
import os
import os.path
import urllib
import gzip


# get day from command line args
day = sys.argv[1]
month = sys.argv[2]
year = sys.argv[3]

# initialize node list
nodelist = []


def parse():

	# initialize global variables
	global day, month, year

	# open nodelist file
	f = open("/home/jay/Desktop/Data_Collector/ark_nodes.txt", "r")

	# read nodes into list
	for item in f:
		nodelist.append(item)
	f.close()

	# re-initialize variables each time (clear)
	trace = []

	all_trace = []
	unique_trace = set()

	all_ip = []
	unique_ip = set()

	edgeList = set()

	src = ''
	dst = ''
	hop = ''
	ip = ''
	addr = ''

	starCounter = 1
	count = 1

	# check for directories and create if necessary
	if not os.path.exists("/home/jay/Desktop/Data_Collector/ArkData"):
		os.makedirs("/home/jay/Desktop/Data_Collector/ArkData")

	if not os.path.exists("/home/jay/Desktop/Data_Collector/processing"):
		os.makedirs("/home/jay/Desktop/Data_Collector/processing")

	# open files for write
	out1 = open("/home/jay/Desktop/Data_Collector/ArkData/all-traces.txt", "w")
	out2 = open("/home/jay/Desktop/Data_Collector/ArkData/unique-traces.txt", "w")
	out3 = open("/home/jay/Desktop/Data_Collector/ArkData/all-ip.txt", "w")
	out4 = open("/home/jay/Desktop/Data_Collector/ArkData/unique-ip.txt", "w")
	out5 = open("/home/jay/Desktop/Data_Collector/ArkData/unique-edge.txt", "w")
	out6 = open("/home/jay/Desktop/Data_Collector/ArkData/stats.txt", "w")

	# iterate through each team
	for x in range(1, 4):

		# cycle through each file for team/day
		for item in nodelist:


			item = item.strip('\n')

			# set file name
			filename = "https://topo-data.caida.org/team-probing/list-7.allpref24/team-" + str(x) + "/daily/" + year + "/cycle-" + year + month + day + "/daily.l7.t1.c004461." + year + month + day + "." + item + ".warts.gz"

			# print filename for visual affirmation
			print filename



			# retrieve file
			urllib.urlretrieve(filename, "/home/jay/Desktop/Data_Collector/processing/temp.gz")	

			# open in and out files for .gz processing
			in_file = gzip.open("/home/jay/Desktop/Data_Collector/processing/temp.gz", "rb")
			s = in_file.read()

			out_file = open("/home/jay/Desktop/Data_Collector/processing/temp.warts", "wb")
			out_file.write(s)

			in_file.close()
			out_file.close()							
			"""

			# open file for read
			f = open("/home/jthom/Ark/ark-data/day-" + str(y) + "/" + filename, "r")
			try:
				# iterate through each line
				for line in f:

					# split line into pieces
					line = line.split()

					# build trace string (line not traceroute)
					if line[0] != 'traceroute':
						hop = line[0]
						ip = line[1]
						addr = ip + '-' + hop + ' '
						trace.append(addr)
						all_ip.append(ip)
						unique_ip.add(ip)

					# reset and append running list each time line == traceroute
					if line[0] == 'traceroute':

						# get values for src, dst
						src = line[2]
						dst = line[4]

						all_ip.append(src)
						all_ip.append(dst)
						unique_ip.add(src)
						unique_ip.add(dst)

						# check for empty list and append if good
						if not trace:
							pass
						else:

							# eliminate trailing '*'s
							while '*' in trace[-1]:
								del(trace[-1])

							# convert list to string
							trace = ''.join(trace)

							# append string to running lists
							all_trace.append(trace)
							unique_trace.add(trace)

						# reset trace
						trace = []

						# append src, dst to new trace
						trace.append(src + ':' + dst + ' ')

			except:
				pass

			# once more at end to catch last trace
			try:
				# eliminate trailing '*'s
				while '*' in trace[-1]:
					del(trace[-1])

				# convert list to string
				trace = ''.join(trace)

				# append string to running lists
				all_trace.append(trace)
				unique_trace.add(trace)
			except:
				pass

			f.close()
			"""




	"""
	# find edges...
	# iterate through unique traces
	for item in unique_trace:

		# set list so it will reset
		trace = []

		# split trace and push to list
		for item in item.split():
			if (':' in item):
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

			# set incrementing value for 0's
			if first == '*' and second == '*':
				# don't count * - *
				pass

			else:

				if first == '*':
					first = count
					count += 1

				if second == '*':
					second = count
					count += 1

			# add to edgeList set (unique values only)
			edgeList.add(str(first) + ' ' + str(second))
			i += 1


	# write all_trace to file
	for item in all_trace:
		out1.write(item)
		out1.write('\n')

	# write unique_trace to file
	for item in unique_trace:
		out2.write(item)
		out2.write('\n')

	# write all_ip to file
	for item in all_ip:
		out3.write(item)
		out3.write('\n')

	# write unique_ip to file
	for item in unique_ip:
		out4.write(item)
		out4.write('\n')

	# write edgelist to file
	for item in edgeList:
		out5.write(item)
		out5.write('\n')

	# write stats
	out6.write("Total IP: " + str(len(all_ip)) + '\n')
	out6.write("Unique IP: " + str(len(unique_ip)) + '\n')
	out6.write("Total Trace: " + str(len(all_trace)) + '\n')
	out6.write("Unique Trace: " + str(len(unique_trace)) + '\n')
	out6.write("Unique Edge: " + str(len(edgeList)) + '\n')

	# close files
	out1.close()
	out2.close()
	out3.close()
	out4.close()
	out5.close()
	out6.close()
	"""

def main(argv):
	# run parse
	parse()


	# trace count
	#os.system("./tracecount")

	# ip count
	#os.system("./ipcount")


if __name__ == '__main__':
  main(sys.argv)