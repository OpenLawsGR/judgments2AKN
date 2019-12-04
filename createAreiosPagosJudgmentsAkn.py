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
import argparse
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

program_description = 'A Command Line Interface to transform judgments '
program_description += 'published by the Supreme Civil and Criminal court '
program_description += '(Areios Pagos) into XML using Akoma Ntoso '
program_description += 'prototype. '

parser = argparse.ArgumentParser(
    description = program_description
    )

year_help = 'choose a specific year for judgment(s) to be processed '
parser.add_argument(
    '-year',
    help = year_help
    )

fn_help = 'choose a specific file to be transformed to Akoma Ntoso '
fn_help += '(if argument is present -year parameter must be declared)'
parser.add_argument(
    '-fn',
    metavar = 'FILENAME',
    help = fn_help
    )

# create a namespace object
args = parser.parse_args()

if __name__ == '__main__':
    #print args

    # This is used for statistics purposes (time calculation, validation etc.)
    #general_LOG_file = 'statistics_AreiosPagos.txt'

    # Create regex object for publicHearingDate
    publicHearingDateObj = re.compile(publicHearingDatePattern)
    # Create regex objext for decisionPublicationDate
    decisionPublicationDateObj = re.compile(decisionPublicationDatePattern)             
    # Create regex objext for courtConferenceDate
    courtConferenceDateObj = re.compile(courtConferenceDatePattern)
    # Create regex objext for fix XML string
    paragraphPatternObj = re.compile(paragraphPattern)

    if args.fn is not None:
        if args.year is None:
            parser.error(
                'You must provide -year parameter ' +
                'in order to process a specific file'
                )
        else:
            file_pattern = '*' + args.fn
    else:
        file_pattern = '*' + TXT_EXT

    source_path = os.path.join(
        os.getcwd(),
        os.path.join(
            LEGAL_TEXTS,
            AREIOS_PAGOS
            )
        )
    
    if args.year is not None:
        source_path = os.path.join(
            source_path,
            args.year
            )
    #print source_path

    for root, dirs, files in os.walk(source_path):
        #print root
        logs_path = root.replace(
            os.path.join(
                os.getcwd(),
                LEGAL_TEXTS
                ),
            os.path.join(
                os.getcwd(),
                LOGS
                )
            )
        #print "logs: " + logs_path

        xml_path = root.replace(
            os.path.join(
                os.getcwd(),
                LEGAL_TEXTS
                ),
            os.path.join(
                os.getcwd(),
                XML
                )
            )
        #print "xml: " + xml_path

        #xml_no_ner_path = root.replace(
        #    os.path.join(
        #        os.getcwd(),
        #        LEGAL_TEXTS
        #        ),
        #    os.path.join(
        #        os.getcwd(),
        #        XML_NO_NER
        #        )
        #    )
        #print "xmlnoner: " +xml_no_ner_path

        ner_path = root.replace(
            os.path.join(
                os.getcwd(),
                LEGAL_TEXTS
                ),
            os.path.join(
                os.getcwd(),
                NER
                )
            )
        #print "ner: " + ner_path
        #sys.exit()
        
        # Create LOG folder if it does not exist
        if not os.path.exists(logs_path):
            #print "Creating Logs folder..."
            os.makedirs(logs_path)

        # Create XML folder if it does not exist
        if not os.path.exists(xml_path):
            #print "Creating XML folder..."
            os.makedirs(xml_path)

        # Create XML without NER folder if it does not exist
        #if not os.path.exists(xml_no_ner_path):
            #print "Creating XML without NER folder..."
            #os.makedirs(xml_no_ner_path)
            
        for name in files:
            if fnmatch.fnmatch(name, file_pattern):
                print "judgment decision: " + name
                global is_valid
                is_valid = False
                try:
                    # just for statistics purposes
                    start_time = time.clock()
                    
                    # Foreach judgment file create a corresponding log,
                    # XML and text filename
                    year = name.split('.')[0].split('_')[-1]
                    log_file = os.path.join(
                        logs_path,
                        name
                        )
                    xml_file = os.path.join(
                        xml_path,
                        name.split('.')[0] + XML_EXT
                        )
                    #xml_file_NO_NER = os.path.join(
                    #    xml_no_ner_path,
                    #    name.split('.')[0] + XML_EXT
                    #    )
                    text_file = os.path.join(
                        xml_path,
                        name.split('.')[0] + TXT_EXT
                        )
                    #text_file_NO_NER = os.path.join(
                    #    xml_no_ner_path,
                    #    name.split('.')[0] + TXT_EXT
                    #    )
                    
                    # Declare Gate XML file where named entities are stored
                    gate_xml_file = os.path.join(
                        ner_path,
                        name + XML_EXT
                        )
                    #print "log_file: " + log_file
                    #print "xml_file: " + xml_file
                    #print "text_fle: " + text_file
                    #print "gate_xml: " + gate_xml_file
                    #sys.exit()

                    # Setup a logger
                    Akn_LOGGER = setupLogger('Akn_LOGGER', log_file)
                    Akn_LOGGER.info('Converting %s', name)

                    ######################## METADATA #########################
                    # Dictionary of metadata
                    # Usually metadata comes from external files or
                    # could be extracted from legal text later
                    meta = {}
                    meta['textType'] = "judgment"
                    meta['author'] = "#SCCC"
                    meta['foreas'] = "SCCC"

                    # In Areios Pagos we can extract decision number and
                    # year from file name
                    datePattern = re.search(
                        r'Ar?\s+(?P<decisionNumber>\d+)[_](?P<issueYear>\d+)',
                        name,
                        re.DOTALL
                        )
                    if datePattern:
                        #print datePattern.group('decisionNumber')
                        #print datePattern.group('issueYear')
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
                    #print(etree.tostring(
                    #    metaElem,
                    #    pretty_print=True,
                    #    encoding="UTF-8",
                    #    xml_declaration =True
                    #    ))
                    
                    # Populate reference node with Named Entities
                    if os.path.isfile(gate_xml_file):
                        #print "gate_xml_file exists"
                        referencesNode = metaElem.find('references')
                        if referencesNode is not None:
                            referencesNodeIndex = metaElem.getchildren().index(referencesNode)
                            #print referencesNodeIndex
                            newReferencesNode = judgmentObj.modifyReferencesFromGateXml(
                                gate_xml_file,
                                referencesNode
                                )
                            metaElem.remove(referencesNode)
                            metaElem.insert(
                                referencesNodeIndex,
                                newReferencesNode
                                )
                    #sys.exit()
                    ######################## END METADATA #####################
                    
                    ########################### LEGAL REFERENCES #################
                    #print 'Parsing legal references...'
                    finput = FileStream(os.path.join(root, name), encoding='utf-8')
                    lexer = Legal_refLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = Legal_refParser(stream)
                    tree = parser.legal_text()
                    answer = AknLegalReferences().visit(tree)
                    #print(answer)
                    ########################### END LEGAL REFERENCES ##############
                    
                    ############################# STRUCTURE #######################
                    #print 'Creating judgment structure...'
                    Akn_LOGGER.info('Creating judgment structure...')
                    finput = InputStream(answer)
                    lexer = SupremeCourtLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = SupremeCourtParser(stream)
                    tree = parser.judgment()
                    walker = ParseTreeWalker()
                    walker.walk(judgmentObj, tree)
                    #print judgmentObj.text
                    ############################## END STRUCTURE ####################               

                    ############################ Named Entities in text #############
                    if os.path.isfile(gate_xml_file):
                        judgmentObj.text = judgmentObj.createNamedEntitiesInText(
                            gate_xml_file,
                            judgmentObj.text
                            )
                    ##################################################################

                    # Create AkomaNtoso Root element
                    akomaNtosoElem = judgmentObj.createAkomaNtosoRoot()
                    
                    # This is due to cases where a ref tag does not close
                    # before the end tag of a paragraph (<p><ref></p></ref>)
                    judgmentObj.text = fixStringXML(
                        judgmentObj.text,
                        paragraphPatternObj
                        )

                    try:
                        # Create judgment element based on parser and append to root
                        Akn_LOGGER.info('Transforming to XML element...')

                        # etree.fromstring is being used it will change range
                        # ids character '>' to &gt; 
                        judgmentElem = judgmentObj.XML()

                        #print etree.tostring(
                        #    judgmentElem,
                        #    pretty_print=True,
                        #    encoding="UTF-8",
                        #    xml_declaration =True
                        #    )
                        akomaNtosoElem.insert(0, judgmentElem)
                        
                        # Find judgment node and insert metaElement
                        judgmentNode = akomaNtosoElem.find("judgment")
                        judgmentNode.insert(0, metaElem)
                        #print(
                        #    etree.tostring(
                        #        akomaNtosoElem,
                        #        pretty_print=True,
                        #        encoding="UTF-8",
                        #        xml_declaration =True
                        #        )
                        #    )

                        # Specific nodes that will be used after
                        headerNode = akomaNtosoElem.xpath("/akomaNtoso/judgment/header")
                        conclusionsNode = akomaNtosoElem.xpath("/akomaNtoso/judgment/conclusions")
                        workflow = akomaNtosoElem.xpath("/akomaNtoso/judgment/meta/workflow")
                        references = metaElem.xpath("/akomaNtoso/judgment/meta/references")

                        # Dates of interest can be found in specific elements
                        # in a judgment decision - find nodes
                        Akn_LOGGER.info('Searching for dates of interest...')
                        
                        ######################  publicHearingDate  #########################
                        # PublicHearingDate can be found on header element
                        # of AkomaNtoso structure
                        if headerNode:
                            newHeaderNode = findDatesOfInterest(
                                headerNode[0],
                                publicHearingDateObj,
                                'publicHearingDate',
                                meta['author']
                                )
                            
                            if newHeaderNode is not None:
                                if workflow is not None:
                                    workflow[0].insert(0, newHeaderNode[1])

                                if references is not None:
                                    references[0].append(newHeaderNode[2])
                        ###################################################################

                        # Get FRBRdate date attribute of FRBRWork and FRBRExpression elements
                        FRBRdateWorkNode = akomaNtosoElem.xpath(
                            "/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRdate"
                            )
                        FRBRdateExpressionNode = akomaNtosoElem.xpath(
                            "/akomaNtoso/judgment/meta/identification/FRBRExpression/FRBRdate"
                            )
                        ########################## decisionPublicationDate  ################
                        # DecisionPublicationDate can be found on conclusions element
                        # of AkomaNtoso structure
                        hasDecisionPublicationDate = True
                        if conclusionsNode:
                            newConclusionsNode = findDatesOfInterest(
                                conclusionsNode[0],
                                decisionPublicationDateObj,
                                'decisionPublicationDate',
                                meta['author']
                                )
                            #print newConclusionsNode

                            if newConclusionsNode is not None:
                                pubHearDate = newConclusionsNode[1].get('date')

                                # Set step element to workflow node
                                if workflow is not None:
                                    workflow[0].insert(0, newConclusionsNode[1])

                                # Set TLCEvent element to workflow node
                                if references is not None:
                                    references[0].append(newConclusionsNode[2])

                                # Set "date" attribute to FRBRdate node of
                                # FRBRWork and FRBRExpression
                                if FRBRdateWorkNode:
                                    FRBRdateWorkNode[0].set('date', pubHearDate)

                                if FRBRdateExpressionNode:
                                    FRBRdateExpressionNode[0].set('date', pubHearDate)
                            else:
                                hasDecisionPublicationDate = False
                        ####################################################################
                        
                        ########################## courtConferenceDate  ####################
                        # CourtConferenceDate can also be found in conclusions node
                        if conclusionsNode:
                            newConclusionsNode = findDatesOfInterest(
                                conclusionsNode[0],
                                courtConferenceDateObj,
                                'courtConferenceDate',
                                meta['author']
                                )

                            if newConclusionsNode is not None:
                                courtConfDate = newConclusionsNode[1].get('date')

                                # Set step element to workflow node
                                if workflow is not None:
                                    workflow[0].insert(0, newConclusionsNode[1])

                                # Set TLCEvent element to workflow node
                                if references is not None:
                                    references[0].append(newConclusionsNode[2])

                                # If for some reason DecisionPublicationDate does not exist
                                # try fill FRBR date with
                                # court conference date
                                if hasDecisionPublicationDate == False:
                                    if FRBRdateWorkNode:
                                        FRBRdateWorkNode[0].set('date', courtConfDate)
                                        
                                    if FRBRdateExpressionNode:
                                        FRBRdateExpressionNode[0].set('date', courtConfDate)
                        ######################################################################
                        Akn_LOGGER.info('Stop searching for dates of interest...')

                        # Create the corresponding ElementTree object
                        XmlTree = etree.ElementTree(akomaNtosoElem)
                        #print etree.tostring(
                        #    XmlTree,
                        #    pretty_print = True,
                        #    encoding="UTF-8",
                        #    xml_declaration = True
                        #    )
                        
                        # Open the XML file and append elementTree to it
                        Akn_LOGGER.info('Creating XML file...')
                        # Problem with href range_id cannot retain '>' character,
                        # so write string tree representation to file
                        with codecs.open(xml_file, "w") as fin:
                             fin.write(
                                 etree.tostring(
                                     XmlTree,
                                     pretty_print=True,
                                     encoding="UTF-8",
                                     xml_declaration =True
                                     ).replace('&gt;', '>')
                                 )

                        ########## copy XML tree and save it without including NER ##############
                        """
                        rootNode = XmlTree.getroot()
                        for child in rootNode.xpath("./judgment/meta/references"):
                            for  child_lv2 in child:
                                if child_lv2.tag == 'TLCOrganization' or child_lv2.tag == 'TLCPerson' or child_lv2.tag == 'TLCLocation':
                                    #print child_lv2
                                    child_lv2.getparent().remove(child_lv2)

                        XmlTreeStr_NO_NER = etree.tostring(
                            XmlTree,
                            pretty_print=True,
                            encoding="UTF-8",
                            xml_declaration =True
                            )
                        XmlTreeStr_NO_NER = re.sub(
                            r'[<]/?organization.*?[>]',
                            '',
                            XmlTreeStr_NO_NER,
                            flags = re.DOTALL
                            )
                        XmlTreeStr_NO_NER = re.sub(
                            r'[<]/?person.*?[>]',
                            '',
                            XmlTreeStr_NO_NER,
                            flags = re.DOTALL
                            )
                        XmlTreeStr_NO_NER = re.sub(
                            r'[<]/?location.*?[>]',
                            '',
                            XmlTreeStr_NO_NER,
                            flags = re.DOTALL
                            )
                        #print XmlTreeStr_NO_NER
                        # etree.fromstring is being used it will change
                        # range ids character '>' to &gt; 
                        XmlElement_NO_NER = etree.fromstring(XmlTreeStr_NO_NER)
                        #print XmlElement_NO_NER
                        XmlTree_NO_NER = etree.ElementTree(XmlElement_NO_NER)
                        #print XmlElement_NO_NER
                        with codecs.open(xml_file_NO_NER, "w") as fin:
                             fin.write(
                                 etree.tostring(
                                     XmlTree_NO_NER,
                                     pretty_print=True,
                                     encoding="UTF-8",
                                     xml_declaration =True
                                     ).replace('&gt;', '>')
                                 )
                        """
                        ########################################################################

                        # Validation
                        validateXML('akomantoso30.xsd', xml_file, log_file)
                        #is_valid = CheckXMLvalidity('akomantoso30.xsd', xml_file)
                        #print is_valid

                    except etree.XMLSyntaxError:
                        # Something went wrong write the corresponding
                        # XML string to a .txt file
                        Akn_LOGGER.info('Could not create XML element from string! Check validity!')
                        with open(text_file, "w") as fin:
                            fin.write(judgmentObj.text)

                        #with open(text_file_NO_NER, "w") as fin:
                        #    fin.write(judgmentObj.text)

                except KeyboardInterrupt:
                    raise

                except Exception as e:
                    print(e)
                    Akn_LOGGER.info('Something went wrong! Error raised and passed...')
                    with open(text_file, "w") as fin:
                        fin.write('')

                    #with open(text_file_NO_NER, "w") as fin:
                    #    fin.write('')
                    #pass

                end_time = time.clock()
                file_process_time = round(end_time - start_time, 2)
                #print is_valid
                Akn_LOGGER.info('file process time: %s',  file_process_time)
                #with open (general_LOG_file, "a") as file_log:
                #    file_log.write(
                #        os.path.join(root, name) +
                #        ';' +
                #        str(file_process_time) +
                #        ';' +
                #        str(is_valid) +
                #        '\n'
                #        )
                  
                logging.shutdown()
