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
from grammars.gen.CouncilOfStateLexer import CouncilOfStateLexer
from grammars.gen.CouncilOfStateParser import CouncilOfStateParser
from grammars.gen.CouncilOfStateListener import CouncilOfStateListener
from grammars.gen.Legal_refLexer import Legal_refLexer
from grammars.gen.Legal_refParser import Legal_refParser
from grammars.gen.Legal_refListener import Legal_refListener
from grammars.gen.Legal_refVisitor import Legal_refVisitor

program_description = 'A Command Line Interface for transforming judgments '
program_description += 'published by the Council of State into XML using '
program_description += 'Akoma Ntoso prototype. '

parser = argparse.ArgumentParser(
    description = program_description
    )

year_help = 'choose a specific year for judgment(s) to be processed'
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

    # This is used for statistics purposes (time calculate,
    # XML validation etc.)
    #general_LOG_file = 'statistics_CouncilOfState.txt'

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
            STE
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

        ste_metadata_path = root.replace(
            os.path.join(
                os.getcwd(),
                LEGAL_TEXTS
                ),
            os.path.join(
                os.getcwd(),
                STE_METADATA
                )
            )
        #print "ste_metadata_path: " + ste_metadata_path
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
                    # XML and text filenames
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
                    #print log_file
                    #print xml_file
                    #print text_file
                    #print gate_xml_file
                    #sys.exit()

                    # Setup a logger
                    Akn_LOGGER = setupLogger('Akn_LOGGER', log_file)
                    Akn_LOGGER.info('Converting %s', name)

                    ######################## METADATA ##########################################
                    # Initialize a dictionary where metadata is stored.
                    # Usually metadata comes from external files
                    # other metadata should be extracted from legal text later
                    meta = {}
                    meta['textType'] = "judgment"
                    meta['author'] = "#COS"
                    meta['foreas'] = "COS"
                
                    # Some metadata can be extracted from STE_META_FOLDER
                    year = name.split('.')[0].split('_')[1]
                    metaFileExists = os.path.isfile(
                        os.path.join(
                            ste_metadata_path,
                            name.split('.')[0]+'_meta' + TXT_EXT
                            )
                        )

                    if metaFileExists:
                        with open(
                            os.path.join(
                                os.path.join(
                                    ste_metadata_path,
                                    name.split('.')[0]+'_meta' + TXT_EXT
                                    )
                                ), 'r') as fin:
                            text = fin.read()
                            text = text.split('\n')            
                            meta['issueYear'] = text[0].strip().split('/')[1]
                            meta['decisionNumber'] = text[0].strip().split('/')[0]
                            if text[7].strip() != '-':
                                meta['ECLI'] = text[7].strip()
                            else:
                                meta['ECLI'] = None
                            meta['pub_date'] = text[3].strip()
                            #print text[3]
                            #print datetime.datetime.strptime(meta['pub_date'], '%d/%m/%Y')
                            try:
                                # Return a datetime object corresponding to meta['pub_date'],
                                # based on format
                                datetimeObj = datetime.datetime.strptime(
                                    meta['pub_date'],
                                    '%d/%m/%Y'
                                    )
                                meta['publicationDate'] = str(datetimeObj.date())
                            except ValueError:
                                #print("Time data does not match format")
                                meta['publicationDate'] = str(
                                    datetime.date(
                                        int(meta['pub_date']),
                                        1,
                                        1
                                        )
                                    )
                    else:
                        # No metadata folder exists - Read from filename
                        meta['issueYear'] = year
                        meta['decisionNumber'] = name.split('_')[0]
                        meta['ECLI'] = None
                        meta['publicationDate'] = None
                        
                    #for key in meta:
                        #print key + ":", meta[key]

                    # Create AknJudgementXML object
                    judgmentObj = AknJudgementXML(
                        textType = meta['textType'],
                        author = meta['author'],
                        foreas = meta['foreas'],
                        issueYear = meta['issueYear'],
                        decisionNumber = meta['decisionNumber'].decode('utf-8'),
                        ECLI = meta['ECLI'],
                        publicationDate = meta['publicationDate']
                        )

                    # Create "meta" node
                    metaElem = judgmentObj.createMeta()
                    # Populate reference node with Named Entities
                    # based on Gate XML file if it exists
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
                    ######################## END METADATA ##########################################
                    
                    ######################## LEGAL REFERENCES #######################################
                    #print 'Parsing legal references...'
                    finput = FileStream(os.path.join(root, name), encoding='utf-8')
                    lexer = Legal_refLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = Legal_refParser(stream)
                    tree = parser.legal_text()
                    answer = AknLegalReferences().visit(tree)
                    #print(answer)
                    ######################## END LEGAL REFERENCES ##################################

                    ############################# STRUCTURE #######################################
                    Akn_LOGGER.info('Creating judgment structure...')
                    finput = InputStream(answer)
                    lexer = CouncilOfStateLexer(finput)
                    stream = CommonTokenStream(lexer)
                    parser = CouncilOfStateParser(stream)
                    tree = parser.judgment()
                    walker = ParseTreeWalker()
                    walker.walk(judgmentObj, tree)
                    ############################# END STRUCTURE #######################################

                    ############################ Named Entities in text ###################################
                    if os.path.isfile(gate_xml_file):
                        judgmentObj.text = judgmentObj.createNamedEntitiesInText(
                            gate_xml_file,
                            judgmentObj.text
                            )
                    #################################################################################
                    
                    # Create AkomaNtoso Root element
                    akomaNtosoElem = judgmentObj.createAkomaNtosoRoot()

                    # This is due to cases where a ref tag does not close before the end tag of a paragraph (<p><ref></p></ref>)
                    judgmentObj.text =fixStringXML(
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
                        
                        #Specific nodes that will be used after
                        headerNode = akomaNtosoElem.xpath("/akomaNtoso/judgment/header")
                        conclusionsNode = akomaNtosoElem.xpath("/akomaNtoso/judgment/conclusions")
                        workflow = akomaNtosoElem.xpath("/akomaNtoso/judgment/meta/workflow")
                        references = metaElem.xpath("/akomaNtoso/judgment/meta/references")

                        # Get FRBRdate date attribute of FRBRWork and FRBRExpression elements
                        FRBRdateWorkNode =akomaNtosoElem.xpath(
                            "/akomaNtoso/judgment/meta/identification/FRBRWork/FRBRdate"
                            )
                        FRBRdateExpressionNode =akomaNtosoElem.xpath(
                            "/akomaNtoso/judgment/meta/identification/FRBRExpression/FRBRdate"
                            )
                        # Dates of interest can be found in specific elements in
                        # a judgment decision - find nodes
                        Akn_LOGGER.info('Searching for dates of interest...')
                        
                        ################################ publicHearingDate #########################
                        # publicHearingDate can be found in header element of
                        # AkomaNtoso structure
                        if headerNode:
                            newHeaderNode = findDatesOfInterest(
                                headerNode[0],
                                publicHearingDateObj,
                                'publicHearingDate',
                                meta['author']
                                )

                            if newHeaderNode is not None:
                                publicHearDate = newHeaderNode[1].get('date')

                                if workflow is not None:
                                    workflow[0].insert(0, newHeaderNode[1])

                                if references is not None:
                                    references[0].append(newHeaderNode[2])

                                # Set "date" attribute to FRBRdate node of
                                # FRBRWork and FRBRExpression
                                if FRBRdateWorkNode:
                                    FRBRdateWorkNode[0].set('date', publicHearDate)
                                    FRBRdateWorkNode[0].set('name', 'publicHearingDate')

                                if FRBRdateExpressionNode:
                                    FRBRdateExpressionNode[0].set('date', publicHearDate)
                                    FRBRdateExpressionNode[0].set('name', 'publicHearingDate')
                        ############################################################################

                        ############################# courtConferenceDate ############################
                        # courtConferenceDate can be found in conclusions element
                        # of AkomaNtoso structure
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
                                #if hasDecisionPublicationDate == False:
                                if FRBRdateWorkNode:
                                    FRBRdateWorkNode[0].set('date', courtConfDate)
                                    FRBRdateWorkNode[0].set('name', 'courtConferenceDate')
                                    
                                if FRBRdateExpressionNode:
                                    FRBRdateExpressionNode[0].set('date', courtConfDate)
                                    FRBRdateExpressionNode[0].set('name', 'courtConferenceDate')
                        ###############################################################################
                        
                        ############################## decisionPublicationDate ######################
                        # decisionPublicationDate can be found in conclusions element
                        # of AkomaNtoso structure
                        #hasDecisionPublicationDate = True
                        if conclusionsNode:
                            newConclusionsNode = findDatesOfInterest(
                                conclusionsNode[0],
                                decisionPublicationDateObj,
                                'decisionPublicationDate',
                                meta['author']
                                )

                            if newConclusionsNode is not None:
                                publicationDate = newConclusionsNode[1].get('date')

                                # Set step element to workflow node
                                if workflow is not None:
                                    workflow[0].insert(0, newConclusionsNode[1])
                                
                                # Set TLCEvent element to workflow node
                                if references is not None:
                                    references[0].append(newConclusionsNode[2])

                                # Set "date" attribute to FRBRdate node of
                                # FRBRWork and FRBRExpression
                                if FRBRdateWorkNode:
                                    FRBRdateWorkNode[0].set('date', publicationDate)
                                    FRBRdateWorkNode[0].set('name', 'decisionPublicationDate')

                                if FRBRdateExpressionNode:
                                    FRBRdateExpressionNode[0].set('date', publicationDate)
                                    FRBRdateExpressionNode[0].set('name', 'decisionPublicationDate')
                            #else:
                            #    hasDecisionPublicationDate = False
                        ####################################################################
                        
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
                                     xml_declaration = True
                                     ).replace('&gt;', '>')
                                 )

                        ########## copy XML tree and save it without including NER #####################################
                        """
                        rootNode = XmlTree.getroot()
                        for child in rootNode.xpath("./judgment/meta/references"):
                            for  child_lv2 in child:
                                if child_lv2.tag == 'TLCOrganization' or child_lv2.tag == 'TLCPerson' or child_lv2.tag == 'TLCLocation':
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
                                     xml_declaration = True
                                     ).replace('&gt;', '>')
                                 )
                        """
                        #######################################################################################
                        
                        # Validation
                        validateXML('akomantoso30.xsd', xml_file, log_file)
                        #is_valid = CheckXMLvalidity('akomantoso30.xsd', xml_file)

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
                #print round(end_time - start_time, 2)
                file_process_time = round(end_time - start_time, 2)
                Akn_LOGGER.info('file process time: %s',  file_process_time)
                #with open (general_LOG_file, "a") as file_log:
                #    file_log.write(
                #        os.path.join(root, name) +
                #        ';' +
                #        str(file_process_time) +
                #        ';' +
                #        str(is_valid) + '\n'
                #        )
                    
                logging.shutdown()
                        
