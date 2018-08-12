# Author: Nyon Yow Feng
# Created: 12-August-2018
# Author: Nyon Yow Feng
# Created: 12-August-2018

import os;
import glob;
import re;
import xml.dom.minidom;


ffmpeg="C:\\ffmpeg-20180810-87cc7e8-win64-static\\bin\\ffmpeg.exe";

input_dir = input("Enter directory to generate thumbnails for:");
input_dir = input_dir + os.sep + "*"

print("Scanning " + input_dir + " ...")

list_files = glob.glob(input_dir);

for file in list_files:
	result = re.search(r's(\d+)e(\d+).*\.nfo *$', file)
	if None == result: 
		# skip all files except .nfo files
		continue;


	#should be only video file when it reaches here
	print ("-->" + file);
	#print ("s" + result.group(1) + ", e" + result.group(2));

	DOMTree = xml.dom.minidom.parse(file)
	if None == DOMTree:
		# not a valid xml file?
		continue;

	docelement = DOMTree.documentElement;
	if "episodedetails" == docelement.tagName:
		#get titles
		edelement = docelement.getElementsByTagName("title");
		if None != edelement:
			# remove all node
			hasUpdates = False;
			for node in edelement:
				#print("number of childs:" + str(node.childNodes.length))
				for child in node.childNodes:
					if child.nodeType == xml.dom.minidom.Node.TEXT_NODE:
						node.removeChild(child);
						node.appendChild(DOMTree.createTextNode("第 {0:d} 集".format(int(result.group(2)))));
						hasUpdates = True;
						break;
			# update changes back into xml file
			if hasUpdates:
				with open(file, "w") as fp:
					docelement.writexml(fp);		

input("Press Enter key to continue");

#end of script
