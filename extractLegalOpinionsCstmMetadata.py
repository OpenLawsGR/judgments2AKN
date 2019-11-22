# -*- coding: utf-8 -*-
import os
import sys
import fnmatch
import requests
from functions import extractDataFromRequests
from lxml import etree

# Folder where legal opinions are stored
BASE_FOLDER =  os.path.join(os.getcwd(), 'pdftotext')
# Declare metadata folders
NSK_META_FOLDER = os.path.join(BASE_FOLDER, 'nsk_metadata')
# Declare folder name
FOLDER_PATH = 'nsk'
# Define folder path that parsing will start from 
SRC = os.path.join(BASE_FOLDER, FOLDER_PATH)

if __name__ == '__main__':

    # Create custom metadata folder if it does not exist
    if not os.path.exists(os.path.join(BASE_FOLDER, 'nsk_custom_metadata')):
        os.makedirs(os.path.join(BASE_FOLDER, 'nsk_custom_metadata'))

    for root, dirs, files in os.walk(SRC):
        for name in files:
            if fnmatch.fnmatch(name, '*.txt'):
                print name
                # check metadata folder to get post parameters
                metaFileExists = os.path.isfile(os.path.join(NSK_META_FOLDER, name))
                if metaFileExists:
                    with open(os.path.join(NSK_META_FOLDER, name), 'r') as fin:
                        #print name
                        XML = etree.parse(fin)
                        #print XML.getroot().nsmap
                        XMLroot = XML.getroot()
                        #print list(root.nsmap.values())[0]
                        ns = list(XMLroot.nsmap.values())[0]
                        protocolNumber = XML.findtext('//ns:protocolNumber', namespaces={'ns' : ns})
                        issueDate = XML.findtext('//ns:issueDate', namespaces={'ns' : ns})
                    try:
                        issueYear = protocolNumber.split('/')[1]
                    except IndexError:
                        issueYear = issueDate.split('-')[0]
                    decisionNumber = protocolNumber.split('/')[0]
                    #print issueYear
                    #print decisionNumber

                    # Create POST url (based in NSK search form) and POST data
                    post_url = 'http://www.nsk.gr/web/nsk/anazitisi-gnomodoteseon'
                    post_url +='?p_p_id=nskconsulatories_WAR_nskplatformportlet&'
                    post_url +='p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&'
                    post_url +='p_p_col_id=column-4&p_p_col_pos=2&p_p_col_count=3'
                    #print post_url
                    post_data = {"_nskconsulatories_WAR_nskplatformportlet_isSearch" : "1",
                        "_nskconsulatories_WAR_nskplatformportlet_inputSuggestionNo" : decisionNumber,
                         "_nskconsulatories_WAR_nskplatformportlet_inputDatefrom" : issueYear,
                        "_nskconsulatories_WAR_nskplatformportlet_consulState":"null"}
                
                    extractedData = extractDataFromRequests(post_url, post_data)
                    #print extractedData
                    # Create a custom element that will hold extracted data
                    customMetadata = etree.Element("customMetadata")
                    keywords = etree.SubElement(customMetadata, 'keywords')
                    cnt = 0
                    for keyword in extractedData['keywords']:
                        # If its is not empty string
                        if keyword:
                            cnt += 1
                            keywordElem = etree.SubElement(keywords, 'keyword_'+str(cnt))
                            keywordElem.text = keyword.strip()

                    chairman = etree.SubElement(customMetadata, 'chairman')
                    chairman.text = extractedData['chairman']
                    rapporteur = etree.SubElement(customMetadata, 'rapporteur')
                    rapporteur.text = extractedData['rapporteur']
                    status = etree.SubElement(customMetadata, 'status')
                    status.text = extractedData['status']

                    #print etree.tostring(customMetadata,pretty_print=True, encoding="UTF-8")
                    XmlTree = etree.ElementTree(customMetadata)

                    # Write ElementTree to file
                    with open(os.path.join(os.path.join(BASE_FOLDER, 'nsk_custom_metadata'), name), 'w') as fin:
                        fin.write(etree.tostring(XmlTree, pretty_print=True, encoding="UTF-8", xml_declaration =True))
