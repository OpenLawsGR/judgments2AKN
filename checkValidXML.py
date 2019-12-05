# -*- coding: utf-8 -*-
import os
import sys
import fnmatch
import time
import argparse
from functions import CheckXMLvalidity
from variables import *
from lxml import etree

program_description = 'Validate XML files against Akoma Ntoso XSD schema '

parser = argparse.ArgumentParser(
    description = program_description
    )

legal_authority_help = 'choose a specific legal authority '
legal_authority_help += '(accepted values: %(choices)s) to perform validation'
parser.add_argument(
    'legal_authority',
    metavar = 'legal_authority',
    choices = [AREIOS_PAGOS, STE, NSK],
    help = legal_authority_help
    )

year_help = 'choose a specific year to perform validation'
parser.add_argument(
    '-year',
    help = year_help
    )

# create a namespace object
args = parser.parse_args()

if __name__ == '__main__':
    print args

    source_path = os.path.join(
        os.getcwd(),
        os.path.join(
            XML,
            args.legal_authority
            )
        )

    # legal opinions are not stored in folders by year of publication
    if args.year is not None and args.legal_authority not in (NSK):
        source_path = os.path.join(
            source_path,
            args.year
            )
        
    #print source_path
    print "Starting validation in : " + source_path
    time.sleep(2)

    total_files_cnt = 0
    total_xml_files = 0
    total_xml_valid = 0
    total_xml_nonValid = 0
    
    validXML = 0
    nonValidXML = 0
    XmlFiles = 0
    filesCnt = 0
    for root, dirs, files in os.walk(source_path):  
        for name in files:
            print name
            total_files_cnt += 1
            if fnmatch.fnmatch(name, '*' + XML_EXT):
                total_xml_files += 1
                if CheckXMLvalidity(
                    'akomantoso30.xsd',
                    os.path.join(
                        root,
                        name
                        )
                    ) == 1:
                    #print name + ": Valid"
                    total_xml_valid += 1
                else:
                    #print name + ": Not Valid"
                    total_xml_nonValid += 1
    
    print "Total Files :" + str(total_files_cnt)
    print "Total XML Files :" + str(total_xml_files)
    print "Valid XML :" + str(total_xml_valid)
    print "Non Valid XML : " + str(total_xml_nonValid)
