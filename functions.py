# -*- coding: utf-8 -*-
import os
import re
import sys
import fnmatch
import requests
import logging
import subprocess
import textwrap
import shutil
import codecs
import datetime
from lxml import etree
from lxml import html
from variables import *


Akn_LOGGER = logging.getLogger('Akn_LOGGER')

def pdfToText(src, dest):
    """Traverses source folder and calls pdftotext to transform any PDF file
    to TXT file. It is based on fnmatch module so files must have an extension

    Args:
        src: The src directory that will be traversed with os.walk()
        
        dest: Destination folder where TXT files will be stored

    Returns:
        Nothing
    """          
    for dirpath, dirnames, filenames in os.walk(src, topdown=True):

        # create destination folder if it doesn't exist
        if not os.path.exists(dirpath.replace(src, dest)):
            os.makedirs(dirpath.replace(src, dest))

        for name in filenames:
            if fnmatch.fnmatch(name, '*.pdf'):
                #print name
                #print os.path.join(dirpath,name)
                #subprocess.call(["pdf2txt.py",
                #                 "-o",
                #                 os.path.join(DEST_FOLDER,name).split('.')[0]+".txt",
                #                 os.path.join(dirpath,name)]) 
                subprocess.call(["pdftotext",
                                 #"-layout",
                                 "-raw",
                                 #"-nopgbrk",
                                 os.path.join(dirpath,name),
                                 os.path.join(dirpath.replace(src, dest),name).split('.')[0]+".txt"
                                 ])

                
def copyFiles(src, dest):
    """Traverses source folder and copy all .txt files to destination folder. It is based on
    fnmatch module so files must have an extension

    Args:
        src: The source directory that will be traversed with os.walk()
        
        dest: Destination folder where TXT files will be copied

    Returns:
        Nothing 
    """
    if not os.path.exists(dest):
        os.makedirs(dest)
        
    for dirpath, dirnames, filenames in os.walk(src, topdown=True):
        #print dirpath.split('/')[-1]
        for name in filenames:
            if fnmatch.fnmatch(name, '*.txt'):
                if dest.split('/')[-2] in ('areios_pagos'):
                    ext = '.txt'
                    newFileName = name.replace('Αρ.', 'Αρ').split('.txt')[0] + ext
                else:
                    year = os.path.join(dirpath, name).split('/')[-2]
                    ext = name.split('.')[1]
                    newFileName = name.split('.')[0]+"_" + year + "." + ext
                
                shutil.copy(os.path.join(dirpath, name), os.path.join(dest, name))
                os.rename(os.path.join(dest, name), os.path.join(dest, newFileName))

 
def create_rules(fileObj):
    """Creates a dictionary of key - values pairs. Used by replaceChars function

    Args:
        fileObj: A file object with lines in the following format (no spaces) old_char=new_char 
        
    Returns:
        A python dictionary with key - value pairs 
    """
    rules={}
    with open (fileObj, "r") as rules_file:
        for line in rules_file:
            rules_list = line.split('=')
            rules[rules_list[0]] = re.sub(r'\n$', '', rules_list[1])
    #print(rules)
    return rules


def replaceChars(text, dictionary={}):
    """This method replaces characters of a text with new ones
    based on a dictionary. It is used to fix damaged characters that exists
    in .txt files (mainly in National Printing Service)

    Args:
        text: The text that needs to be fixed
        
        dictionary: A hash map that contains key(old characters) - value(new characters) pairs.   
        
    Returns:
        text: New text containing fixed characters 
    """
    if not dictionary:
        replCharDict = create_rules(RULES_FILE)
    else:
        replCharDict = dictionary

    for key, value in replCharDict.iteritems():
        text = re.sub(key, value, text, flags=re.DOTALL)

    return text


def subs_text(text, lst):
    """Same as replaceChars function but uses a list instead of a dictionary.
    Collects and removes garbages based on regexes (PDF paging etc.)

    Args:
        text: The text that will be substitute
        
        lst: A list that contains regexes for denoising text   

    Returns:
        text: New text without garbages 
    """
    for n in range(0,len(lst)):
        text = re.sub(lst[n][0], lst[n][1], text, flags=re.DOTALL)
    return text


