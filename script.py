import csv
import math
import srt
from pexif import JpegFile
from os import listdir
from os.path import isfile, join

# calculates the distance between point x and image
# from the images folder. Check whether it is in the
# reqired radius provide as parameter.
def calculateDistance( x,radius ):
	mypath = "images/"
	arr = []
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	for f in onlyfiles:
		# pexif package used to extract geo data from image
		lf = JpegFile.fromFile("images/"+f)
		ef = lf.get_geo()
		lat = abs(ef[1] - x[0])
		long = abs(ef[0] - x[1])
		# here dist is in meters
		dist = pow(10,5) * math.sqrt(pow(lat,2)+pow(long,2))
		if(dist < radius):
			print f
			arr.append(f)
	# returning a list of images names
	return arr

# Generates a csv file for every second of the 
# drone path along with list of images taken
# in a particular radius from a point.
def distanceFromSrtFile(srt_file):
	# srt package used to read a srt file
	subs = list(srt.parse(srt_file))
	csvfile = open("results.csv",'wb')
	csvwriter = csv.writer(csvfile, delimiter=";")
	for idx in subs:
		latLong = idx.content
		triplets = latLong.encode('ascii','ignore')
		lat,lng,zero = triplets.split(",")
		lat = float(lat)
		lng = float(lng)
		point = tuple([lat,lng])
		strName = str(idx.start)
		pics = calculateDistance(point,35)
		# csvwriter.writerow([strName,pics])

# Generates a csv file for every area
# mentioned in a csv file along with a 
# list of images taken in a particular
# radius from a point.
def distanceFromCsvFile(csv_file):
	# csv package used to read csv file
	csvreader = csv.reader(csv_file,delimiter=',')
	csv2file = open("results2.csv","wb")
	csv2writer = csv.writer(csv2file, delimiter=";")
	for row in csvreader:
		# condition to skip the header if present
		if row[0] == "asset_name":
			continue
		lat = float(row[1])
		lng = float(row[2])
		point = tuple([lat,lng])
		print row[0]
		dest = calculateDistance(point,50)
		csv2writer.writerow([row[0],dest])

srtFile = open('videos/DJI_0301.SRT','r').read()
distanceFromSrtFile(srtFile)

csvFile = open("assets.csv","rb")
distanceFromCsvFile(csvFile)
