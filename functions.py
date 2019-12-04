# -*- coding: utf-8 -*-
import os
import re
import sys
import fnmatch
import requests
import logging
import subprocess
import shutil
import codecs
import datetime
from lxml import etree
from lxml import html
from variables import *

Akn_LOGGER = logging.getLogger('Akn_LOGGER')

def pdf_to_text(src, dest, name_pattern=None):
    """Transforms PDF files to texts using pdftotext command
    (https://linux.die.net/man/1/pdftotext). Newly created files are
    stored to dest (destination) path.

    Args:
        src: The source directory that will be traversed with os.walk()
        
        dest: Destination folder where '.txt' files will be stored

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be transformed from PDF to text

    Returns:
        Nothing
    """
    file_pattern = '*' + PDF_EXT
    if name_pattern is not None:
        file_pattern = name_pattern
        
    for root, dirs, files in os.walk(src, topdown=True):
        #print root.replace(src, dest)
        #sys.exit()
        # create destination folder if it does not exist
        if not os.path.exists(root.replace(src, dest)):
            os.makedirs(root.replace(src, dest))

        for name in files:
            if fnmatch.fnmatch(name, file_pattern):
                subprocess.call(
                    ["pdftotext",
                     #"-layout",
                     "-raw",
                     #"-nopgbrk",
                     os.path.join(root, name),
                     os.path.join(
                         root.replace(src, dest),
                         name
                         ).split('.')[0] + TXT_EXT]
                    )

    print("Done...")

                
def copy_files(src, dest, name_pattern=None):
    """Copy all '.txt' files from src (source) to dest (destination) folder.

    Args:
        src: The source directory that will be traversed with os.walk()
        
        dest: Destination folder where '.txt' files will be copied

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be copied

    Returns:
        Nothing 
    """
    file_pattern = '*' + TXT_EXT
    if name_pattern is not None:
        file_pattern = name_pattern
        
    if not os.path.exists(dest):
        os.makedirs(dest)
        
    for root, dirs, files in os.walk(src, topdown=True):
        for name in files:
            if fnmatch.fnmatch(name, file_pattern):             
                shutil.copy(
                    os.path.join(
                        root,
                        name
                        ),
                    os.path.join(
                        dest,
                        name
                        )
                    )

    print ("Done...")


def create_rules(fileObj):
    """Creates a dictionary of key - values pairs. Used by replaceChars
    function

    Args:
        fileObj: A file object with lines in the following format (no spaces)
            old_char=new_char 
        
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
    """Replaces characters of a text with new ones based on a dictionary.
    Mainly used for fixing damaged characters that are present in '.txt'
    files.

    Args:
        text: The text that needs to be fixed
        
        dictionary: A hash map that contains pairs of
            key(old characters) - value(new characters)   
        
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
    """Same as replaceChars but uses a list instead of a dictionary.

    Args:
        text: The text that will be substitute
        
        lst: A list that contains regexes for denoising text   

    Returns:
        text: New text without garbages 
    """
    for n in range(0,len(lst)):
        text = re.sub(lst[n][0], lst[n][1], text, flags=re.DOTALL)

    return text


def clean_ste_text(src, dest, name_pattern=None):
    """Performs pre-processing steps for judgments published by the
    Council of State. By default it reads the first ten lines of a
    judgment that contains metadata (see ste_scapper) and creates the
    appropriate path to store metadata file. The rest of the text
    (judgment body) will be cleaned and stored according to dest
    (destination) parameter 

    Args:
        src: The root directory that will be traversed with os.walk()

        dest: A path to store cleaned data

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be accessed

    Returns:
        Nothing 
    """
    
    file_pattern = '*' + TXT_EXT
    if name_pattern is not None:
        file_pattern = name_pattern
    
    for root, dirs, files in os.walk(src):
        #print src
        #print dest
        metadata_path = dest.replace(STE, STE_METADATA)
        #print metadata_path
        # create a corresponding folder based on 'dest' argument
        if not os.path.exists(root.replace(src, dest)):
            os.makedirs(root.replace(src, dest))

        # create a corresponding metadata folder based on 'dest' argument  
        if not os.path.exists(metadata_path):
            os.makedirs(metadata_path)

        for name in files:
            #print 'name:' + name
            # create new file name so that it contains year of publication
            year = os.path.basename(src)
            new_file_name = name.split('.')[0] + '_' + str(year) 
            if fnmatch.fnmatch(name, file_pattern):
                # declare full path for metadata file
                metadata_file_path = os.path.join(
                    metadata_path,
                    new_file_name + '_meta' + TXT_EXT
                    )
                #print 'metaFilePath: '+ metaFilePath
                with open(os.path.join(src, name), 'r') as fin:
                    # by default the first 10 lines contain metadata
                    # see ste crawler
                    judgmentText_ = fin.readlines()
                    metadata = ''
                    judgmentBody = ''

                    for line in judgmentText_[:10]:
                        metadata += line

                    for line in judgmentText_[11:]:
                        judgmentBody += line
                        
                    # open a new file for writing metadata
                    with open(metadata_file_path, 'w') as fhead:
                        fhead.write(metadata)
                    
                    # open a new file for writing body
                    with open(os.path.join(dest, new_file_name + TXT_EXT), 'w') as fbody:
                        fbody.write(escapeXMLChars(
                            subs_text(
                                judgmentBody,
                                SteGarbages
                                )
                            )
                        )
    print("Done...")
                
    