def clean_text(src, dest, garbage_list, namePattern=None):
    """This function performs a necessary preprocess step including
    garbage removal, escaping XML invalid characters etc. and then stores
    new file to a user defined folder

    Args:
        src: The root directory that will be traversed with os.walk()
        dest: A path to store cleaned legal texts
        garbage_list: A list of regular expressions that removes noise text 
        namePattern: If namePattern is specified only file names that
            match the namePattern will be accessed

    Returns:
        Nothing 
    """
    file_pattern = '*.txt'
    if namePattern is not None:
        file_pattern = namePattern
        
    for root, dirs, files in os.walk(src):
        #print root
        #print root.replace(src, dest)
        if not os.path.exists(root.replace(src, dest)):
            os.makedirs(root.replace(src, dest))

        for name in files:
            if fnmatch.fnmatch(name, file_pattern):
                #print name
                # modify file name so that no dot is present
                new_file_name = os.path.splitext(name)[0].replace('.', '') + '.txt'
                #print new_fil_name
                with open(os.path.join(src, name), 'r') as fin:
                    data = fin.read()
                    text = subs_text(data, garbage_list)
                    fout = codecs.open(os.path.join(dest, new_file_name), 'w', 'UTF-8')
                    fout.write(escapeXMLChars(text).decode('UTF-8'))
                    fout.close()
    print("Done...")


def GrToLat(src, namePattern=None):
    """This function changes all greek characters in a file name to the
    corresponding Latin based on user keyboard. This is done due to brat
    tool which does not support greek names 

    Args:
        src: The root directory that will be traversed with os.walk() 
        namePattern: If namePattern is specified only file names that
            match the pattern will be transformed (fnamtch is used)

    Returns:
        Nothing 
    """
    if namePattern is not None:
        filePattern = namePattern
    else:
        filePattern = '*.txt'
        
    for root, dirs, files in os.walk(src, topdown=True):
        for name in files:
            if fnmatch.fnmatch(name, filePattern):
                print "old_name: "+ name
                old_name = name
                # it seems that in windows we need a sligthly
                # different approach
                if os.name != 'posix':
                    for char in name:
                        for key, value in grToLat.items():
                            if char.decode('windows-1253') == key.decode('utf-8'):
                                name = re.sub(char, value, name)
                # linux operating system
                else:
                    for key, value in grToLat.items():
                        name = re.sub(key, value, name)
                print "GrToLat: "+ name
                os.rename(os.path.join(dirpath, old_name), os.path.join(dirpath, name))
    print("Done...")


def checkForSummaries(src, metadata_path=None, namePattern=None):
    """Check if a judgment contains summary of the decision and deletes
    corresponding file

    Args:
        src: The root directory that contains files

        metadata_path: If specified this is the path where metadata is stored. It will
            also delete the corresponding metadata file (if it exists)

        namePattern: check if specific file contains summary

    Returns:
        Nothing
    """
    
    if namePattern is not None:
        filePattern = namePattern
    else:
        filePattern = '*.txt'

    # total number of files containing summaries
    cnt = 0
    for root, dirs, files in os.walk(src, topdown=True):
        #print root
        year = os.path.basename(root)
        for name in files:
            hasSummary = 0
            if fnmatch.fnmatch(name, filePattern):
                with open(os.path.join(os.path.join(src, str(year)), name), 'r') as fin:
                    summary = re.match(r'^\(Απόσπασμα\)|^Α\d+/\d+', fin.read(), re.DOTALL)
                    #print summary
                    if summary:
                        print "Found Judgment file with summary: " + name
                        hasSummary = 1
                        cnt += 1
                        if metadata_path is not None:
                            metaFileExists = os.path.isfile(os.path.join(os.path.join(metadata_path, str(year), name.split('.')[0]+'_meta.txt')))
                            #print os.path.join(os.path.join(metadata_path, str(year), name.split('.')[0]+'_meta.txt'))
                            if metaFileExists:
                                print "Metadata File exists: " + name
                                print "Removing: " + os.path.join(os.path.join(metadata_path, str(year), name.split('.')[0]+'_meta.txt'))
                                os.remove(os.path.join(os.path.join(metadata_path, str(year), name.split('.')[0]+'_meta.txt')))

                if hasSummary == 1:
                    print "Removing: " + os.path.join(os.path.join(src, str(year)), name)
                    os.remove(os.path.join(os.path.join(src, str(year)), name))

    print "Complete removing summaries. Total Files removed: " + str(cnt)

    
