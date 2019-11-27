# -*- coding: utf-8 -*-
import fnmatch
import os
import codecs
from functions import pdfToText, GrToLat, subs_text, escapeXMLChars
from functions import checkForSummaries
from variables import SteGarbages, AreiosPagosGarbages, nskGarbages, grToLat

BASE_URL_MAIN =  os.path.join(os.getcwd(), 'legal_crawlers/data')
BASE_URL_DEST = os.path.join(os.getcwd(), 'pdftotext')
#RULES_FILE = os.path.join(os.getcwd(), 'replacements')

#declare which folder to start from
FOLDER_PATH = r'ste'

#declare ste metadata folder name
STE_METADATA = r'ste_metadata'
STE_METADATA_FOLDER = os.path.join(BASE_URL_DEST, STE_METADATA)

if __name__ == '__main__':
    
    SRC = os.path.join(BASE_URL_MAIN, FOLDER_PATH)
    DEST = os.path.join(BASE_URL_DEST, FOLDER_PATH)
    folder = os.path.basename(SRC)
    #print "Folder: " + folder
    
    if folder in ('nsk'):
        # 1st step -> get text from pdf files
        pdfToText(SRC, DEST)

        # 2st step -> create latin names of files
        GrToLat(DEST)

        # 3rd step -> remove garbages from files
        HEADER = r'(^.*?(?=Aριθμός|Αριθυός|Αριθμός|Αριθµός|ΑΤΟΜΙΚΗ|ΓNΩΜΟΔΟΤΗΣΗ|ΑΡΙΘ.\s*ΓΝΩΜΟ∆ΟΤΗΣΕΩΣ|Γ Ν Ω Μ Ο Δ Ο Τ Η Σ Η|Αρ. Γνωµ/σεως|Γνωμοδότηση|ΓΝΩΜΟ∆ΟΤΗΣΗ|ΓΝΩΜΟΔΟΤΗΣΗ|ΓΝΩΜΟΔΟΤΗΣΗ|ΑΡΙΘΜΟΣ))'
        if not os.path.exists(os.path.join(BASE_URL_DEST, 'nsk_no_garbage')):
            os.makedirs(os.path.join(BASE_URL_DEST, 'nsk_no_garbage'))
        
        for root, dirs, files in os.walk(DEST):
            for name in files:
                if fnmatch.fnmatch(name, '*.txt'):
                    print name
                    with open(os.path.join(DEST, name), 'r') as fin:
                        text = fin.read()
                        data = subs_text(text, nskGarbages)
                        count = 0
                        changedText = ''
                        for char in data.decode('utf-8'):
                            if char == '«'.decode('utf-8') or char == '»'.decode('utf-8') :
                                if char == '«'.decode('utf-8'):
                                    count += 1
                                    changedText += char
                                elif char == '»'.decode('utf-8'):
                                    count -= 1

                                    if count == 0:
                                        changedText += char
                                    else:
                                        changedText += '@' + char
                                        #changedText += char
                            else:
                                changedText += char
                        if count != 0 :
                            print "Warning: missing embeded text ending!"
                        #print changedText
                        #print type(changedText)
                        #sys.exit()
                        fout = codecs.open(os.path.join(os.path.join(BASE_URL_DEST, 'nsk_no_garbage'), name), 'w', 'UTF-8')
                        fout.write(escapeXMLChars(changedText))
                        fout.close()
            
    elif folder in ('ste'):
        # 1st step -> remove garbages from files
        HEADER = r'(^.*?\n\s*(?=Ε.Ο. Aριθμός|Αριθμός|Aριθμός|Αριθμό|ΑΡΙΘΜΟΣ|ΣτΕ\s*\d+|ΟλΣτΕ\s*\d+|\(Απόσπασμα\)|\(Α π ό σ π α σ μ α\)))'

        # For every judgment into directory 'legal_crawlers/data/ste',
        for year in range (1990, 2018):
            for root, dirs, files in os.walk(os.path.join(SRC, str(year))):

                # create a corresponding year folder into 'post_processing/ste',
                if not os.path.exists(os.path.join(DEST, str(year))):
                    os.makedirs(os.path.join(DEST, str(year)))

                # create a corresponding year folder into 'post_processing' that holds metadata,  
                if not os.path.exists(os.path.join(STE_METADATA_PATH, str(year))):
                    os.makedirs(os.path.join(STE_METADATA_PATH, str(year)))

                for name in files:
                    # create new file name so that it contains year of publication
                    new_file_name = name.split('.')[0] + '_' + str(year)

                    if fnmatch.fnmatch(name, '*.txt'):
                        print name
                        # declare full path for each file where metadata will be stored  
                        metaFilePath = os.path.join(os.path.join(STE_METADATA_PATH, str(year)), new_file_name + '_meta.txt')
                        #print metaFilePath
                        
                        with open(os.path.join(os.path.join(SRC, str(year)), name), 'r') as fin:
                            # by default the first 10 lines contain metadata
                            # see ste crawler
                            judgmentText_ = fin.readlines()
                            metadata = ''
                            judgmentBody = ''

                            for line in judgmentText_[:10]:
                                metadata += line

                            for line in judgmentText_[11:]:
                                judgmentBody += line
                                
                            # we open a new file for writing metadata
                            with open(metaFilePath, 'w') as fhead:
                                fhead.write(metadata)
                                
                            # we open a new file for writing body
                            with open(os.path.join(os.path.join(DEST, str(year)), new_file_name + '.txt'), 'w') as fbody:
                                fbody.write(escapeXMLChars(subs_text(judgmentBody, SteGarbages)))

                            '''
                            # 2nd option (read file until HEADER text and write accordingly)
                            #judgmentText = fin.read()
                            try:
                                header = re.match(HEADER, judgmentText, re.DOTALL).group(0)
                                judgmentBody = judgmentText.replace(header, '', 1)

                                # Open a new file for writing metadata
                                with open(metaFilePath, 'w') as fhead:
                                    fhead.write(header)

                                # Open a new file for writing body
                                with open(os.path.join(os.path.join(DEST, str(year)), name), 'w') as fbody:
                                    fbody.write(escapeXMLChars(subs_text(judgmentBody, SteGarbages)))

                            # If no header exists write all text to new file
                            except AttributeError:
                                with open(os.path.join(os.path.join(DEST, str(year)), name), 'w') as fbody:
                                    fbody.write(escapeXMLChars(subs_text(judgmentText, SteGarbages)))
                                #pass
                            '''

        # 2nd step -> create latin names of files
        GrToLat(DEST)

        # 3rd step -> create latin names of metadata files
        GrToLat(STE_METADATA_PATH)

        # 4th step -> Chek for summaries in judgment files and remove them
        checkForSummaries(DEST, STE_METADATA_PATH)
        
    elif folder in ('areios_pagos'):
        # 1st step -> create latin names of files
        GrToLat(DEST)
        
        # 2st step -> create latin names of metadata files Traverse directory 'areios_pagos'
        # inside directory 'legal_crawlers', remove garbages, escape XML invalid characters
        # and write text to a new destination
        for year in range (1990, 2019):
            for root, dirs, files in os.walk(os.path.join(SRC, str(year))):
                #print os.path.join(SRC, str(year))

                if not os.path.exists(os.path.join(DEST, str(year))):
                    os.makedirs(os.path.join(DEST, str(year)))
                
                for name in files:
                    if fnmatch.fnmatch(name, '*.txt'):
                        print name
                        # remove dots from basename
                        filename = os.path.splitext(name)[0].replace('.', '') + '.txt'
                        with open(os.path.join(os.path.join(SRC, str(year)), name), 'r') as fin:
                            data = fin.read()
                            text = subs_text(data, AreiosPagosGarbages)
                            #print text
                            fout = codecs.open(os.path.join(os.path.join(DEST, str(year)), filename), 'w', 'UTF-8')
                            fout.write(escapeXMLChars(text).decode('utf-8'))
                            fout.close()

        #sys.exit()

        # 3rd step -> Chek for summaries in judgment files and remove them
        cnt = 0
        for year in range (1990, 2019):
            for root, dirs, files in os.walk(os.path.join(DEST, str(year))):
                for name in files:
                    hasSummary = 0
                    if fnmatch.fnmatch(name, '*.txt'):
                        with open(os.path.join(os.path.join(DEST, str(year)), name), 'r') as fin:
                            summary = re.match(r'^Περίληψη', fin.read(), re.DOTALL)
                            #print summary
                            if summary:
                                print "Found Judgment File with summary: " + name
                                hasSummary = 1
                                cnt += 1
                        if hasSummary == 1:
                            print "Removing: " + os.path.join(os.path.join(DEST, str(year)), name)
                            os.remove(os.path.join(os.path.join(DEST, str(year)), name))
        print "Total Files: " + str(cnt)
        #sys.exit()

        """
        # This is just for escaping XML invalid characters
        # This is for files inside DEST (pdftotext) directory
        # create a temporary file, remove old file and rename new one
        for year in range (1997, 2018):
            for root, dirs, files in os.walk(os.path.join(DEST, str(year))):
                for name in files:
                    if fnmatch.fnmatch(name, '*.txt'):
                        print name
                        filename = name
                        #print os.path.join(root, filename)
                        with open(os.path.join(os.path.join(DEST, str(year)), name), 'r') as fin:
                            data = fin.read()
                            #print data
                            fout = codecs.open(os.path.join(root, name).split('.')[0] + '_tmp_.txt', 'w', 'UTF-8')
                            fout.write(escapeXMLChars(data).decode('utf-8'))
                            fout.close()

                        os.remove(os.path.join(root, name))
                        #print os.path.join(root, name).split('.')[0]+"_tmp_nogarb.txt"
                        os.rename(os.path.join(root, name).split('.')[0]+"_tmp_.txt", os.path.join(root, filename))
        """   
    else:
        print "No folder found! Check if folder name exists!"
        

    
