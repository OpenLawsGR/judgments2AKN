# -*- coding: utf-8 -*-
import os
import re
import datetime
import sys
import codecs
import logging
import logging.handlers
import fnmatch
import time
from antlr4 import *
from antlr4.tree.Trees import Trees
from lxml import etree
from AknJudgementClass import AknJudgementXML
from AknLegalReferencesClass import AknLegalReferences
from functions import validateXML, findDatesOfInterest
from functions import setupLogger, fixStringXML, CheckXMLvalidity
from variables import *
from grammars.gen.Legal_refLexer import Legal_refLexer
from grammars.gen.Legal_refParser import Legal_refParser
from grammars.gen.Legal_refListener import Legal_refListener
from grammars.gen.Legal_refVisitor import Legal_refVisitor
from grammars.gen.LegalOpinionLexer import LegalOpinionLexer
from grammars.gen.LegalOpinionParser import LegalOpinionParser
from grammars.gen.LegalOpinionListener import LegalOpinionListener

# Folder where legal opinions are stored
BASE_FOLDER =  os.path.join(os.getcwd(), 'pdftotext')

# Folder path where logs are stored
LOGS_FOLDER = os.path.join(os.getcwd(), 'logs')

# Folder path where XML are stored
XML_FOLDER = os.path.join(os.getcwd(), 'XML')

# Folder path where XML without NER files are stored
XML_NO_NER_FOLDER = os.path.join(os.getcwd(), 'XML_NO_NER')

# Declare folder name
START_FOLDER = r'nsk_no_garbage'
START_FOLDER_TEXT = r'nsk'
# Define folder path that parsing will start from 
SRC = os.path.join(BASE_FOLDER, START_FOLDER)

# Define NER folder path
NER_FOLDER = 'NER_final_results'

# Declare metadata folders
NSK_META_FOLDER = os.path.join(BASE_FOLDER, 'nsk_metadata')
NSK_CUSTOM_METADATA_FOLDER = os.path.join(BASE_FOLDER, 'nsk_custom_metadata')

# This is used for statistics purposes (time calculate, XML validation etc.)
general_LOG_file = 'statistics_LegalOpinions.txt'