def fixFek(path):
    """For issues between 2000-2005 pdf encoding is damaged. This is only
        for pdfotetxt not pdfminer! This function fixes characters using replace all

    Args:
        path: The root directory that will be traversed with os.walk()

    Returns:
        Nothing 
    """
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        for name in filenames:
            if fnmatch.fnmatch(name, '*.txt'):
                with open(os.path.join(dirpath,name)+"_pre_", "wt") as fout, open(os.path.join(dirpath,name), "r") as fin:
                    mytext = fin.read()
                    text = replaceChars(mytext)
                    fout.write(text)
                    os.remove(os.path.join(dirpath, name))
                    os.rename(os.path.join(dirpath, name)+"_pre_", os.path.join(dirpath, name))


def countPDFPages(path):
    """This function counts the number of Pages of all PDF stored in path
    
    Args:
        path: The root directory that will be traversed with os.walk()

    Returns:
        count: The total number of pages 
    """
    count = 0
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        for name in filenames:
            if fnmatch.fnmatch(name, '*.pdf'):
                #print name
                try:
                    cmd = subprocess.check_output(["pdfinfo",
                                 "-meta",
                                 os.path.join(dirpath,name)
                                 ])
                    num = re.findall(r'Pages:\s*(\d+)', cmd)[0]
                    count += int(num)
                except subprocess.CalledProcessError:
                    pass
    return count


def valid_xml_char_ordinal(c):
    '''Function that filters out certain bytes when XML is
    constructed. XML standard defines a valid character as:
    Char ::= #x9 | #xA | #xD | [#x20 - #xD7FF] | [#xE000 - #xFFFD] | [#x10000 - #x10FFFF]

    Args:
        c: Character to be checked

    Returns:
        true if character codepoint in valid range
    '''
    codepoint = ord(c)
    #conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
    )


def escapeXMLChars(text):
    '''Controls characters that need to be escaped (to obtain a well-formed document)

    Args:
        text: The text that will be escaped (string)

    Returns:
        text: The text containing XML entities instead of characters (string)
    '''
    text = text.replace("&", "&amp;")
    #text = text.replace("\"", "&quot;")
    #text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    #text = text.replace(">", "&gt;")
    return text


def validateXML (schemaFile, xmlFile, logFile):
    '''Creates/Open a log file for an XML file that contains information
    about errors based on a Schema file. SchemaFile must be an XSD file
    
    Args:
        schemaFile: File that contains the XML schema
        
        xmlFile: XML file that is used to check if it is valid based on the XSD
        
        logFile: Log file where errors will be written
        
    Returns:
        nothing
    '''
    xmlSchemaDoc = etree.parse(schemaFile)
    xmlSchema = etree.XMLSchema(xmlSchemaDoc)
    xml_doc = etree.parse(xmlFile)
    #with open(logFile, 'a+') as error_log_file:
        #error_log_file.write('Starting Validation...\n')
    Akn_LOGGER.info('Starting Validation...')
    try:
        xmlSchema.assertValid(xml_doc)
        #error_log_file.write('XML valid: True\n')
        Akn_LOGGER.info('XML valid: True')
    except etree.DocumentInvalid as error:
        #error_log_file.write('XML valid: False\n')
        Akn_LOGGER.info('XML valid: False')
        for error in error.error_log:
            Akn_LOGGER.error('domain_name: '+error.domain_name)
            Akn_LOGGER.error('domain: ' + str(error.domain))
            Akn_LOGGER.error('filename: ' + error.filename)
            Akn_LOGGER.error('level: ' + str(error.level))
            Akn_LOGGER.error('line: ' + str(error.line))
            Akn_LOGGER.error('message: ' + error.message)
            #print 'domain_name: '+error.domain_name
            #print('domain_name: '+error.domain_name)
            #print('domain: ' + str(error.domain))
            #print('filename: ' + error.filename)
            #print('level: ' + str(error.level))
            #print('line: ' + str(error.line))
            #print('message: ' + error.message)
    except:
        #error_log_file.write('XML valid: False\n')
        Akn_LOGGER.info('XML valid: False')
        Akn_LOGGER.info('unknown error!')
        #error_log_file.write('unknown error!')
        #print('unknown error')

def CheckXMLvalidity (schemaFile, xmlFile):
    """Checks if a certain XML file is valid against a schema file.

    Args:
        schemaFile: The path to the schema file
        
        xmlFile: The XML file that needs to be tested

    Returns:
        True (if it is valid) or False (if it is not) 
    """
    xmlSchemaDoc = etree.parse(schemaFile)
    xmlSchema = etree.XMLSchema(xmlSchemaDoc)
    xml_doc = etree.parse(xmlFile)
    return xmlSchema.validate(xml_doc)