def clean_areios_pagos_text(src, dest, name_pattern=None):
    """Performs pre-processing steps for judgments published by the
    Supreme Civil and Criminal Court (Areios Pagos) and stores new file(s)
    in dest (destination) folder.

    Args:
        src: The root directory that will be traversed with os.walk()

        dest: A path to store cleaned data

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be accessed

    Returns:
        Nothing 
    """
    file_pattern = '*' + TXT_EXT
    if name_pattern is not None:
        file_pattern = name_pattern
        
    for root, dirs, files in os.walk(src):
        #print root
        #print root.replace(src, dest)
        if not os.path.exists(root.replace(src, dest)):
            os.makedirs(root.replace(src, dest))

        for name in files:
            if fnmatch.fnmatch(name, file_pattern):
                #print name
                # modify file name so that no dot is present
                new_file_name = os.path.splitext(name)[0].replace('.', '') + TXT_EXT
                #print new_fil_name
                with open(os.path.join(src, name), 'r') as fin:
                    text = fin.read()
                    cleaned_text = subs_text(text, AreiosPagosGarbages)
                    fout = codecs.open(
                        os.path.join(dest, new_file_name),
                        'w',
                        'UTF-8'
                        )
                    fout.write(escapeXMLChars(cleaned_text).decode('UTF-8'))
                    fout.close()

    print("Done...")


def clean_nsk_text(src, dest, name_pattern=None):
    """Performs pre-processing steps for legal opinions published by the
    Legal Council of State and stores new file(s) in dest (destination)
    folder.

    Args:
        src: The root directory that will be traversed with os.walk()

        dest: A path to store cleaned data

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be accessed

    Returns:
        Nothing 
    """
    HEADER = r'(^.*?(?=Aριθμός|Αριθυός|Αριθμός|Αριθµός|ΑΤΟΜΙΚΗ|ΓNΩΜΟΔΟΤΗΣΗ|ΑΡΙΘ.\s*ΓΝΩΜΟ∆ΟΤΗΣΕΩΣ|Γ Ν Ω Μ Ο Δ Ο Τ Η Σ Η|Αρ. Γνωµ/σεως|Γνωμοδότηση|ΓΝΩΜΟ∆ΟΤΗΣΗ|ΓΝΩΜΟΔΟΤΗΣΗ|ΓΝΩΜΟΔΟΤΗΣΗ|ΑΡΙΘΜΟΣ))'

    file_pattern = '*' + TXT_EXT
    if name_pattern is not None:
        file_pattern = name_pattern

    if not os.path.exists(dest):
        os.makedirs(dest)
    
    for root, dirs, files in os.walk(src):
        for name in files:
            if fnmatch.fnmatch(name, file_pattern):
                print name
                with open(os.path.join(src, name), 'r') as fin:
                    text = fin.read()
                    cleaned_text = subs_text(text, nskGarbages)
                    cleaned_text = re.sub(
                        HEADER,
                        '',
                        cleaned_text,
                        flags=re.DOTALL
                        )
                    # many legal opinions missing embeded text ending
                    count = 0
                    changed_text = ''
                    for char in cleaned_text.decode('utf-8'):
                        if char == '«'.decode('utf-8') or char == '»'.decode('utf-8') :
                            if char == '«'.decode('utf-8'):
                                count += 1
                                changed_text += char
                            elif char == '»'.decode('utf-8'):
                                count -= 1
                                if count == 0:
                                    changed_text += char
                                else:
                                    changed_text += '@' + char
                        else:
                            changed_text += char
                    if count != 0 :
                        print "Warning: missing embeded text ending!"
                    #print changed_text
                    fout = codecs.open(
                        os.path.join(dest, name),
                        'w',
                        'UTF-8'
                        )
                    fout.write(escapeXMLChars(changed_text))
                    fout.close()

    print("Done...")