if __name__ == '__main__':

    # Create regex objext for councilConferenceDate
    councilConferenceDateObj = re.compile(councilConferenceDatePattern)
    # Create regex objext for opinionSignatureDate
    opinionSignatureDateObj = re.compile(opinionSignatureDatePattern)
    # Create regex objext for fix XML string
    paragraphPatternObj = re.compile(paragraphPattern)

    if len(sys.argv) != 2:
        filename = '*.txt'
    else :
        filename = sys.argv[1]
        
    #folder = os.path.basename(SRC)
    #print "Folder: " + folder
    #print "Full path folder: " + SRC
    #sys.exit()

    for root, dirs, files in os.walk(SRC):
        # Create LOG folder if it does not exist
        if not os.path.exists(os.path.join(LOGS_FOLDER, START_FOLDER_TEXT)):
            #print "Creating Logs folder..."
            os.makedirs(os.path.join(LOGS_FOLDER, START_FOLDER_TEXT))

        # Create XML folder if it does not exist
        if not os.path.exists(os.path.join(XML_FOLDER, START_FOLDER_TEXT)):
            #print "Creating XML folder..."
            os.makedirs(os.path.join(XML_FOLDER, START_FOLDER_TEXT))

        # Create XML without NER folder if it does not exist
        if not os.path.exists(os.path.join(XML_NO_NER_FOLDER, START_FOLDER_TEXT)):
            #print "Creating XML without NER folder..."
            os.makedirs(os.path.join(XML_NO_NER_FOLDER, START_FOLDER_TEXT))


        for name in files:
            if fnmatch.fnmatch(name, filename):
                print "Legal Opinion: " + name
                global is_valid
                is_valid = False
                try:
                    start_time = time.clock()

                    # Foreach Legal Opinion create a corresponding log, XML and text filenames
                    #log_file = os.path.join(os.path.join(LOGS_FOLDER, START_FOLDER_TEXT), name)
                    xml_file = os.path.join(os.path.join(XML_FOLDER, START_FOLDER_TEXT), name.split('.')[0] + '.xml')
                    xml_file_NO_NER = os.path.join(os.path.join(XML_NO_NER_FOLDER, START_FOLDER_TEXT), name.split('.')[0] + '.xml')
                    text_file = os.path.join(os.path.join(XML_FOLDER, START_FOLDER_TEXT), name.split('.')[0] + '.txt')
                    text_file_NO_NER = os.path.join(os.path.join(XML_NO_NER_FOLDER, START_FOLDER_TEXT), name.split('.')[0] + '.txt')
                    # Declare Gate XML file where named entities are stored
                    GateXml_file = os.path.join(os.path.join(os.path.join(BASE_FOLDER, NER_FOLDER), os.path.basename(START_FOLDER_TEXT)), name + '.xml')
                    #print log_file
                    #print xml_file
                    #print text_file
                    #print GateXml_file
                    
                    # Setup a logger
                    #Akn_LOGGER = setupLogger('Akn_LOGGER', log_file)
                    #Akn_LOGGER.info('Converting %s', name)
                    
                    ######################## METADATA ##########################################
                    # Dictionary of metadata
                    # Usually metadata comes from external filles or could be extracted from legal text later
                    meta = {}
                    meta['textType'] = "judgment/advisoryOpinion"
                    meta['author'] = "#legalCouncilOfState"
                    meta['foreas'] = "legalCouncilOfState"
                    
                    # Check if metadata file exists in NSK_META_FOLDER
                    metaFileExists = os.path.isfile(os.path.join(NSK_META_FOLDER, name))
                    #print metaFileExists
                    
                    if metaFileExists:
                        with open(os.path.join(NSK_META_FOLDER, name), 'r') as fin:
                            #print name
                            XML = etree.parse(fin)
                            #print XML.getroot().nsmap
                            XMLroot = XML.getroot()
                            #print list(root.nsmap.values())[0]
                            ns = list(XMLroot.nsmap.values())[0]
                            ada = XML.findtext('//ns:ada', namespaces={'ns' : ns})
                            status = XML.findtext('//ns:status', namespaces={'ns' : ns})
                            summary = XML.findtext('//ns:subject', namespaces={'ns' : ns})
                            protocolNumber = XML.findtext('//ns:protocolNumber', namespaces={'ns' : ns})
                            publishTimestamp = XML.findtext('//ns:publishTimestamp', namespaces={'ns' : ns})
                            issueDate = XML.findtext('//ns:issueDate', namespaces={'ns' : ns})
                            try:
                                publicationDatetimeObj = datetime.datetime.strptime(publishTimestamp[0:-6], '%Y-%m-%dT%H:%M:%S.%f')
                                publicationDate = str(publicationDatetimeObj.date())
                                #print type(publicationDate)
                            except:
                                #print("Time data does not match format '%Y-%m-%dT%H:%M:%S.%f - " + "issueDate will be used")
                                try:
                                    publicationDatetimeObj = datetime.datetime.strptime(issueDate[0:-6], '%Y-%m-%d')
                                    publicationDate = str(publicationDatetimeObj.date())
                                except:
                                    publicationDate = None
                    
                    # Fill other metadata tha will be used to create FRBR elements
                    meta['issueYear'] = protocolNumber.split('/')[1]
                    meta['decisionNumber'] = protocolNumber.split('/')[0]
                    meta['publicationDate'] = publicationDate
                    meta['ada'] = ada
                    meta['summary'] = re.sub('\n\s*', '', summary, re.DOTALL)
                    
                    # Custom metadata can be found in NSK_CUSTOM_METADATA_FOLDER
                    # Check if file exists
                    cstmMetadataFileExists = os.path.isfile(os.path.join(NSK_CUSTOM_METADATA_FOLDER, name))
                    #print cstmMetadataFileExists
                    if cstmMetadataFileExists:
                        keywordsArray = []
                        elementTree = etree.parse(os.path.join(NSK_CUSTOM_METADATA_FOLDER, name))
                        chairman = elementTree.findtext('//chairman')
                        rapporteur = elementTree.findtext('//rapporteur')
                        status = elementTree.findtext('//status')
                        for elem in elementTree.findall('//keywords/'):
                            keywordsArray.append(elem.text)

                    # Populate other metadata
                    meta['keywords'] = keywordsArray
                    meta['chairman'] = chairman
                    meta['rapporteur'] = rapporteur
                    meta['status'] = status
                    
                    # Create AknJudgementXML object
                    judgmentObj = AknJudgementXML(
                        textType = meta['textType'],
                        author = meta['author'],
                        foreas = meta['foreas'],
                        issueYear = meta['issueYear'],
                        decisionNumber = meta['decisionNumber'],
                        publicationDate = meta['publicationDate'],
                        ada = meta['ada'],
                        status = meta['status'],
                        summary = meta['summary'],
                        keywords = meta['keywords'],
                        chairman = meta['chairman'],
                        rapporteur = meta['rapporteur']
                        )

                    # Create "meta" node
                    judgmentObj.nsmap['openlawsgr'] = "http://openlawsgr/proprietary"
                    metaElem = judgmentObj.createMeta()
                    #print(etree.tostring(metaElem, pretty_print=True, encoding="UTF-8", xml_declaration =True))

                    # Populate reference node with Named Entities based on Gate XML file
                    if os.path.isfile(GateXml_file):
                        #print "Gate XML file exists"
                        referencesNode = metaElem.find('references')
                        if referencesNode is not None:
                            referencesNodeIndex = metaElem.getchildren().index(referencesNode)
                            #print referencesNodeIndex
                            newReferencesNode = judgmentObj.modifyReferencesFromGateXml(GateXml_file, referencesNode)
                            #print(etree.tostring(newReferencesNode, pretty_print=True, encoding="UTF-8", xml_declaration =True))
                            metaElem.remove(referencesNode)
                            metaElem.insert(referencesNodeIndex, newReferencesNode)
                    #print(etree.tostring(metaElem, pretty_print=True, encoding="UTF-8", xml_declaration =True))
                    #sys.exit()
                    ############################### END METADATA ##################################

                    ########################### LEGAL REFERENCES ###################################
                    #print 'Parsing legal references...'
                    finput = FileStream(os.path.join(SRC, name), encoding='utf-8')
                    lexer = Legal_refLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = Legal_refParser(stream)
                    tree = parser.legal_text()
                    answer = AknLegalReferences().visit(tree)
                    #print(answer)
                    ########################### END LEGAL REFERENCES ###############################

                    ############################# STRUCTURE #######################################
                    #print 'Creating judgment structure...'
                    #Akn_LOGGER.info('Creating judgment structure...')
                    finput = InputStream(answer)
                    #finput = FileStream(os.path.join(SRC, name), encoding='utf-8')
                    lexer = LegalOpinionLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = LegalOpinionParser(stream)
                    tree = parser.judgment()
                    walker = ParseTreeWalker()
                    walker.walk(judgmentObj, tree)
                    ############################## END STRUCTURE ####################################
        
                    judgmentObj.text = re.sub(r'@', '', judgmentObj.text, flags=re.DOTALL)
                    #print judgmentObj.text

                    ############################ Named Entities in text #################################
                    if os.path.isfile(GateXml_file):
                        judgmentObj.text = judgmentObj.createNamedEntitiesInText(GateXml_file, judgmentObj.text)
                    ################################################################################
                    #print judgmentObj.text

                    # Define a custom namespace uri
                    judgmentObj.nsmap['openlawsgr'] = "http://openlawsgr/proprietary"
                    #print judgmentObj.nsmap

                    # Create AkomaNtoso Root element
                    akomaNtosoElem = judgmentObj.createAkomaNtosoRoot()

                    # This is due to cases where a ref tag does not close before the end tag of a paragraph (<p><ref></p></ref>)
                    judgmentObj.text =fixStringXML(judgmentObj.text, paragraphPatternObj)

                    try:
                        # Create judgment element based on parser and append to root
                        #Akn_LOGGER.info('Transforming to XML element...')

                        # etree.fromstring is being used it will change range ids character '>' to &gt; 
                        judgmentElem = judgmentObj.XML()
                        
                        #print etree.tostring(judgmentElem, pretty_print=True, encoding="UTF-8",
                        #         xml_declaration =True)
                        akomaNtosoElem.insert(0, judgmentElem)

                        # Find judgment node and insert metaElement
                        judgmentNode = akomaNtosoElem.find("judgment")
                        judgmentNode.insert(0, metaElem)
                        #print(etree.tostring(akomaNtosoElem, pretty_print=True, encoding="UTF-8", xml_declaration =True))
                        
                        # Specific nodes that will be used after
                        headerNode = akomaNtosoElem.xpath("/akomaNtoso/judgment/header")
                        conclusionsNode = akomaNtosoElem.xpath("/akomaNtoso/judgment/conclusions")
                        references = metaElem.xpath("/akomaNtoso/judgment/meta/references")

                        # Dates of interest can be found in specific elements in a Legal Opinion - find nodes
                        #Akn_LOGGER.info('Searching for dates of interest...')
                        ################################# councilConferenceDate ##########################################
                        # councilConferenceDate can be found on header element of AkomaNtoso structure
                        if headerNode:
                            newHeaderNode = findDatesOfInterest(headerNode[0], councilConferenceDateObj, 'councilConferenceDate', meta['author'])
                            if newHeaderNode is not None:
                                if references is not None:
                                    references[0].append(newHeaderNode[2])
                        ###############################################################################################

                        ################################ opinionSignatureDate ############################################
                        # opinionSignatureDate can be found on conclusions element of Akomantoso structure
                        if conclusionsNode:
                            newConclusionsNode = findDatesOfInterest(conclusionsNode[0], opinionSignatureDateObj, 'opinionSignatureDate', meta['author'])

                            if newConclusionsNode is not None:
                                if references is not None:
                                    references[0].append(newConclusionsNode[2])
                        ##############################################################################################
                        #Akn_LOGGER.info('Stop searching for dates of interest...')
                        
                        # Create the corresponding ElementTree object
                        XmlTree = etree.ElementTree(akomaNtosoElem)
                        #print(etree.tostring(akomaNtosoElem, pretty_print=True, encoding="UTF-8", xml_declaration =True))

                        # Open the XML file and append elementTree to it
                        #Akn_LOGGER.info('Creating XML file...')
                        # Problem with href range_id cannot retain '>' character, so write string tree representation to file
                        with codecs.open(xml_file, "w") as fin:
                            fin.write(etree.tostring(XmlTree, pretty_print=True, encoding="UTF-8",
                                 xml_declaration =True).replace('&gt;', '>'))

                        ########## copy XML tree and save it without including NER #####################################
                        rootNode = XmlTree.getroot()
                        for child in rootNode.xpath("./judgment/meta/references"):
                            for  child_lv2 in child:
                                if child_lv2.tag == 'TLCOrganization' or child_lv2.tag == 'TLCPerson' or child_lv2.tag == 'TLCLocation':
                                    #print child_lv2
                                    child_lv2.getparent().remove(child_lv2)

                        XmlTreeStr_NO_NER = etree.tostring(XmlTree, pretty_print=True, encoding="UTF-8", xml_declaration =True)
                        XmlTreeStr_NO_NER = re.sub(r'[<]/?organization.*?[>]', '', XmlTreeStr_NO_NER, flags = re.DOTALL)
                        XmlTreeStr_NO_NER = re.sub(r'[<]/?person.*?[>]', '', XmlTreeStr_NO_NER, flags = re.DOTALL)
                        XmlTreeStr_NO_NER = re.sub(r'[<]/?location.*?[>]', '', XmlTreeStr_NO_NER, flags = re.DOTALL)
                        #print XmlTreeStr_NO_NER
                        # etree.fromstring is being used it will change range ids character '>' to &gt; 
                        XmlElement_NO_NER = etree.fromstring(XmlTreeStr_NO_NER)
                        #print XmlElement_NO_NER
                        XmlTree_NO_NER = etree.ElementTree(XmlElement_NO_NER)
                        #print XmlElement_NO_NER
                        with codecs.open(xml_file_NO_NER, "w") as fin:
                             fin.write(etree.tostring(XmlTree_NO_NER, pretty_print=True, encoding="UTF-8",
                                 xml_declaration =True).replace('&gt;', '>'))
                        #######################################################################################

                        # Validation
                        #validateXML ('akomantoso30.xsd', xml_file, log_file)
                        is_valid = CheckXMLvalidity('akomantoso30.xsd', xml_file)
                        #logging.shutdown()
        
                    except etree.XMLSyntaxError:
                        #print "test"
                        # Something went wrong write the corresponding XML string to a .txt file
                        #Akn_LOGGER.info('Could not create XML element from string! Check validity!')
                        with open(text_file, "w") as fin:
                            fin.write(judgmentObj.text)

                        with open(text_file_NO_NER, "w") as fin:
                            fin.write(judgmentObj.text)
                            #logging.shutdown()

                except KeyboardInterrupt:
                    raise

                except Exception as e:
                    #print(e)
                    #Akn_LOGGER.info('Something went wrong! Error raised and passed...')
                    with open(text_file, "w") as fin:
                        fin.write(judgmentObj.text)
                        #logging.shutdown()

                    with open(text_file_NO_NER, "w") as fin:
                        fin.write(judgmentObj.text)

                    #logging.shutdown()
                    pass

                end_time = time.clock()
                #print round(end_time - start_time, 2)
                file_process_time = round(end_time - start_time, 2)
                #Akn_LOGGER.info('file prcessing time: %s',  file_process_time)
                #print is_valid
                with open (general_LOG_file, "a") as file_log:
                    file_log.write(os.path.join(root, name) + ';' + str(file_process_time) + ';' + str(is_valid) + '\n')
                    
                #logging.shutdown()