def createHrefFromDictionary (dictionary, splitMultHref = 0, element = 0):
    '''Creates an AkomaNtoso href attribute based on a dictionary of elements
    
    Args:
        dictionary: A dictionary containing context nodes with elements. Possible keys
            are type, legalYear, legalNumber, ExplicitArthroContext, ExplicitParContext etc.

    Returns:
        href : A unicode href attribute
    '''
    href = ''

    if dictionary.get('type'):
        href += dictionary.get('type') + '/'

    if dictionary.get('legalYear'):
        href += dictionary.get('legalYear') + '/'

    if dictionary.get('legalNumber'):
        href += dictionary.get('legalNumber') + '/'
        
    href += '!main'

    if splitMultHref == 0:
        if dictionary.get('ExplicitArthroContext'):
            href += '#art_' + dictionary.get('ExplicitArthroContext', '0')
        if dictionary.get('ExplicitParContext'):
            href += '__par_' + dictionary.get('ExplicitParContext', '0')
        if dictionary.get('ExplicitPeriptwsiContext'):
            href += '__case_' + dictionary.get('ExplicitPeriptwsiContext', '0')

    elif splitMultHref == 1:
        if element == 'ExplicitLegalTypeContext':
            href += ''
        if element == 'ExplicitArthroContext':
            href += ''
        if element == 'ExplicitParContext':
            if 'ExplicitArthroContext' in dictionary and isinstance(dictionary['ExplicitArthroContext'], list):
                href += '#art_' + dictionary.get('ExplicitArthroContext', '0')[-1]
            else:
                href += '#art_' + dictionary.get('ExplicitArthroContext', '0')
        if element == 'ExplicitPeriptwsiContext':
            href += '#art_' + dictionary.get('ExplicitArthroContext', '0')[-1]
            try:
                href += '__par_' + dictionary.get('ExplicitParContext', '0')
            except:
                href += '__par_0'
    return href


def findDatesOfInterest(searchNodeElem, regexObj, dateName, author):
    '''Function that searches for specific dates (e.g. publication date) in a legal text and
    returns a new text containing xml labels about them

    Args:
        searchNodeElem: The AkomaNtoso node that we would like to search
        
        regexObj: A compiled regex object that we use for different dates
        
        dateName: The name of the date of interest for example "courtConferenceDate"
        
        author: The author is used when creating the attribute 'by' of the "step" sublement in
                the meta section of akoma Ntoso
                
    Returns:
        searchNodeElem: A new node after finding all dates
        DateStep: An element that is to be written in workflow section of akomaNtoso metadata
        DateTLCEvent: An element that is to be written in references section of AkomaNtoso metadata
    '''
    for child in searchNodeElem.getchildren():
        childText = etree.tostring(child, pretty_print=True, encoding = 'UTF-8')
        if childText:
            DateOfInterest = re.search(regexObj, childText)
            if DateOfInterest:
                #print "vrethike"
                #print DateOfInterest.group()
                #print DateOfInterest.group('yyyy')
                #print DateOfInterest.group('mm')
                #print DateOfInterest.group('dd')
                elemIndex = searchNodeElem.getchildren().index(child)
                #print elemIndex
                Date = datetime.date(int(DateOfInterest.group('yyyy')), months.get(DateOfInterest.group('mm'), 0), int(DateOfInterest.group('dd')))
                #print str(Date)
                DateStr = DateOfInterest.group('dd') + DateOfInterest.group('numSpecialLektiko') + DateOfInterest.group('keno_1') + DateOfInterest.group('mm') + DateOfInterest.group('keno_2') + DateOfInterest.group('yyyy')
                text_to_replace = "<date refersTo= " '"'+ str(dateName) + '"' + " date = " + '"' + str(Date) + '"' +">" + DateStr + "</date>"
                new_text = childText.replace(DateStr, text_to_replace)
                newNode = etree.fromstring(new_text)
                searchNodeElem.remove(child)
                searchNodeElem.insert(elemIndex, newNode)
                
                # create a TLCevent that will be passed to Akomantoso "references" node
                DateStep = etree.Element("step", attrib={"date" : str(Date),
                                                         'by' : author, "refersTo" : '#'+dateName})

                
                DateTLCEvent = etree.Element("TLCEvent", attrib={"eId" : dateName,
                                                             "href":"/akn/ontology/event/gr/"+dateName,
                                                             "showAs": importantDates.get(dateName, 'no_important_date_found').decode('utf-8')
                                                                 })

                return searchNodeElem, DateStep, DateTLCEvent


