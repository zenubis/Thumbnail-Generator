# Author: Nyon Yow Feng
# Created: 12-August-2018
# Author: Nyon Yow Feng
# Created: 12-August-2018

import os;
import glob;
import re;
import xml.dom.minidom;

import os
script_dir = (os.path.dirname(os.path.realpath(__file__)));

input_dir = input("Enter directory to generate thumbnails for: ");
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
		updateText = "第 {0:d} 集".format(int(result.group(2)));
		edelement = docelement.getElementsByTagName("title");
		needUpdate = True;
		if None != edelement:
			# remove all node
			for node in edelement:
				#print("number of childs:" + str(node.childNodes.length))
				for child in node.childNodes:
					if child.nodeType == xml.dom.minidom.Node.TEXT_NODE:
						# check if the node that we're trying to add exists or not
						if re.search(updateText, child.nodeValue) != None:
							needUpdate = False; #exists, no need to update the file
							break;	
						node.removeChild(child);


			if not needUpdate:
				continue;

			# append our own text
			node.appendChild(DOMTree.createTextNode(updateText));
			
			# update changes back into xml file
			try:
				with open(file, "w") as fp:
					docelement.writexml(fp);	
			except PermissionError as e:
				# create a new file at the script directory
				print("Unable to update original files, updated file created instead.")
				newfile = script_dir + os.sep + os.path.basename(file)
				with open(newfile, "w") as fp:
					docelement.writexml(fp);
					


input("Press Enter key to continue");

#end of script
