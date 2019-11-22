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
from grammars.gen.SupremeCourtLexer import SupremeCourtLexer
from grammars.gen.SupremeCourtParser import SupremeCourtParser
from grammars.gen.SupremeCourtListener import SupremeCourtListener
from grammars.gen.Legal_refLexer import Legal_refLexer
from grammars.gen.Legal_refParser import Legal_refParser
from grammars.gen.Legal_refListener import Legal_refListener
from grammars.gen.Legal_refVisitor import Legal_refVisitor

# Folder where judgments
BASE_FOLDER =  os.path.join(os.getcwd(), 'pdftotext')

# Folder path where logs are stored
LOGS_FOLDER = os.path.join(os.getcwd(), 'logs')

# Folder path where XML files are stored
XML_FOLDER = os.path.join(os.getcwd(), 'XML')

# Folder path where XML without NER files are stored
XML_NO_NER_FOLDER = os.path.join(os.getcwd(), 'XML_NO_NER')

# Declare folder name
START_FOLDER = r'areios_pagos'

# Define folder path that parsing will start from 
SRC = os.path.join(BASE_FOLDER, START_FOLDER)

# Define NER folder path
NER_FOLDER = 'NER_final_results'

# This is used for statistics purposes (time calculate, XML validation etc.)
general_LOG_file = 'statistics_AreiosPagos.txt'

