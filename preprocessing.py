# -*- coding: utf-8 -*-
import argparse
import fnmatch
import os
import sys
import codecs
import time
from functions import clean_areios_pagos_text, clean_ste_text, clean_nsk_text 
from functions import delete_summaries, pdf_to_text, copy_files, GrToLat
from variables import TXT_EXT, PDF_EXT, STE, NSK, NSK_TMP, AREIOS_PAGOS
from variables import STE_METADATA, NSK_METADATA, NSK_CSTM_METADATA

program_description = 'A Command Line Interface for implementing the '
program_description += 'pre-processing steps for judgments and legal pinions '
program_description += 'of the three major legal authorities of Greece. '
program_description += 'Pre-processing steps include garbage removal,'
program_description += 'escaping XML invalid characters and metadata '
program_description += 'storage management (if available)' 

parser = argparse.ArgumentParser(
    description = program_description,
    epilog = 'Enjoy the program!'
    )

legal_authority_help = 'run pre-processing steps for a specific legal '
legal_authority_help += 'authority (accepted values: %(choices)s)'
parser.add_argument(
    'legal_authority',
    metavar = 'legal_authority',
    choices = [AREIOS_PAGOS, STE, NSK],
    help = legal_authority_help
    )

src_help = 'define base folder where judgments and legal opinions ' 
src_help += 'are stored (default is legal_crawlers\data). A different path '
src_help += 'can be provided if legal texts are stored in a different folder'
parser.add_argument(
    '-src',
    default = os.path.join('legal_crawlers', 'data'),
    metavar = 'SOURCE',
    help = src_help
    )

dest_help = 'define a name for base folder where judgments and legal opinions ' 
dest_help += 'will be stored after pre-processing (default is pdftotext)'
parser.add_argument(
    '-dest',
    default = r'pdftotext',
    metavar = 'DESTINATION',
    help = dest_help
    )

year_help = 'choose a specific year for pre-processing (if absent ' 
year_help += 'all years will be included)'
parser.add_argument(
    '-year',
    help = year_help
    )

parser.add_argument(
    '-fn',
    metavar = 'FILENAME',
    help = 'choose a specific file for pre-processing'
    )

# create a namespace object
args = parser.parse_args()

if __name__ == '__main__':
    #print args

    if args.src == args.dest:
        parser.error(
            'destination folder must be different from source folder'
            )

    if args.fn is not None:
        if args.year is None and args.legal_authority not in (NSK):
            parser.error(
                'You must provide "year" parameter ' +
                'in order to process a specific file'
                )
        else:
            file_pattern = '*' + args.fn
    else:
        file_pattern = '*' + TXT_EXT
    

    source_path = os.path.join(
        os.getcwd(),
        os.path.join(
            args.src,
            args.legal_authority
            )
        )

    # legal opinions are not stored in folders by year of publication
    if args.year is not None and args.legal_authority not in (NSK):
        source_path = os.path.join(
            source_path,
            args.year
            )

    dest_path = os.path.join(
        os.getcwd(),
        os.path.join(
            args.dest,
            args.legal_authority
            )
        )

    # legal opinions are not stored in folders by year of publication
    if args.year is not None and args.legal_authority not in (NSK):
        dest_path = os.path.join(dest_path, args.year)
    
    #print source_path
    #print dest_path
    #print file_pattern
    #sys.exit()

    if args.legal_authority in (AREIOS_PAGOS):
        # 1st step: traverse src directory and clean text
        print("Start cleaning data...")
        time.sleep(2)
        clean_areios_pagos_text(source_path, dest_path, file_pattern)

        # 2nd step: create latin names of files
        print("Creating latin names for file(s)...")
        time.sleep(2)
        GrToLat(dest_path)

        # 3rd step: some texts contain only summaries
        # and not full decision body
        # check for summaries and remove them
        print("Start searching for summaries...")
        time.sleep(2)
        delete_summaries(dest_path)

    elif args.legal_authority in (STE):
        # 1st step: traverse src directory and clean text
        print("Start cleaning data...")
        time.sleep(2)
        clean_ste_text(source_path, dest_path, file_pattern)

        # 2nd step -> create latin names of files
        print("Creating latin names for file(s)...")
        time.sleep(2)
        GrToLat(dest_path)

        # 3rd step -> create latin names of metadata files
        print("Creating latin names for metadata file(s)...")
        time.sleep(2)
        GrToLat(dest_path.replace(STE, STE_METADATA))

        # 4th step -> chek for summaries and remove them
        print("Start searching for summaries...")
        time.sleep(2)
        delete_summaries(dest_path, dest_path.replace(STE, STE_METADATA))

    elif args.legal_authority in (NSK):
        # 1st step -> get text from pdf files
        # pdf_to_text deals with PDF files temporarily change extension
        print("Converting PDF file(s) to text...")
        time.sleep(2)
        tmp_file_pattern = file_pattern.replace(TXT_EXT, PDF_EXT)
        pdf_to_text(
            source_path,
            dest_path.replace(NSK, NSK_TMP),
            tmp_file_pattern
            )

        # 2nd step -> clean text
        print("Start cleaning data...")
        time.sleep(2)
        tmp_file_pattern = file_pattern.replace(PDF_EXT, TXT_EXT)
        clean_nsk_text(
            dest_path.replace(NSK, NSK_TMP),
            dest_path,
            tmp_file_pattern
            )
        
        # 3rd step -> copy metadata files downloaded from diavgeia
        # to a new destination
        print("Copying metadata file(s) to dest...")
        time.sleep(2)
        #tmp_file_pattern = file_pattern.replace(PDF_EXT, TXT_EXT)
        copy_files(
            source_path,
            dest_path.replace(NSK, NSK_METADATA),
            tmp_file_pattern
            )

        # 4th step -> create latin names of files
        print("Creating latin names for file(s)...")
        time.sleep(2)
        GrToLat(dest_path.replace(NSK, NSK_TMP))
        GrToLat(dest_path)

        # 5th step -> create latin names of metadata files
        print("Creating latin names for metadata file(s)...")
        time.sleep(2)
        GrToLat(dest_path.replace(NSK, NSK_METADATA))

        # TODO: 6th step -> download custom metadata from official
        # Legal Council of State website
        #print ("In order to create some appropriate Akoma Ntoso XML " +
        #       "metadata nodes, you are advised to execute " +
        #       "extractLegalOpinionsCstmMetadata.py (with no arguments)")
        