def extractDataFromRequests(url, paramsData):
    '''Uses requests libary to extract data from NSK
    based on search form

    Args:
        url: The url to submit the request
        
        paramsData: post parameters

    Returns:
        dict: A dictionary containin several information such as keywords etc.
    '''
    extractedData = {}
    try:
        req = requests.post(url, params=paramsData)

        if req.status_code == 200:
            page = html.fromstring(req.content.decode('utf-8'))
            dataToExtract = page.xpath('//div[@class="article_text"]/p/text()')
            keywords_list = dataToExtract[3].strip().split(',')
            chairman = dataToExtract[7].strip()
            rapporteur = dataToExtract[9].strip()
            status = dataToExtract[11].strip()
            extractedData['keywords'] = keywords_list
            extractedData['chairman'] = chairman
            extractedData['rapporteur'] = rapporteur
            extractedData['status'] = status
    except requests.exceptions.HTTPError as errh:
        print ("Http Error: ", errh)
        pass
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting: ", errc)
        pass
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error: ", errt)
        pass
    except requests.exceptions.RequestException as err:
        print ("Something went wrong: ", err)
        pass

    return extractedData


def setupLogger(logger_name, log_file, level = logging.DEBUG):
    """Setup a logger so that logs can be stored as a file

    Args:
        logger_name: The logger name
        
        log_file: used to create a file_handler
        
        level: sets the level of messages that will be written in log_file

    returns:
        a logger instance
    """          
    logger = logging.getLogger(logger_name)
    #print logger
    logger.setLevel(level)

    for handler in logger.handlers[:]:  # make a copy of the list
        logger.removeHandler(handler)

    file_handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger          


def textToNumbering(text, dictionary):
    """Function that converts a small text to the corresponding ID (naming convention).
    This is due the fact that legislators sometimes refer to an element not using a
    number but a combination of number and a string eg 32A, First, Second etc.

    Args:
        text: A portion of text
        
        dictionary: A dictionary that holds values
        
    Returns:
        elemID: The corresponding element id based on a dictionary of values
        
    """
    elemID = []
    # Problem with python Greek letters, convert dictionary keys and values to unicode text
    unidict = {unicode(k, encoding='UTF-8'): v for k, v in dictionary.items()}
    
    #convert text to unicode
    if isinstance(text, str):
        text= text.decode('utf-8')
        
    split = re.search(ur'(?P<digit>\d*)(?P<space>\s*)(?P<lektiko>[Α-Ωα-ωάέήίόύώ]*)', text)
    if split:
        if split.group('lektiko'):
            elemID.insert(0, unidict.get(split.group('lektiko'), '0'))
        if split.group('digit'):
            elemID.insert(0, split.group('digit'))
            
    if elemID:
        elemIDstr = '_'.join(elemID)
    else:
        elemIDstr = '0'
    #print elemID
    #print elemIDstr
    return elemIDstr


def getTokenName(context, funcList, Dict, defaultVal):
    """Get the token name of a rule context that triggered this grammar rule.
    It is used only for Code Laws and Courts

    Args:
        context: the context rule
        
        funcList: this is a list containing all available functions of context
                (grammar tokens are represented as functions)
                
        Dict: dictionary that will be used to search the token
        
        defaultVal: If no key is found, return a user defined value

    returns:
        gramar token as a string
    """ 
    try:
        indx = funcList.index('__class__')
    except ValueError:
        indx = 0
    #print indx
    methodTriggered = ''
    for method in funcList[0:indx]:
        method_to_call = getattr(context, method)
        if callable(method_to_call):
            result = method_to_call()
            if result is not None:
                methodTriggered = method_to_call.__name__
                #print method_to_call.__name__
                #print courts.get(method_to_call.__name__, defaultVal)
    return Dict.get(methodTriggered, defaultVal)


def fixStringXML(text, regPatternObj):
    """This method fixes the XML string in order to be a valid XML string.
    It is used for cases where a ref tag closes after a new paragraph tag (</p><p>)

    Args:
        text: The text to be fixed
        
        regPatternObj: A regex pattern object -> r'([<][/]p[>][<]p[>])'

    returns:
        changed text as a valid XML string
    """
    refString = re.findall(r'[<]ref.*?[<][/]ref[>]', text, flags = re.DOTALL)
    if refString is not None:
        for string in refString:
            #print 'string in list:' +string
            if re.search(regPatternObj, string):
                newString = string.replace(re.search(regPatternObj, string).group(0), ' ')
                text = text.replace(string, newString)
    return text