if __name__ == '__main__':

    # Create regex object for publicHearingDate
    publicHearingDateObj = re.compile(publicHearingDatePattern)
    # Create regex objext for decisionPublicationDate
    decisionPublicationDateObj = re.compile(decisionPublicationDatePattern)             
    # Create regex objext for courtConferenceDate
    courtConferenceDateObj = re.compile(courtConferenceDatePattern)
    # Create regex objext for fix XML string
    paragraphPatternObj = re.compile(paragraphPattern)

    if len(sys.argv) != 2:
        filename = '*1997.txt'
    else :
        filename = sys.argv[1]

    ### LAST VERSION   ##########
    """for year in range(int(startYear), int(startYear)+1):
        #print year
        #print SRC
        folder = os.path.join(SRC, str(year)) 
        for root, dirs, files in os.walk(os.path.join(folder)):
    """
    ### LAST VERSION   ##########

    for root, dirs, files in os.walk(os.path.join(SRC)):
        # Last part of full path
        basename = os.path.basename(SRC)
        #print basename
       
        # Create LOG folder if it does not exist
        if not os.path.exists(root.replace(BASE_FOLDER, LOGS_FOLDER)):
            #print "Creating Logs folder..."
            os.makedirs(root.replace(BASE_FOLDER, LOGS_FOLDER))

        # Create XML folder if it does not exist
        if not os.path.exists(root.replace(BASE_FOLDER, XML_FOLDER)):
            #print "Creating XML folder..."
            os.makedirs(root.replace(BASE_FOLDER, XML_FOLDER))

        # Create XML without NER folder if it does not exist
        if not os.path.exists(root.replace(BASE_FOLDER, XML_NO_NER_FOLDER)):
            #print "Creating XML without NER folder..."
            os.makedirs(root.replace(BASE_FOLDER, XML_NO_NER_FOLDER))
            
        for name in files:
            statinfo = os.stat(os.path.join(root, name))
            if fnmatch.fnmatch(name, filename):
                #print name
            #if fnmatch.fnmatch(name, filename):
                #print "Judgment: " + name
                #print "size: " + str(os.path.getsize(os.path.join(root, name)))
                #print statinfo.st_size
                global is_valid
                #sys.exit()
                is_valid = False
                try:
                    start_time = time.clock()
                    
                    # Foreach judgment file create a corresponding log, XML and text filenames
                    year = name.split('.')[0].split('_')[-1]
                    #log_file = os.path.join(root.replace(BASE_FOLDER, LOGS_FOLDER), name)
                    xml_file = os.path.join(root.replace(BASE_FOLDER, XML_FOLDER), name.split('.')[0] + '.xml')
                    xml_file_NO_NER = os.path.join(root.replace(BASE_FOLDER, XML_NO_NER_FOLDER), name.split('.')[0] + '.xml')
                    text_file = os.path.join(root.replace(BASE_FOLDER, XML_FOLDER), name.split('.')[0] + '.txt')
                    text_file_NO_NER = os.path.join(root.replace(BASE_FOLDER, XML_NO_NER_FOLDER), name.split('.')[0] + '.txt')
                    # Declare Gate XML file where named entities are stored
                    #GateXml_file = os.path.join(os.path.join(os.path.join(BASE_FOLDER, NER_FOLDER), year), name + '.xml')
                    GateXml_file = os.path.join(os.path.join(os.path.join(os.path.join(BASE_FOLDER, NER_FOLDER), basename), year), name + '.xml')
                    #print log_file
                    #print xml_file
                    #print text_file
                    #print GateXml_file
                    #sys.exit()

                    # Setup a logger
                    #Akn_LOGGER = setupLogger('Akn_LOGGER', log_file)
                    #Akn_LOGGER.info('Converting %s', name)

                    #sys.exit()
                    ######################## METADATA ##########################################
                    # Dictionary of metadata
                    # Usually metadata comes from external files or could be extracted from legal text later
                    meta = {}
                    meta['textType'] = "judgment"
                    meta['author'] = "#SCCC"
                    meta['foreas'] = "SCCC"

                    # In Supreme Court we can extract decision number and year from file name
                    datePattern = re.search(r'Ar?\s+(?P<decisionNumber>\d+)[_](?P<issueYear>\d+)', name, re.DOTALL)
                    if datePattern:
                        #print 'decisionNumber ' + datePattern.group('decisionNumber')
                        #print 'issueYear '+ datePattern.group('issueYear')
                        meta['issueYear'] = datePattern.group('issueYear')
                        meta['decisionNumber'] = datePattern.group('decisionNumber')

                    # Create AknJudgementXML object
                    judgmentObj = AknJudgementXML(
                        textType = meta['textType'],
                        author = meta['author'],
                        foreas = meta['foreas'],
                        issueYear = meta['issueYear'],
                        decisionNumber = meta['decisionNumber']
                        )

                    # Create "meta" node
                    metaElem = judgmentObj.createMeta()
                    #print(etree.tostring(metaElem, pretty_print=True, encoding="UTF-8", xml_declaration =True))
                    
                    # Populate reference node with Named Entities
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
                    ######################## END METADATA ###########################################
                    
                    ########################### LEGAL REFERENCES #####################################
                    #print 'Parsing legal references...'
                    finput = FileStream(os.path.join(root, name), encoding='utf-8')
                    lexer = Legal_refLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = Legal_refParser(stream)
                    tree = parser.legal_text()
                    answer = AknLegalReferences().visit(tree)
                    #print(answer)
                    ########################### END LEGAL REFERENCES ###################################
                    
                    ############################# STRUCTURE ###########################################
                    #print 'Creating judgment structure...'
                    #Akn_LOGGER.info('Creating judgment structure...')
                    #finput = FileStream(os.path.join(os.path.join(SRC, str(year), name)), encoding='utf-8')
                    finput = InputStream(answer)
                    lexer = SupremeCourtLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = SupremeCourtParser(stream)
                    tree = parser.judgment()
                    walker = ParseTreeWalker()
                    walker.walk(judgmentObj, tree)
                    #print judgmentObj.text
                    ############################## END STRUCTURE ######################################               

                    ############################ Named Entities in text ###################################
                    if os.path.isfile(GateXml_file):
                        judgmentObj.text = judgmentObj.createNamedEntitiesInText(GateXml_file, judgmentObj.text)
                    #################################################################################
                    
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
                        workflow = akomaNtosoElem.xpath("/akomaNtoso/judgment/meta/workflow")
                        references = metaElem.xpath("/akomaNtoso/judgment/meta/references")

                        # Dates of interest can be found in specific elements in a judgment decision - find nodes
                        #Akn_LOGGER.info('Searching for dates of interest...')
                        
                        #################################  publicHearingDate  ########################################
                        # PublicHearingDate can be found on header element of AkomaNtoso structure
                        if headerNode:
                            newHeaderNode = findDatesOfInterest(headerNode[0], publicHearingDateObj, 'publicHearingDate', meta['author'])
                            if newHeaderNode is not None:
                                if workflow is not None:
                                    workflow[0].insert(0, newHeaderNode[1])

                                if references is not None:
                                    references[0].append(newHeaderNode[2])
                        ###########################################################################################

                        # Get FRBRdate date attribute of FRBRWork and FRBRExpression elements
                        FRBRdateWorkNode =akomaNtosoElem.xpath("/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRdate")
                        FRBRdateExpressionNode =akomaNtosoElem.xpath("/akomaNtoso/judgment/meta/identification/FRBRExpression/FRBRdate")
                        ########################## decisionPublicationDate  ############################################
                        # DecisionPublicationDate can be found on conclusions element of AkomaNtoso structure
                        hasDecisionPublicationDate = True
                        if conclusionsNode:
                            newConclusionsNode = findDatesOfInterest(conclusionsNode[0], decisionPublicationDateObj, 'decisionPublicationDate', meta['author'])
                            #print newConclusionsNode

                            if newConclusionsNode is not None:
                                pubHearDate = newConclusionsNode[1].get('date')

                                # Set step element to workflow node
                                if workflow is not None:
                                    workflow[0].insert(0, newConclusionsNode[1])

                                # Set TLCEvent element to workflow node
                                if references is not None:
                                    references[0].append(newConclusionsNode[2])

                                # Set "date" attribute to FRBRdate node of FRBRWork and FRBRExpression
                                if FRBRdateWorkNode:
                                    FRBRdateWorkNode[0].set('date', pubHearDate)

                                if FRBRdateExpressionNode:
                                    FRBRdateExpressionNode[0].set('date', pubHearDate)
                            else:
                                hasDecisionPublicationDate = False
                        #############################################################################################
                        
                        ########################## courtConferenceDate  #################################################
                        # CourtConferenceDate can also be found in conclusions node
                        if conclusionsNode:
                            newConclusionsNode = findDatesOfInterest(conclusionsNode[0], courtConferenceDateObj, 'courtConferenceDate', meta['author'])

                            if newConclusionsNode is not None:
                                courtConfDate = newConclusionsNode[1].get('date')

                                # Set step element to workflow node
                                if workflow is not None:
                                    workflow[0].insert(0, newConclusionsNode[1])

                                # Set TLCEvent element to workflow node
                                if references is not None:
                                    references[0].append(newConclusionsNode[2])

                                # If for some reason DecisionPublicationDate does not exist try fill FRBR date with
                                # court conference date
                                if hasDecisionPublicationDate == False:
                                    if FRBRdateWorkNode:
                                        FRBRdateWorkNode[0].set('date', courtConfDate)
                                        
                                    if FRBRdateExpressionNode:
                                        FRBRdateExpressionNode[0].set('date', courtConfDate)
                        ##############################################################################################
                        #Akn_LOGGER.info('Stop searching for dates of interest...')

                        # Create the corresponding ElementTree object
                        XmlTree = etree.ElementTree(akomaNtosoElem)
                        #print(etree.tostring(XmlTree, pretty_print=True, encoding="UTF-8", xml_declaration =True))
                        
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
                        #print is_valid
                        #logging.shutdown()

                    except etree.XMLSyntaxError:
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
                with open (general_LOG_file, "a") as file_log:
                    file_log.write(os.path.join(root, name) + ';' + str(file_process_time) + ';' + str(is_valid) + '\n')
                    
                #logging.shutdown()