def GrToLat(src, name_pattern=None):
    """Changes all greek characters in a file name to the corresponding latin
    based on qwerty keyboard. 

    Args:
        src: The root directory that will be traversed with os.walk() 

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be transformed

    Returns:
        Nothing 
    """
    file_pattern = '*' + TXT_EXT
    if name_pattern is not None:
        file_pattern = name_pattern
        
    for root, dirs, files in os.walk(src, topdown=True):
        for name in files:
            if fnmatch.fnmatch(name, file_pattern):
                #print "old_name: "+ name
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
                #print "GrToLat: "+ name
                os.rename(
                    os.path.join(
                        root,
                        old_name),
                    os.path.join(
                        root,
                        name
                        )
                    )

    print("Done...")


def delete_summaries(src, metadata_path=None, name_pattern=None):
    """Checks if legal text(s) contain(s) summary of the decision and deletes
    corresponding file. If metadata_path is defined it also deletes the
    corresponding metadata file.

    Args:
        src: The root directory that contains text files

        metadata_path: The path to file(s) where metadata is stored

        name_pattern: If name_pattern is specified only file names that
            match the pattern will be checked for summaries

    Returns:
        Nothing
    """
    file_pattern = '*' + TXT_EXT
    if name_pattern is not None:
        file_pattern = name_pattern

    # total number of files containing summaries
    cnt = 0
    for root, dirs, files in os.walk(src, topdown=True):
        #print root
        #year = os.path.basename(root)
        for name in files:
            has_summary = 0
            if fnmatch.fnmatch(name, file_pattern):
                with open(os.path.join(src, name), 'r') as fin:
                    summary = re.match(
                        r'^\(Απόσπασμα\)|^Περίληψη',
                        fin.read(),
                        re.DOTALL
                        )
                    #print summary
                    if summary:
                        #print "Found Judgment file with summary: " + name
                        has_summary = 1
                        cnt += 1
                        
                        if metadata_path is not None:
                            meta_file_path = os.path.join(
                                    os.path.join(
                                        metadata_path,
                                        #str(year),
                                        name.split('.')[0]+'_meta' + TXT_EXT
                                        )
                                    )
                            #print meta_file_path
                            meta_file_xists = os.path.isfile(meta_file_path)
                            if meta_file_xists:
                                #print "Metadata File exists, removing: " + meta_file_path
                                os.remove(meta_file_path)
                        
                if has_summary == 1:
                    #print "Removing: " + os.path.join(src, name)
                    os.remove(os.path.join(src, name))

    print "Complete removing summaries. Total Files removed: " + str(cnt)


def fix_fek(path):
    """For issues between 2000-2005 PDFs encoding downloaded from National
    Printing Service is damaged. This function fixes characters using
    replaceChars

    Args:
        path: The root directory that will be traversed with os.walk()

    Returns:
        Nothing 
    """
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        for name in filenames:
            if fnmatch.fnmatch(name, TXT_EXT):
                with open(os.path.join(dirpath,name)+"_pre_", "wt") as fout, open(os.path.join(dirpath,name), "r") as fin:
                    mytext = fin.read()
                    text = replaceChars(mytext)
                    fout.write(text)
                    os.remove(os.path.join(dirpath, name))
                    os.rename(os.path.join(dirpath, name)+"_pre_", os.path.join(dirpath, name))


def valid_xml_char_ordinal(c):
    """Filters out certain bytes so that XML files contains valid
    characters. XML standard defines a valid character as:
    Char ::= #x9 | #xA | #xD | [#x20 - #xD7FF] |
            [#xE000 - #xFFFD] | [#x10000 - #x10FFFF]

    Args:
        c: Character to be checked

    Returns:
        true if character codepoint in valid range
    """
    codepoint = ord(c)
    #conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
    )


def escapeXMLChars(text):
    """Controls characters that need to be escaped (to obtain a well-formed
    XML document)

    Args:
        text: The text that will be escaped (string)

    Returns:
        text: new text containing XML entities instead of characters (string)
    """
    text = text.replace("&", "&amp;")
    #text = text.replace("\"", "&quot;")
    #text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    #text = text.replace(">", "&gt;")
    return text


