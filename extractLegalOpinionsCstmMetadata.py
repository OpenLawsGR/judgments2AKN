# -*- coding: utf-8 -*-
import os
import sys
import fnmatch
import argparse
from functions import extract_data_from_nsk
from variables import NSK_METADATA, NSK_CSTM_METADATA, NSK, TXT_EXT
from variables import LEGAL_TEXTS
from lxml import etree


program_description = 'A module for downloading specific data (e.g. keywords) '
program_description += 'from Legal Council of State official website. '
program_description += 'Extracted data may be used later to build some '
program_description += 'appropriate Akoma Ntoso metadata nodes.'

parser = argparse.ArgumentParser(
    description = program_description
    )

parser.add_argument(
    '-fn',
    metavar = 'FILENAME',
    help = 'choose a specific legal opinion to extract data'
    )

# create a namespace object
args = parser.parse_args()

if __name__ == '__main__':

    source_path = os.path.join(
        os.getcwd(),
        os.path.join(
            LEGAL_TEXTS,
            NSK
            )
        )

    if args.fn is not None:
        file_pattern = '*' + args.fn
    else:
        file_pattern = '*' + TXT_EXT

    #print(source_path)
    
    # Create custom metadata folder if it does not exist
    if not os.path.exists(source_path.replace(NSK, NSK_CSTM_METADATA)):
        os.makedirs(source_path.replace(NSK, NSK_CSTM_METADATA))

    for root, dirs, files in os.walk(source_path):
        for name in files:
            #print name
            if fnmatch.fnmatch(name, file_pattern):
                print name
                # check metadata folder if meta_file exists
                # open and get post parameters
                meta_file_exists = os.path.isfile(
                    os.path.join(
                        source_path.replace(NSK, NSK_METADATA),
                        name
                        )
                    )

                if meta_file_exists:
                    with open(
                        os.path.join(
                            source_path.replace(NSK, NSK_METADATA),
                            name
                            ),
                        'r') as fin:
                        XML = etree.parse(fin)
                        #print XML.getroot().nsmap
                        XML_root = XML.getroot()
                        #print list(root.nsmap.values())[0]
                        try:
                            ns = list(XML_root.nsmap.values())[0]
                            protocolNumber = XML.findtext(
                                '//ns:protocolNumber',
                                namespaces = {'ns' : ns}
                                )
                            issueDate = XML.findtext(
                                '//ns:issueDate',
                                namespaces = {'ns' : ns}
                                )
                        except IndexError:
                            protocolNumber = XML.findtext(
                                '//protocolNumber'
                                )
                            issueDate = XML.findtext(
                                '//issueDate'
                                )
                    try:
                        issueYear = protocolNumber.split('/')[1]
                    except IndexError:
                        issueYear = issueDate.split('-')[0]

                    decisionNumber = protocolNumber.split('/')[0]
                    #print issueYear
                    #print decisionNumber

                    # Create POST url (based in NSK search form) and POST data
                    post_url ='http://www.nsk.gr/web/nsk/'
                    post_url +='anazitisi-gnomodoteseon'
                    post_url +='?p_p_id=nskconsulatories_WAR_nskplatformportlet'
                    post_url +='&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view'
                    post_url +='&p_p_col_id=column-4&p_p_col_pos=2'
                    post_url +='&p_p_col_count=3'
                    #print post_url
                    
                    post_data = {
                        "_nskconsulatories_WAR_nskplatformportlet_isSearch" : "1",
                        "_nskconsulatories_WAR_nskplatformportlet_inputSuggestionNo" : decisionNumber,
                         "_nskconsulatories_WAR_nskplatformportlet_inputDatefrom" : issueYear,
                        "_nskconsulatories_WAR_nskplatformportlet_consulState":"null"
                        }
                
                    extracted_data = extract_data_from_nsk(post_url, post_data)
                    #print extracted_data
                    if extracted_data:
                        # Create a custom element that will hold extracted data
                        custom_metadata = etree.Element("customMetadata")
                        keywords = etree.SubElement(custom_metadata, 'keywords')
                        cnt = 0
                        for keyword in extracted_data['keywords']:
                            # If its is not empty string
                            if keyword:
                                cnt += 1
                                keyword_elem = etree.SubElement(
                                    keywords,
                                    'keyword_' + str(cnt)
                                    )
                                keyword_elem.text = keyword.strip()

                        chairman = etree.SubElement(custom_metadata, 'chairman')
                        chairman.text = extracted_data['chairman']
                        rapporteur = etree.SubElement(custom_metadata, 'rapporteur')
                        rapporteur.text = extracted_data['rapporteur']
                        status = etree.SubElement(custom_metadata, 'status')
                        status.text = extracted_data['status']

                        #print etree.tostring(
                        #    custom_metadata,
                        #    pretty_print=True,
                        #    encoding="UTF-8"
                        #    )
                        XmlTree = etree.ElementTree(custom_metadata)

                        # Write ElementTree to file
                        with open(
                            os.path.join(
                                source_path.replace(NSK, NSK_CSTM_METADATA),
                                name),
                            'w') as fin:
                            fin.write(
                                etree.tostring(
                                    XmlTree,
                                    pretty_print = True,
                                    encoding = "UTF-8",
                                    xml_declaration = True
                                    )
                                )
