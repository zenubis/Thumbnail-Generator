# Author: Nyon Yow Feng
# Created: 12-August-2018

import sys;
import os;
import glob;
import re;
import subprocess;


ffmpeg="C:\\ffmpeg-20180810-87cc7e8-win64-static\\bin\\ffmpeg.exe";

input_dir = input("Enter directory to generate thumbnails for: ");
input_dir = input_dir + os.sep + "*"


print("Scanning " + input_dir + " ...")

list_files = glob.glob(input_dir);

for file in list_files:
	if None != re.search(r'\.nfo *$', file): 
		# skip all .nfo files. we dont care about these
		continue;

	elif None != re.search(r'-thumb.jpg$', file):
		#skip also thumbnail files
		continue;

	#should be only video file when it reaches here
	print ("-->" + file);
	
	#contruct thumbnail filename
	thumbnail_filename = os.path.splitext(file)[0] + "-thumb.jpg";
	
	#check if corresponding thumb nail file exists or not
	if os.path.exists(thumbnail_filename):
		#has thumbnail already, skip
		continue;

	#print(thumbnail_filename)
	cmd="{2:s} -ss 0:10:00 -i \"{0:s}\" -vframes 1 -q:v 2 -vf scale=400:-1 \"{1:s}\"".format(file, thumbnail_filename, ffmpeg);
	print(cmd);
	subprocess.run(cmd, shell=True);

input("Press Enter key to continue");

#end of script
