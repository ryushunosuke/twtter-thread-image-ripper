import urllib.request
import urllib.parse
import urllib.error
import urllib.response
import numpy as np
import os, sys
import pathlib
import re
import cv2

#Returns image urls that you are most likely looking for within a thread to "<url> images.txt" and saves them into a folder
#Running the program will most likely look like this
#python tt.py twitter.com/somelink :orig /desiredfolder
if len(sys.argv) < 3 or len(sys.argv) >4:
	print("Invalid arguments have been passed.\nUse with <url> <endfix> <dir>\nExiting...")
elif x in sys.argv == "-h":
	print("Usage is tt.py <twitter thread url> [:small,:medium,:large,:orig] <directory>\n")
else:
	ourURL = urllib.request.urlopen(sys.argv[1])
	beg = sys.argv[1].rfind("/")
	end = len(sys.argv[1])
try:
	if(len(sys.argv) == 4):
		os.mkdir(sys.argv[3])
		os.chdir(os.path.join(os.getcwd(),sys.argv[3]))
		print(sys.argv[3])
	else:
		os.mkdir(sys.argv[1][beg+1:end])
		os.chdir(os.path.join(os.getcwd(),sys.argv[1][beg+1:end]))
		print(sys.argv[1][beg+1:end])
except:
	print("Checking if folder exists.")
	try:
		os.chdir(os.path.join(os.getcwd(),sys.argv[1][beg+1:end]))
	except:
		print("Invalid dir.")
	#workingDir = os.chdir(sys.argv[3])
	output = open(sys.argv[1][beg+1:end]+" images.txt",'w')
	d = {}
	dSize = 0
	for line in ourURL.readlines():
		line = line.decode("ascii","ignore")
		if line.find(".jpg")!=-1 and line.find("data-image-url=") != -1:
			end = line.rfind("\"")
			beg = line.rfind("\"",0,end)
			if line[beg+1:end] not in d:
				d[line[beg+1:end]] = 1
				dSize+=1
	string = ""
	pageOn = 1
	for link in d.keys():
		string += link + sys.argv[2] +"\n"

	output.write(string)
	for link in d.keys():
			filename = link[link.rfind("/")+1:]
			link += sys.argv[2]
			req = urllib.request.urlopen(link)
			arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
			img = cv2.imdecode(arr, -1)
			cv2.imwrite(filename, img)
			
