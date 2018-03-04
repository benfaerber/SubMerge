# -*- coding: utf-8 -*-
import re, numpy, pprint
from operator import itemgetter
debug = True

# Unix line endings ftw
# Only tested with \n
lineEnding = "\n"
# Output name
out = "SubmergedSub.srt"

# Show the logo and display some information
print('''
	 _____       _    ___  ___                    
	/  ___|     | |   |  \/  |                    
	\ `--. _   _| |__ | .  . | ___ _ __ __ _  ___ 
	 `--. \ | | | '_ \| |\/| |/ _ \ '__/ _` |/ _ \\
	/\__/ / |_| | |_) | |  | |  __/ | | (_| |  __/
	\____/ \__,_|_.__/\_|  |_/\___|_|  \__, |\___|
	                                    __/ |     
	                                   |___/      
''')
print("Welcome to SubMerge! This is used to merge 2 srt files so you can watch in 2 languages at once.")
print("Useful for language learning, or if you need something shown to people of different linguistic backgrounds.")
print("By Benjamin Faerber 2018, Open source\n")

# Uses default file names unless not in debug mode
fileNames = ["eng.srt", "ger.srt"]
output = ""
if (debug):
	print("In Debug mode, no input required")
else:
	fileNames[0] = raw_input("File path to language 1: ")
	fileNames[1] = raw_input("File path to language 2: ")

print("Merging " + fileNames[0] + " and " + fileNames[1] + "...")

# Open files and decode them to unicode
# Alot of theses subtitle files use latin1 for some reason	
files = [
open(fileNames[0], "rb"),
open(fileNames[1], "rb")
]
read = [files[0].read().decode('latin1').encode('utf8'), files[1].read().decode('latin1').encode('utf8')]

# Unify the line endings
def uniLine(inp):	
	inp = inp.replace("\r\n", "LINE_ENDING")
	inp = inp.replace("\r", "LINE_ENDING")
	inp = inp.replace("\n", "LINE_ENDING")

	inp = inp.replace("LINE_ENDING", lineEnding)
	return inp
read[0] = uniLine(read[0])
read[1] = uniLine(read[1])

# Create a list line by line
data = [[], []]
data[0] = re.split(lineEnding, read[0])
data[1] = re.split(lineEnding, read[1])

# Is it a label line ex. 40
# It just has a number and no time
def isLabel(inputString):
	if (any(char.isdigit() for char in inputString)
		and not any(char.isalpha() for char in inputString)
		and ":" not in inputString
		and "-" not in inputString
		and "," not in inputString
		and "." not in inputString):
		return True
	return False

# Gets the first chunk of time out of a time string
# 00:03:29,459 --> 00:03:31,211
# turns into:
# 00:03:29,459
def pullTime(t):
	t = t.replace(lineEnding, "")
	c = t.split(" --> ")
	return c[0]

# Uses math and other jazz to turn a string time code into and integer for comparison
# 00:03:29,459 --> 00:03:31,211
# turns into 
# 2094
def timeCode(data):
	data = pullTime(data)
	div = 100
	ta = [
	(int(data[:2]) * 3600000) / div,
	(int(data[3:5]) * 60000) / div,
	(int(data[6:8]) * 1000) / div,
	(int(data[9:12]) / div)
	]

	tc = 0
	for t in ta:
		tc += t
	return tc

# This gets the amount of chunks in the files
co = [0, 0]
for y in range(0, len(data)):
	for x in range(0, len(data[y])):
		if (isLabel(data[y][x])):
			co[y] += 1

# This creates a new array to merge it into
comp = [""] * (co[0]+co[1])
for i in range(co[0]+co[1]):
	comp[i] = [""] * 3

# This parses the files and stores the chunks into the an array
ind = 0
for y in range(0, len(data)):
	for x in range(0, len(data[y])):
		if (isLabel(data[y][x])):
			comp[ind][0] = data[y][x+1]
			comp[ind][2] = timeCode(comp[ind][0])
			for j in range(2, 10):
				if (x+j+1 < len(data[y])):
					if (data[y][x+j] != ""):
						comp[ind][1] += data[y][x+j]
						if (data[y][x+j+1] != ""):
							comp[ind][1] += lineEnding
					else:
						break
				else:
					break
			ind += 1

# Sorts the array by time code
def take(elem):
    return elem[2]
comp.sort(key=take)

# Outputs to a new srt
file = open(out,"w") 
for x in range(0, len(comp)):
	file.write(str(x+1) + lineEnding)
	file.write(comp[x][0] + lineEnding)
	file.write(comp[x][1] + lineEnding + lineEnding) 
print("Done and outputted to " + out + "!")