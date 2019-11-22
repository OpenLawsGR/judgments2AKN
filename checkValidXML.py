# -*- coding: utf-8 -*-
import os
import fnmatch
from functions import CheckXMLvalidity
from lxml import etree

# Folder where judgments
BASE_XML_FOLDER =  os.path.join(os.getcwd(), 'XML')

# Declare folder name
FOLDER_PATH = r'ste/2013'

# Define folder path that parsing will start from 
SRC = os.path.join(BASE_XML_FOLDER, FOLDER_PATH)

if __name__ == '__main__':
    print "Starting validation in : " + SRC
    validXML = 0
    nonValidXML = 0
    XmlFiles = 0
    filesCnt = 0
    for root, dirs, files in os.walk(SRC):  
        for name in files:
            filesCnt += 1
            if fnmatch.fnmatch(name, '*.xml'):
                #print  name
                XmlFiles += 1
                if CheckXMLvalidity('akomantoso30.xsd', os.path.join(root, name)) == 1:
                    #print name + ": Valid"
                    validXML += 1
                else:
                    #print name + ": Not Valid"
                    nonValidXML +=1
    
    print "Total Files :" + str(filesCnt)
    print "Total XML Files :" + str(XmlFiles)
    print "Valid XML :" + str(validXML)
    print "Non Valid XML : " + str(nonValidXML)
