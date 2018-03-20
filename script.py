import csv
import math
import srt
from pexif import JpegFile
from os import listdir
from os.path import isfile, join

def calculateDistance( x,radius ):
	mypath = "images/"
	arr = []
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	for f in onlyfiles:
		lf = JpegFile.fromFile("images/"+f)
		ef = lf.get_geo()
		lat = abs(ef[1] - x[0])
		long = abs(ef[0] - x[1])
		dist = pow(10,5) * math.sqrt(pow(lat,2)+pow(long,2))
		if(dist < radius):
			print f
			arr.append(f)
			# print dist
	return arr

def distanceFromSrtFile(srt_file):
	subs = list(srt.parse(srt_file))
	csvfile = open("results.csv",'wb')
	csvwriter = csv.writer(csvfile, delimiter=";")
	for idx in subs:
		# print idx.index
		latLong = idx.content
		triplets = latLong.encode('ascii','ignore')
		lat,lng,zero = triplets.split(",")
		lat = float(lat)
		lng = float(lng)
		point = tuple([lat,lng])
		print str(idx.index)+"------"+str(idx.start)+"-------"+str(idx.end)
		strName = str(idx.start)
		pics = calculateDistance(point,35)
		# csvwriter.writerow([strName,pics])

def distanceFromCsvFile(csv_file):
	csvreader = csv.reader(csv_file,delimiter=',')
	csv2file = open("results2.csv","wb")
	csv2writer = csv.writer(csv2file, delimiter=";")
	for row in csvreader:
		if row[0] == "asset_name":
			continue
		lat = float(row[1])
		lng = float(row[2])
		point = tuple([lat,lng])
		print row[0]
		dest = calculateDistance(point,50)
		csv2writer.writerow([row[0],dest])

point_csv = (73.0049496892297,19.15211247589279)
point_srt = (73.00135763743417,19.149798647687)
#calculateDistance(point_srt) 

# srtFile = open('videos/DJI_0301.SRT','r').read()
# distanceFromSrtFile(srtFile)

csvFile = open("assets.csv","rb")
distanceFromCsvFile(csvFile)
