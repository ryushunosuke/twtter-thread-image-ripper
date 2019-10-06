import requests
import os, sys
import pathlib
def MinReturner(Content):
	beg = Content.find(":")+2
	end = Content.find("\"",beg+1)
	return Content[beg:end]

#Returns image urls that you are most likely looking for within a thread to "<url> images.txt" and saves them into a folder
#Running the script will most likely look like this
#python tt.py twitter.com/somelink :orig /desiredfolder
if len(sys.argv) < 3 or len(sys.argv) >4:
	sys.exit("Invalid arguments have been passed.\nUse with <url> <endfix> <dir>\nExiting...")
if "-h" in sys.argv:
	print("Usage is tt.py <twitter thread url> [:small,:medium,:large,:orig] <directory>\nSaving profile media can't be used alongside giving directiories cause of lolcode")
else:
	ourURL = requests.get(sys.argv[1])
	beg = sys.argv[1].rfind("/")
	end = len(sys.argv[1])
if "-p" in sys.argv:
	ProfileRip = True
elif "-p" not in sys.argv:
	ProfileRip = False
try:
	if(len(sys.argv) == 4 and not "-p" in sys.argv):
		os.mkdir(sys.argv[3])
		os.chdir(os.path.join(os.getcwd(),sys.argv[3]))
	else:
		if "-p" in sys.argv:
			ProfileName = sys.argv[1][sys.argv[1].rfind("/",0, sys.argv[1].rfind("/") - 2)+1: sys.argv[1].rfind('/')]
			os.mkdir(ProfileName)
			os.chdir(os.path.join(os.getcwd(),ProfileName))
			
		if not "-p" in sys.argv:
			os.mkdir(sys.argv[1][beg+1:end])
			os.chdir(os.path.join(os.getcwd(),sys.argv[1][beg+1:end]))
except:
	print("Checking if folder exists.")
	try:
		if "-p" in sys.argv:
			ProfileName = sys.argv[1][sys.argv[1].rfind("/",0, sys.argv[1].rfind("/") - 2)+1: sys.argv[1].rfind('/')]
			os.chdir(os.path.join(os.getcwd(),ProfileName))
		else:
			os.chdir(os.path.join(os.getcwd(),sys.argv[1][beg+1:end]))

	except:
		sys.exit('Invalid dir.')
#workingDir = os.chdir(sys.argv[3])
if "-p" in sys.argv:
	output = open(ProfileName+" images.txt",'w')
else:
	output = open(sys.argv[1][beg+1:end]+" images.txt",'w')
d = {}
dSize = 0
data_max=""
for line in ourURL.iter_lines(): #Thread ripping
	line = line.decode("ascii","ignore")
	if (line.find("data-min-position=") != -1):
		data_max =line[line.find("data-min-position=")+19:line.find("\"",line.find("data-min-position=")+20)]
	if line.find(".jpg")!=-1 and line.find("data-image-url=") !=-1 or line.find("data-preview-image-src=") != -1 and line.find("profile_images") == -1:
		end = line.rfind("\"")
		beg = line.rfind("\"",0,end)
		if line[beg+1:end] not in d:
			d[line[beg+1:end]] = 1
			dSize+=1
		lastline = line
RipCount = 0
try:
	while (ProfileRip): #Profile ripping
		if data_max == "/script" or data_max == "ull,":
			break
		ProfileName = sys.argv[1][sys.argv[1].rfind("/",0, sys.argv[1].rfind("/") - 2)+1: sys.argv[1].rfind('/')]
		UpdateLink = "https://twitter.com/i/profiles/show/" + ProfileName + "/media_timeline?max_position=" + data_max
		print("ProfileName, UpdateLink:",ProfileName, UpdateLink)
		ourURL = requests.get(UpdateLink)
		for line in ourURL.iter_lines():
			line = line.decode("ascii","ignore")
			if line.find("min_position"):
				data_max = MinReturner(line)
			nindex = line.find("data-image-url=")
			if nindex > 0:
				while nindex > 0:
					beg = line.find("\"",nindex)
					end = line.find("\"",beg+1)
					Url = line[beg+1:end].replace("\\","")
					if Url not in d:
						d[Url] = 1
						dSize+=1
					nindex = line.find("data-image-url=",end)
except KeyboardInterrupt :
	print("Released from loop early.")
string = ""
pageOn = 1
for link in d.keys():
	string += link + sys.argv[2] +"\n"
print("Image count:", len(d))
output.write(string)
try:
	for link in d.keys():
			filename = link[link.rfind("/")+1:]
			link += sys.argv[2]
			OpenedFile = open(filename,"wb")
			OpenedFile.write(requests.get(link).content)
			OpenedFile.close()
except Exception as e:
	print(str(e))
		