def validateXML (schemaFile, xmlFile, logFile):
    """Validates a XML file against a XML schema and stores error info
    in a log file
    
    Args:
        schemaFile: The XML schema file
        
        xmlFile: XML file to be checked if it is valid
        
        logFile: Log file where errors will be written
        
    Returns:
        nothing
    """
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
    except:
        #error_log_file.write('XML valid: False\n')
        Akn_LOGGER.info('XML valid: False')
        Akn_LOGGER.info('unknown error!')
        #error_log_file.write('unknown error!')


def CheckXMLvalidity (schemaFile, xmlFile):
    """Checks if a certain XML file is valid against a schema file.

    Args:
        schemaFile: The path to the schema file
        
        xmlFile: The XML file to be checked

    Returns:
        True or False 
    """
    xmlSchemaDoc = etree.parse(schemaFile)
    xmlSchema = etree.XMLSchema(xmlSchemaDoc)
    xml_doc = etree.parse(xmlFile)
    return xmlSchema.validate(xml_doc)


def createHrefFromDictionary (dictionary, splitMultHref = 0, element = 0):
    """Creates an AkomaNtoso href attribute based on a dictionary of elements
    
    Args:
        dictionary: A dictionary containing context nodes with elements.
            Possible keys: type, legalYear, legalNumber,
            ExplicitArthroContext, ExplicitParContext etc.

    Returns:
        href: A unicode href attribute
    """
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
    """Searches for specific dates (e.g. publication date) in a legal text
    and returns a new text containing xml labels about extracted dates

    Args:
        searchNodeElem: The AkomaNtoso node to be searched
        
        regexObj: A compiled regex object that we use for different dates
        
        dateName: The name of the date of interest
            (for example "courtConferenceDate") to be written in node
        
        author: The author is used when creating the attribute 'by'
                of the "step" sublement in the meta section of akoma Ntoso
                
    Returns:
        searchNodeElem: A new node after finding all dates
        
        DateStep: An element that is to be written in workflow
            section of akomaNtoso metadata

        DateTLCEvent: An element that is to be written in references
            section of AkomaNtoso metadata
    """
    for child in searchNodeElem.getchildren():
        childText = etree.tostring(child, pretty_print=True, encoding = 'UTF-8')
        if childText:
            DateOfInterest = re.search(regexObj, childText)
            if DateOfInterest:
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
                DateStep = etree.Element(
                    "step",
                    attrib = {
                        "date" : str(Date),
                        'by' : author,
                        "refersTo" : '#'+dateName
                        }
                    )

                
                DateTLCEvent = etree.Element(
                    "TLCEvent",
                    attrib = {
                        "eId": dateName,
                        "href":"/akn/ontology/event/gr/"+dateName,
                        "showAs": importantDates.get(
                            dateName,
                            'no_important_date_found').decode('utf-8')
                        }
                    )

                return searchNodeElem, DateStep, DateTLCEvent


def extract_data_from_nsk(url, paramsData):
    """Uses requests libary to extract data from NSK
    based on official site search form

    Args:
        url: The url to submit the request
        
        paramsData: post parameters

    Returns:
        dict: A dictionary containin several information such as keywords etc.
    """
    extractedData = {}
    try:
        req = requests.post(url, params=paramsData)

        if req.status_code == 200:
            page = html.fromstring(req.content.decode('utf-8'))
            dataToExtract = page.xpath('//div[@class="article_text"]/p/text()')
            if dataToExtract:
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
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
        )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger          


def textToNumbering(text, dictionary):
    """Converts a small text to the corresponding ID (naming convention).
    This is due the fact that legislators sometimes refer to an element
    not using a number but a combination of number and a string
    eg 32A, First, Second etc.

    Args:
        text: A portion of text
        
        dictionary: A dictionary that holds values
        
    Returns:
        elemID: The corresponding element id
        
    """
    elemID = []
    # Problem with python Greek letters,
    # convert dictionary keys and values to unicode text
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
    """Get the token name of a rule context that triggered a grammar rule.
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
    """Fixes the XML string in order to be a valid XML string. It is used
    for cases where a ref tag closes after a new paragraph tag (</p><p>)

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
                newString = string.replace(
                    re.search(
                        regPatternObj,
                        string
                        ).group(0),
                    ' ')
                text = text.replace(string, newString)
    return text
