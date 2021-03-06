# -*- coding: utf-8 -*-
#########################################################################
##### Defines a set of variables that are used in different modules #####
#########################################################################
import re


"""Define files extensions"""
TXT_EXT = '.txt'
XML_EXT = '.xml'
PDF_EXT = '.pdf'


"""Define custom variables"""
STE = 'ste'
STE_METADATA = 'ste_metadata'
NSK = 'nsk'
NSK_TMP = 'nsk_tmp'
NSK_METADATA = 'nsk_metadata'
NSK_CSTM_METADATA = 'nsk_custom_metadata'
AREIOS_PAGOS = 'areios_pagos'
LEGAL_CRAWLERS = 'legal_crawlers'
DATA = 'data'
LEGAL_TEXTS = 'legal_texts'
LOGS = 'logs'
XML = 'XML'
XML_NO_NER = 'XML_NO_NER'
NER = 'NER'

"""This is a dictionary containing most of the code laws found in legal
texts and the corresponding type of legal document that certifies them.
Formal type is always type_number_year"""
codeLaws = {
    'KWDIKAS_POLITIKWN_KAI_STRATIWTIKWN_SUNTAKSEWN' : 'act/presidentialDecree_169_2007',
    'KWDIKAS_FOROLOGIKIS_DIADIKASIAS' : 'act/law_4174_2013',
    'YPALLILIKOS_KWDIKAS' : 'act/law_3528_2007',
    'AGROTIKOS_KWDIKAS' : 'act/royalDecree_29.10_1949',
    'ALIEUTIKOS_KWDIKAS' : 'act/decreeLaw_420_1970',
    'ASTIKOS_KWDIKAS' : 'act/compulsoryLaw_2783_1941',
    'AGORANOMIKOS_KWDIKAS': 'act/decreeLaw_136_1946',
    'GENIKOS_OIKODOMIKOS_KANONISMOS' : 'act/royalDecree_9_1955',
    'NEOS_OIKODOMIKOS_KANONISMOS' : 'act/law_4067_2012',
    'KWDIKAS_ADEIWN_FORTIGWN_AUTOKINITWN' : 'act/royalDecree_281_1973',   
    'KWDIKAS_APODIMIAS_METANASTEUSIS_DIAVATIRIA': 'act/presidentialDecree_417_1993',    
    'KWDIKAS_DEONTOLOGIAS_DIKIGORIKOU_LEITOURGIMATOS' : 'lawSocietyAthens_04.01_1980',
    'KWDIKAS_DIATAGMATWN_GIA_DIMOTOLOGIA' : 'act/presidentialDecree_497_1991',
    'KWDIKAS_DIATAKSEWN_STRATOLOGIKIS_FISIS' : 'act/presidentialDecree_292_2003',
    'KWDIKAS_ELLINIKIS_ITHAGENEIAS' : 'act/law_3284_2004',
    'KWDIKAS_ESODWN_DIMWN_KAI_KOINOTITWN' : 'act/royalDecree_24_1958',
    'KWDIKAS_ESODWN_DIMWN_KAI_KOINOTITWN' : 'act/decreeLaw_86_1969',
    'KWDIKAS_AEROPORIKOY_DIKAIOY' : 'act/law_1815_1988',
    'KWDIKAS_KATASKEUIS_DIMOSIWN_ERGWN' : 'act/law_3669_2008',
    'KWDIKAS_NOMOTHESIAS_KUVERNISIS' : 'act/presidentialDecree_63_2005',
    'KWDIKAS_NOMWN_GIA_NARKWTIKA' : 'law_3459_2006',
    'KWDIKAS_PAROXIS_EPENDITIKWN_KINITRWN' : 'act/presidentialDecree_456_1995',
    'KWDIKAS_PAROXIS_EPENDITIKWN_KINITRWN' : 'act/presidentialDecree_9_1932',
    'KWDIKAS_SYNALLAGWN_HLEKTRIKIS_ENERGEIAS' : 'act/ministerialDecision_D5/HL/B/F1/8988_2001',
    'KWDIKAS_TAMEIOU_NOMIKWN' : 'act/decreeLaw_4114_1960',
    'KWDIKAS_TROFIMWN_KAI_POTWN' : 'GeneralChemicalStateLaboratory_1100_1987',
    'KWDIKAS_FOROLOGIAS_KAPNOU' : 'act/royalDecree_13_1920',
    'KWDIKAS_FOROLOGIKWN_STOIXEIWN' : 'act/presidentialDecree_99_1977',
    'KWDIKAS_ANAGK_APAL_AKINITWN' : 'act/law_2882_2001',
    'KWDIKAS_BIBLIWN_KAI_STOIXEIWN' : 'act/presidentialDecree_186_1992',
    'KWDIKAS_POINIKIS_DIKONOMIAS' : 'act/presidentialDecree_258_1986',
    'POINIKOS_KWDIKAS' : 'act/presidentialDecree_283_1985',
    'ETHNIKOS_TELWNIAKOS_KWDIKAS' : 'act/law_2960_2001',
    'KWDIKAS_FOROLOGIAS_EISODIMATOS' : 'act/law_4172_2013',
    'KWDIKAS_BASIKIS_POLEODOMIKIS_NOMOTHESIAS' : 'act/presidentialDecree_14_1999',
    'KTINOTROFIKOS_KWDIKAS' : 'act/decreeLaw_203_1969',
    'KWDIKAS_TELWN_XARTOSIMOU' : 'act/decreeLaw_4755_1930',
    'KWDIKAS_BASIKWN_KANONWN_KRATOUMENWN' : 'act/law_1851_1989',
    'KWDIKAS_FOROLOGIKIS_DIKONOMIAS' : 'act/presidentialDecree_331_1985',
    'KWDIKAS_DIKIGORWN' : 'act/law_4194_2013',
    'KWDIKAS_DIMOSIOU_LOGISTIKOU' : 'act/law_2362_1995',
    'KWDIKAS_DIMOSIOU_NAUTIKOU_DIKAIOU' : 'act/decreeLaw_187_1973',
    'KWDIKAS_FOROY_PROSTITHEMENIS_AKSIAS' : 'act/law_2859_2000',
    'KWDIKAS_POLITIKIS_DIKONOMIAS' : 'act/presidentialDecree_503_1985',
    'KWDIKAS_DHMWN_KAI_KOINOTITWN' : 'act/law_3463_2006',
    'KWDIKAS_ODIKIS_KYKLOFORIAS' : 'act/law_2696_1999',
    'KWDIKAS_DIKASTIKOU_SWMATOS_ENOPLWN_DINAMEWN' :  'act/law_2304_1995',
    'KWDIKAS_DIKASTIKWN_EPIMELITWN' : 'act/law_2318_1995',
    'KWDIKAS_ORGANISMOU_DIKASTIRIWN' : 'act/law_1756_1988',
    'KWDIKAS_DIKASTIKWN_YPALLHLWN' : 'act/law_2812_2000',  
    'KWDIKAS_DIKWN_DIMOSIOU' : 'act/royalDecree_26.6_1944',
    'KWDIKAS_DIOIKITIKIS_DIADIKASIAS' : 'act/law_2690_1999',
    'KWDIKAS_DIOIKITIKIS_DIKONOMIAS' : 'act/law_2717_1999',
    'KWDIKAS_EISPRAKSEWN_DHMOSIWN_ESODWN' : 'act/decreeLaw_356_1974',
    'KWDIKAS_FARMAKEUTIKIS_DEONTOLOGIAS' : 'act/presidentialDecree_340_1993',
    'KWDIKAS_IDIWTIKOU_NAUTIKOU_DIKAIOU' : 'act/law_3816_1958',
    'KWDIKAS_POLEMIKWN_SYNTAKSEWN' : 'act/presidentialDecree_168_2007',
    'KWDIKAS_METOXIKOU_TAMEIOU_POLITIKWN_YPALLHLWN' : 'act/presidentialDecree_422_1981',
    'KWDIKAS_METOXIKOU_TAMEIOU_STRATOU' : 'act/decreeLaw_24_1927',
    'KWDIKAS_PROSOPIKOU_LIMENIKOU_SWMATOS' : 'act/law_3079_2002',
    'KWDIKAS_SYMVOLEOGRAFWN' : 'act/law_2830_2000',   
    'KWDIKAS_SYNTAKSEWN_PROSOPIKOU_OSE' : 'act/presidentialDecree_167_2000',
    'KWDIKAS_ANOTATOU_EIDIKOU_DIKASTIRIOU' : 'act/law_345_1976',
    'KWDIKAS_FOROLOGIAS_KLIRONOMIWN' : 'act/law_2961_2001',
    'KWDIKAS_FOROLOGIKIS_APEIKONISIS_SYNALLAGWN' : 'act/law_4390_2012'
    }


"""A dictionary containing all context nodes of courts based on grammar.
it is used to create the court part of a judgment reference"""
courts = {
    'STE' : 'COS',
    'SUPREME_COURT' : 'SCCC',
    'AED' : 'SuperiorSpecialCourt',
    'MAGISTRATE_COURT_OF_THESSALONIKI' : 'MagistrateCourtThessaloniki',
    'MAGISTRATE_COURT_OF_LAMIA' : 'MagistrateCourtLamia',
    'MAGISTRATE_COURT_OF_PIRAEUS' : 'MagistrateCourtPiraeus',
    'MAGISTRATE_COURT_OF_ATHENS' : 'MagistrateCourtAthens',
    'APELLATE_COURT_OF_ATHENS' : 'AppelateCourtAthens',
    'APELLATE_COURT_OF_LAMIA': 'AppelateCourtLamia',
    'APELLATE_COURT_OF_PIRAEUS' : 'AppelateCourtPiraeus',
    'APELLATE_COURT_OF_THESSALONIKI' : 'AppelateCourtThessaloniki',
    'APELLATE_COURT_OF_CORFU' : 'AppelateCourtCorfu',    
    'APELLATE_COURT_OF_THRAKI' : 'AppelateCourtThraki',
    'APELLATE_COURT_OF_IOANNINA' : 'AppelateCourtIoannina',
    'APELLATE_COURT_OF_DODEKANISA' : 'AppelateCourtDodekanisa',
    'APELLATE_COURT_OF_AEGEAN' : 'AppelateCourtAegean',
    'APELLATE_COURT_OF_CRETE' : 'AppelateCourtCrete',
    'APELLATE_COURT_OF_WEST_MACEDONIA' : 'AppelateCourtWestMacedonia',
    'APELLATE_COURT_OF_LARISA' : 'AppelateCourtLarisa',
    'APELLATE_COURT_OF_NAFPLIO' : 'AppelateCourtNafplio',
    'APELLATE_COURT_OF_PATRAS' : 'AppelateCourtPatras',
    'APELLATE_COURT_OF_WEST_STEREAS' : 'AppelateCourtWestStereas',
    'APELLATE_COURT_OF_NORTH_AEGEAN' : 'AppelateCourtNorthAegean',
    'APELLATE_COURT_OF_EAST_CRETE' : 'AppelateCourtEastCrete',
    'APELLATE_COURT_OF_KALAMATA' : 'AppelateCourtKalamata',
    'APELLATE_COURT_OF_EVOIA' : 'AppelateCourtEvoia',    
    'FIRST_INSTANCE_COURT_OF_ATHENS' : 'FirstInstanceCourtAthens',
    'FIRST_INSTANCE_COURT_OF_LAMIA' : 'FirstInstanceCourtLamia',
    'FIRST_INSTANCE_COURT_OF_AMFISSA' : 'FirstInstanceCourtAmfissa',
    'FIRST_INSTANCE_COURT_OF_EVRITANIA' : 'FirstInstanceCourtEvritania',
    'FIRST_INSTANCE_COURT_OF_LIVADIA' : 'FirstInstanceCourtLivadia',
    'FIRST_INSTANCE_COURT_OF_PIRAEUS' : 'FirstInstanceCourtPiraeus',
    'FIRST_INSTANCE_COURT_OF_THESSALONIKI' : 'FirstInstanceCourtThessaloniki',
    'FIRST_INSTANCE_COURT_OF_VEROIA' : 'FirstInstanceCourtVeroia',
    'FIRST_INSTANCE_COURT_OF_EDESSA' : 'FirstInstanceCourtEdessa',
    'FIRST_INSTANCE_COURT_OF_KATERINI' : 'FirstInstanceCourtKaterini',
    'FIRST_INSTANCE_COURT_OF_KILKIS' : 'FirstInstanceCourtKilkis',
    'FIRST_INSTANCE_COURT_OF_SERRES' : 'FirstInstanceCourtSerres',
    'FIRST_INSTANCE_COURT_OF_XALKIDIKI' : 'FirstInstanceCourtXalkidiki',
    'FIRST_INSTANCE_COURT_OF_CORFU' : 'FirstInstanceCourtCorfu',
    'FIRST_INSTANCE_COURT_OF_GIANNITSA' : 'FirstInstanceCourtGiannitsa',
    'FIRST_INSTANCE_COURT_OF_THESPRWTIA' : 'FirstInstanceCourtThesprwtia',    
    'FIRST_INSTANCE_COURT_OF_RODOPI' : 'FirstInstanceCourtRodopi',
    'FIRST_INSTANCE_COURT_OF_DRAMA' : 'FirstInstanceCourtDrama',
    'FIRST_INSTANCE_COURT_OF_EVROS' : 'FirstInstanceCourtEvros',
    'FIRST_INSTANCE_COURT_OF_KAVALA' : 'FirstInstanceCourtKavala',
    'FIRST_INSTANCE_COURT_OF_XANTHI' : 'FirstInstanceCourtXanthi',
    'FIRST_INSTANCE_COURT_OF_ORESTIADA' : 'FirstInstanceCourtOrestiada',
    'FIRST_INSTANCE_COURT_OF_IOANNINA' : 'FirstInstanceCourtIoannina',
    'FIRST_INSTANCE_COURT_OF_ARTA' : 'FirstInstanceCourtArta',
    'FIRST_INSTANCE_COURT_OF_PREVEZA' : 'FirstInstanceCourtPreveza',
    'FIRST_INSTANCE_COURT_OF_RODOS' : 'FirstInstanceCourtRodos',
    'FIRST_INSTANCE_COURT_OF_KOS' : 'FirstInstanceCourtKos',
    'FIRST_INSTANCE_COURT_OF_SYROS' : 'FirstInstanceCourtSyros',
    'FIRST_INSTANCE_COURT_OF_SAMOS' : 'FirstInstanceCourtSamos',
    'FIRST_INSTANCE_COURT_OF_NAXOS' : 'FirstInstanceCourtNaxos',
    'FIRST_INSTANCE_COURT_OF_CHANIA' : 'FirstInstanceCourtChania',
    'FIRST_INSTANCE_COURT_OF_RETHYMNO' : 'FirstInstanceCourtRethymno',
    'FIRST_INSTANCE_COURT_OF_KOZANI' : 'FirstInstanceCourtKozani',
    'FIRST_INSTANCE_COURT_OF_GREVENA' : 'FirstInstanceCourtGrevena',
    'FIRST_INSTANCE_COURT_OF_KASTORIA' : 'FirstInstanceCourtKastoria',
    'FIRST_INSTANCE_COURT_OF_FLORINA' : 'FirstInstanceCourtFlorina',
    'FIRST_INSTANCE_COURT_OF_LARISA': 'FirstInstanceCourtLarisa',
    'FIRST_INSTANCE_COURT_OF_VOLOS' : 'FirstInstanceCourtVolos',
    'FIRST_INSTANCE_COURT_OF_KARDITSA' : 'FirstInstanceCourtKarditsa',
    'FIRST_INSTANCE_COURT_OF_TRIKALA' : 'FirstInstanceCourtTrikala',
    'FIRST_INSTANCE_COURT_OF_NAFPLIO' : 'FirstInstanceCourtNafplio',
    'FIRST_INSTANCE_COURT_OF_CORINTH' : 'FirstInstanceCourtCorinth',
    'FIRST_INSTANCE_COURT_OF_SPARTI' : 'FirstInstanceCourtSparti',
    'FIRST_INSTANCE_COURT_OF_TRIPOLI' : 'FirstInstanceCourtTripoli',
    'FIRST_INSTANCE_COURT_OF_KALAMATA' : 'FirstInstanceCourtKalamata',
    'FIRST_INSTANCE_COURT_OF_KIPARISSIA' : 'FirstInstanceCourtKiparissia',
    'FIRST_INSTANCE_COURT_OF_GYHTEIO' : 'FirstInstanceCourtGytheio',
    'FIRST_INSTANCE_COURT_OF_PATRAS' : 'FirstInstanceCourtPatras',
    'FIRST_INSTANCE_COURT_OF_PATRAS' : 'FirstInstanceCourtAigio',
    'FIRST_INSTANCE_COURT_OF_KALAVRITA' : 'FirstInstanceCourtKalavrita',
    'FIRST_INSTANCE_COURT_OF_HLEIAS' : 'FirstInstanceCourtHleias',
    'FIRST_INSTANCE_COURT_OF_AMALIADA' : 'FirstInstanceCourtAmaliada',
    'FIRST_INSTANCE_COURT_OF_ZAKINTHOS' : 'FirstInstanceCourtZakinthos',
    'FIRST_INSTANCE_COURT_OF_KEFALLONIA' : 'FirstInstanceCourtKefallonia',
    'FIRST_INSTANCE_COURT_OF_AGRINIO' : 'FirstInstanceCourtAgrinio',
    'FIRST_INSTANCE_COURT_OF_LEFKADA' : 'FirstInstanceCourtLefkada',
    'FIRST_INSTANCE_COURT_OF_MESOLOGGI' : 'FirstInstanceCourtMesologgi',
    'FIRST_INSTANCE_COURT_OF_MITILINI' : 'FirstInstanceCourtMitilini',
    'FIRST_INSTANCE_COURT_OF_CHIOS' : 'FirstInstanceCourtChios',
    'FIRST_INSTANCE_COURT_OF_HRAKLEIO' : 'FirstInstanceCourtHrakleio',
    'FIRST_INSTANCE_COURT_OF_LASITHI' : 'FirstInstanceCourtLasithi',
    'FIRST_INSTANCE_COURT_OF_THIVA' : 'FirstInstanceCourtThiva',
    'FIRST_INSTANCE_COURT_OF_CHALKIDA' : 'FirstInstanceCourtChalkida',
    'COUNTY_COURT_OF_ATHENS' : 'CountyCourtAthens',
    'COUNTY_COURT_OF_MAROUSSI' : 'CountyCourtMaroussi',
    'COUNTY_COURT_OF_AXARNON' : 'CountyCourtAxarnon',
    'COUNTY_COURT_OF_ELEFSINA' : 'CountyCourtElefsina',
    'COUNTY_COURT_OF_KALLITHEA' : 'CountyCourtKallithea',
    'COUNTY_COURT_OF_KROPIA' : 'CountyCourtKropia',
    'COUNTY_COURT_OF_LAVRIO' : 'CountyCourtLavrio',
    'COUNTY_COURT_OF_NEAS_IONIAS' : 'CountyCourtNeasIonias',
    'COUNTY_COURT_OF_NEA_LIOSIA' : 'CountyCourtNeaLiosia',
    'COUNTY_COURT_OF_MARATHONA' : 'CountyCourtMarathona',
    'COUNTY_COURT_OF_MEGARA' : 'CountyCourtMegara',
    'COUNTY_COURT_OF_PERISTERI' : 'CountyCourtPeristeri',
    'COUNTY_COURT_OF_CHALANDRI' : 'CountyCourtChalandri',
    'COUNTY_COURT_OF_LAMIA' : 'CountyCourtLamia',    
    'COUNTY_COURT_OF_ATALANTI' : 'CountyCourtAtalanti',
    'COUNTY_COURT_OF_AMFISSA' : 'CountyCourtAmfissa',
    'COUNTY_COURT_OF_EVRITANIA' : 'CountyCourtEvritania',
    'COUNTY_COURT_OF_LIVADIA' : 'CountyCourtLivadia',
    'COUNTY_COURT_OF_AIGINA' : 'CountyCourtAigina',
    'COUNTY_COURT_OF_KALAVRIA' : 'CountyCourtKalavria',   
    'COUNTY_COURT_OF_KITHIRA' : 'CountyCourtKithira',
    'COUNTY_COURT_OF_NIKAIAS' : 'CountyCourtNikaias',
    'COUNTY_COURT_OF_SALAMINA' : 'CountyCourtSalamina',
    'COUNTY_COURT_OF_SPETSES' : 'CountyCourtSpetses',
    'COUNTY_COURT_OF_THESSALONIKI' : 'CountyCourtThessaloniki',
    'COUNTY_COURT_OF_PIRAEUS' : 'CountyCourtPiraeus',
    'COUNTY_COURT_OF_VASILIKON' : 'CountyCourtVasilikon',
    'COUNTY_COURT_OF_KOUFALION' : 'CountyCourtKoufalion',
    'COUNTY_COURT_OF_LAGKADA' : 'CountyCourtLagkada',
    'COUNTY_COURT_OF_ALEXANDRIA' : 'CountyCourtAlexandria',
    'COUNTY_COURT_OF_NAOUSA' : 'CountyCourtNaousa',
    'COUNTY_COURT_OF_EDESSA' : 'CountyCourtEdessa',
    'COUNTY_COURT_OF_ALMOPIA' : 'CountyCourtAlmopia',
    'COUNTY_COURT_OF_SKYDRA' : 'CountyCourtSkydra',
    'COUNTY_COURT_OF_PIERIA' : 'CountyCourtPieria',
    'COUNTY_COURT_OF_KOLINDROU' : 'CountyCourtKolindrou',
    'COUNTY_COURT_OF_POLIKASTRO' : 'CountyCourtPolikastro',
    'COUNTY_COURT_OF_SERRES' : 'CountyCourtSerres',
    'COUNTY_COURT_OF_NIGRITA' : 'CountyCourtNigrita',
    'COUNTY_COURT_OF_RODOLIVON' : 'CountyCourtRodolivon',
    'COUNTY_COURT_OF_SINTIKIS' : 'CountyCourtSintikis',
    'COUNTY_COURT_OF_POLIGIROU' : 'CountyCourtPoligirou',
    'COUNTY_COURT_OF_POLIGIROU' : 'CountyCourtArnaia',
    'COUNTY_COURT_OF_KASSANDRA' : 'CountyCourtKassandra',
    'COUNTY_COURT_OF_NEA_MOUDANIA' : 'CountyCourtNeaMoudania',
    'COUNTY_COURT_OF_CORFU' : 'CountyCourtCorfu',
    'COUNTY_COURT_OF_IGOUMENITSA' : 'CountyCourtIgoumenitsa',
    'COUNTY_COURT_OF_KOMOTINI' : 'CountyCourtKomotini',
    'COUNTY_COURT_OF_DRAMA' : 'CountyCourtDrama',
    'COUNTY_COURT_OF_THASOS' : 'CountyCourtThasos',
    'COUNTY_COURT_OF_PAGGAIOU' : 'CountyCourtPaggaiou',
    'COUNTY_COURT_OF_ORESTIADA' : 'CountyCourtOrestiada',
    'COUNTY_COURT_OF_ALEXANDROUPOLI' : 'CountyCourtAlexandroupoli',
    'COUNTY_COURT_OF_KAVALA' : 'CountyCourtKavala',
    'COUNTY_COURT_OF_DIDIMOTEIXO' : 'CountyCourtDidimoteixo',
    'COUNTY_COURT_OF_IOANNINA' : 'CountyCourtIoannina',
    'COUNTY_COURT_OF_KONITSA' : 'CountyCourtKonitsa',
    'COUNTY_COURT_OF_ARTA' : 'CountyCourtArta',
    'COUNTY_COURT_OF_PREVEZA' : 'CountyCourtPreveza',
    'COUNTY_COURT_OF_RODOS' : 'CountyCourtRodos',
    'COUNTY_COURT_OF_KARPATHOS' : 'CountyCourtKarpathos',
    'COUNTY_COURT_OF_KALIMNOS' : 'CountyCourtKalimnos',
    'COUNTY_COURT_OF_LEROS' : 'CountyCourtKos',
    'COUNTY_COURT_OF_LEROS' : 'CountyCourtLeros',
    'COUNTY_COURT_OF_ANDROS' : 'CountyCourtAndros',
    'COUNTY_COURT_OF_ERMOUPOLI' : 'CountyCourtErmoupoli',
    'COUNTY_COURT_OF_MILOS' : 'CountyCourtMilos',
    'COUNTY_COURT_OF_MYKONOS' : 'CountyCourtMykonos',
    'COUNTY_COURT_OF_PAROS' : 'CountyCourtParos',
    'COUNTY_COURT_OF_TINOS' : 'CountyCourtTinos',
    'COUNTY_COURT_OF_SAMOS' : 'CountyCourtSamos',
    'COUNTY_COURT_OF_IKARIA' : 'CountyCourtIkaria',
    'COUNTY_COURT_OF_KARLOVASI' : 'CountyCourtKarlovasi',
    'COUNTY_COURT_OF_NAXOS' : 'CountyCourtNaxos',
    'COUNTY_COURT_OF_CHANIA' : 'CountyCourtChania',
    'COUNTY_COURT_OF_CHANIA' : 'CountyCourtVamos',
    'COUNTY_COURT_OF_RETHYMNO' : 'CountyCourtRethymno',
    'COUNTY_COURT_OF_KOZANI' : 'CountyCourtKozani',   
    'COUNTY_COURT_OF_EORDAIA' : 'CountyCourtEordaia',
    'COUNTY_COURT_OF_GREVENA' : 'CountyCourtGrevena',
    'COUNTY_COURT_OF_KASTORIA' : 'CountyCourtKastoria',
    'COUNTY_COURT_OF_FLORINA' : 'CountyCourtFlorina',
    'COUNTY_COURT_OF_AMUNTAIO' : 'CountyCourtAmuntaio',
    'COUNTY_COURT_OF_LARISA' : 'CountyCourtLarisa',
    'COUNTY_COURT_OF_ELASSONAS' : 'CountyCourtElassona',
    'COUNTY_COURT_OF_FARSALA' : 'CountyCourtFarsala',
    'COUNTY_COURT_OF_VOLOS' : 'CountyCourtVolos',
    'COUNTY_COURT_OF_ALMIROS' : 'CountyCourtAlmiros',
    'COUNTY_COURT_OF_SKOPELOS' : 'CountyCourtSkopelos',
    'COUNTY_COURT_OF_KARDITSA' : 'CountyCourtKarditsa',
    'COUNTY_COURT_OF_TRIKALA' : 'CountyCourtTrikala',
    'COUNTY_COURT_OF_KALAMPAKA' : 'CountyCourtKalampaka',
    'COUNTY_COURT_OF_NAFPLIO' : 'CountyCourtNafplio',
    'COUNTY_COURT_OF_ASTROS' : 'CountyCourtAstros',
    'COUNTY_COURT_OF_ARGOS' : 'CountyCourtArgos',
    'COUNTY_COURT_OF_MASSITOS' : 'CountyCourtMassitos',
    'COUNTY_COURT_OF_MASSITOS' : 'CountyCourtThira',
    'COUNTY_COURT_OF_CORINTH' : 'CountyCourtCorinth',
    'COUNTY_COURT_OF_SIKIONOS' : 'CountyCourtSikionos',
    'COUNTY_COURT_OF_NEMEA' : 'CountyCourtNemea',
    'COUNTY_COURT_OF_XYLOKASTRO' : 'CountyCourtXylokastro',
    'COUNTY_COURT_OF_SPARTI': 'CountyCourtSparti',
    'COUNTY_COURT_OF_EPIDAVROS_LIMIRAS' : 'CountyCourtEpidavrosLimiras',
    'COUNTY_COURT_OF_TRIPOLI' : 'CountyCourtTripoli',
    'COUNTY_COURT_OF_MEGALOPOLI' : 'CountyCourtMegalopoli',
    'COUNTY_COURT_OF_PSOFIDA' : 'CountyCourtPsofida',
    'COUNTY_COURT_OF_KALAMATA' : 'CountyCourtKalamata',
    'COUNTY_COURT_OF_PILOS' : 'CountyCourtPilos',
    'COUNTY_COURT_OF_KIPARISSIA' : 'CountyCourtKiparissia',
    'COUNTY_COURT_OF_PLATAMODA' : 'CountyCourtPlatamoda',
    'COUNTY_COURT_OF_GYTHEIO' : 'CountyCourtGytheio',
    'COUNTY_COURT_OF_NEAPOLI_VOIWN' : 'CountyCourtNeapoliVoiwn',
    'COUNTY_COURT_OF_PATRAS' : 'CountyCourtPatras',
    'COUNTY_COURT_OF_DIMI' : 'CountyCourtDimi',
    'COUNTY_COURT_OF_AIGIALIA' : 'CountyCourtAigialia',
    'COUNTY_COURT_OF_AIGIALIA' : 'CountyCourtKalavrita',
    'COUNTY_COURT_OF_AKRATA' : 'CountyCourtAkrata',
    'COUNTY_COURT_OF_PIRGOS' : 'CountyCourtPirgos',
    'COUNTY_COURT_OF_OLYMPIA' : 'CountyCourtOlympia',
    'COUNTY_COURT_OF_ARINI' : 'CountyCourtArini',
    'COUNTY_COURT_OF_AMALIADA' : 'CountyCourtAmaliada',
    'COUNTY_COURT_OF_GASTOUNI' : 'CountyCourtGastouni',
    'COUNTY_COURT_OF_MYRTOUNTION' : 'CountyCourtMyrtountion',
    'COUNTY_COURT_OF_ZAKINTHOS' : 'CountyCourtZakinthos',
    'COUNTY_COURT_OF_ARGOSTOLI' : 'CountyCourtArgostoli',
    'COUNTY_COURT_OF_SAMEON' : 'CountyCourtSameon',
    'COUNTY_COURT_OF_AGRINIO' : 'CountyCourtAgrinio',
    'COUNTY_COURT_OF_VALTOS' : 'CountyCourtValtos',
    'COUNTY_COURT_OF_LEFKADA' : 'CountyCourtLefkada',
    'COUNTY_COURT_OF_VONITSA' : 'CountyCourtVonitsa',
    'COUNTY_COURT_OF_MESOLOGGI' : 'CountyCourtMesologgi',
    'COUNTY_COURT_OF_NAFPAKTOS' : 'CountyCourtNafpaktos',
    'COUNTY_COURT_OF_MITILINI' : 'CountyCourtMitilini',
    'COUNTY_COURT_OF_KALLONI' : 'CountyCourtKalloni',
    'COUNTY_COURT_OF_CHIOS' : 'CountyCourtChios',
    'COUNTY_COURT_OF_HRAKLEIO' : 'CountyCourtHrakleio',
    'COUNTY_COURT_OF_KASTELI' : 'CountyCourtKasteli',
    'COUNTY_COURT_OF_LASITHI' : 'CountyCourtLasithi',
    'COUNTY_COURT_OF_IERAPETRA' : 'CountyCourtIerapetra',
    'COUNTY_COURT_OF_SITEIA' : 'CountyCourtSiteia',
    'COUNTY_COURT_OF_THIVA' : 'CountyCourtThiva',
    'COUNTY_COURT_OF_CHALKIDA' : 'CountyCourtChalkida',
    'COUNTY_COURT_OF_ISTIAIA' : 'CountyCourtIstiaia',
    'COUNTY_COURT_OF_KARYSTOS' : 'CountyCourtKarystos',
    'COUNTY_COURT_OF_KIMI' : 'CountyCourtKimi',
    'COUNTY_COURT_OF_TAMINEON' : 'CountyCourtTamineon',
    'DISTRICT_COURT_OF_ATHENS' : 'DistrictCourtAthens',
    'DISTRICT_COURT_OF_LAMIA' : 'DistrictCourtLamia',
    'DISTRICT_COURT_OF_LIVADIA' : 'DistrictCourtLivadia',
    'DISTRICT_COURT_OF_PIRAEUS' : 'DistrictCourtPiraeus',
    'DISTRICT_COURT_OF_THESSALONIKI' : 'DistrictCourtThessaloniki',
    'DISTRICT_COURT_OF_VEROIA' : 'DistrictCourtVeroia',
    'DISTRICT_COURT_OF_PIERIA' : 'DistrictCourtPieria',
    'DISTRICT_COURT_OF_SERRES' : 'DistrictCourtSerres',
    'DISTRICT_COURT_OF_CORFU' : 'DistrictCourtCorfu',
    'DISTRICT_COURT_OF_KOMOTINI' : 'DistrictCourtKomotini',
    'DISTRICT_COURT_OF_DRAMA' : 'DistrictCourtDrama',
    'DISTRICT_COURT_OF_KAVALA' : 'DistrictCourtKavala',
    'DISTRICT_COURT_OF_ARTA' : 'DistrictCourtArta',
    'DISTRICT_COURT_OF_RODOS' : 'DistrictCourtRodos',
    'DISTRICT_COURT_OF_CHANIA' : 'DistrictCourtChania',
    'DISTRICT_COURT_OF_RETHYMNO' : 'DistrictCourtRethymno',
    'DISTRICT_COURT_OF_KOZANI' : 'DistrictCourtKozani',
    'DISTRICT_COURT_OF_KLEISOURA' : 'DistrictCourtKleisoura',
    'DISTRICT_COURT_OF_LARISA' : 'DistrictCourtLarisa',
    'DISTRICT_COURT_OF_ELASSONAS' : 'DistrictCourtElassona',
    'DISTRICT_COURT_OF_VOLOS' : 'DistrictCourtVolos',
    'DISTRICT_COURT_OF_KARDITSA' : 'DistrictCourtKarditsa',
    'DISTRICT_COURT_OF_TRIKALA' : 'DistrictCourtTrikala',
    'DISTRICT_COURT_OF_NAFPLIO' : 'DistrictCourtNafplio',
    'DISTRICT_COURT_OF_NAFPLIO' : 'DistrictCourtArgos',
    'DISTRICT_COURT_OF_CORINTH' : 'DistrictCourtCorinth',
    'DISTRICT_COURT_OF_SIKIONOS' : 'DistrictCourtSikionos',
    'DISTRICT_COURT_OF_SPARTI' : 'DistrictCourtSparti',
    'DISTRICT_COURT_OF_TRIPOLI' : 'DistrictCourtTripoli',
    'DISTRICT_COURT_OF_KALAMATA' : 'DistrictCourtKalamata',
    'DISTRICT_COURT_OF_PATRAS' : 'DistrictCourtPatras',
    'DISTRICT_COURT_OF_AIGIALIA' : 'DistrictCourtAigialia',
    'DISTRICT_COURT_OF_PIRGOS' : 'DistrictCourtPirgos',
    'DISTRICT_COURT_OF_AMALIADA' : 'DistrictCourtAmaliada',
    'DISTRICT_COURT_OF_AGRINIO' : 'DistrictCourtAgrinio',
    'DISTRICT_COURT_OF_VALTOS' : 'DistrictCourtValtos',
    'DISTRICT_COURT_OF_MESOLOGGI' : 'DistrictCourtMesologgi',
    'DISTRICT_COURT_OF_MITILINI' : 'DistrictCourtMitilini',
    'DISTRICT_COURT_OF_LIMNOS' : 'DistrictCourtLimnos',
    'DISTRICT_COURT_OF_PLOMARI' : 'DistrictCourtPlomari',
    'DISTRICT_COURT_OF_HRAKLEIO' : 'DistrictCourtHrakleio',
    'DISTRICT_COURT_OF_MOIRES' : 'DistrictCourtMoires',
    'DISTRICT_COURT_OF_PIRGOS_KRITIS' : 'DistrictCourtPirgosCrete',
    'DISTRICT_COURT_OF_THIVA' : 'DistrictCourtThiva',
    'DISTRICT_COURT_OF_CHALKIDA' : 'DistrictCourtChalkida',
    }


"""A dictionary used to convert any greek character to the corresponding
latin according to qwerty keyboard."""
grToLat = {
    'Α':'A', 'α':'a', 'ά':'a', 'Β':'B', 'β':'b',
    'Γ':'G', 'γ':'g', 'Δ':'D', 'δ':'d', 'Ε':'E',
    'έ':'e', 'ε':'e', 'Ζ':'Z', 'ζ':'z', 'Η':'H',
    'η':'h', 'ή':'h', 'Θ':'U', 'θ':'u', 'Ι':'I',
    'ι':'i', 'ί':'i', 'Κ':'K', 'κ':'k', 'Λ':'L',
    'λ':'l', 'Μ':'M', 'μ':'m', 'Ν':'N', 'ν':'n',
    'Ξ':'J', 'ξ':'j', 'Ο':'O', 'ο':'o', 'ό':'o',
    'Π':'P', 'π':'p', 'Ρ':'R', 'ρ':'r', 'Σ':'S',
    'ς':'s', 'σ':'s', 'Τ':'T', 'τ':'t', 'Υ':'Y',
    'ύ':'y', 'υ':'y', 'Φ':'F', 'φ':'f', 'Χ':'X',
    'χ':'x', 'Ψ':'C', 'ψ':'c', 'ω':'v', 'ώ':'v',
    'Ω':'V'
    }


"""A dictionary used to convert any greek character to the corresponding
latin one with minor changes"""
grToLat_v2 = {
    'Α':'A', 'α':'a', 'ά':'a', 'Β':'B', 'β':'b',
    'Γ':'G', 'γ':'g', 'Δ':'D', 'δ':'d', 'Ε':'E',
    'έ':'e', 'ε':'e', 'Ζ':'Z', 'ζ':'z', 'Η':'H',
    'η':'i', 'ή':'i', 'Θ':'Th', 'θ':'th', 'Ι':'I',
    'ι':'i', 'ί':'i', 'Κ':'K', 'κ':'k', 'Λ':'L',
    'λ':'l', 'Μ':'M', 'μ':'m', 'Ν':'N', 'ν':'n',
    'Ξ':'KS', 'ξ':'ks', 'Ο':'O', 'ο':'o', 'ό':'o',
    'Π':'P', 'π':'p', 'Ρ':'R', 'ρ':'r', 'Σ':'S',
    'ς':'s', 'σ':'s', 'Τ':'T', 'τ':'t', 'Υ':'Y',
    'ύ':'y', 'υ':'y', 'Φ':'F', 'φ':'f', 'Χ':'X',
    'χ':'x', 'Ψ':'PS', 'ψ':'ps', 'ω':'w', 'ώ':'w',
    'Ω':'W'
    }


"""A dictionary to convert any style of element indexing to the appropriate
number according to Akoma Ntoso naming convention (used when authors provide
combinationf of numbers and letters or words for element indexing)"""
numberingSystem = {
    'α' : '1', 'Α' : '1', 'β' : '2', 'Β' : '2', 'γ' : '3', 'Γ' : '3', 'Α':'1',
    'δ' : '4', 'Δ' : '4', 'ε' : '5', 'Ε' : '5', 'στ' : '6', 'ΣΤ' : '6',
    'ζ' : '7', 'Ζ' : '7', 'η' : '8', 'Η' : '8', 'θ' : '9', 'Θ' : '9',
    'ι' : '10', 'Ι' : '10', 'ια' : '11', 'IA' : '11', 'ιβ' : '12', 'ΙΒ' : '12',
    'ιγ' : '13', 'ΙΓ' : '13', 'ιδ' : '14', 'ΙΔ' : '14', 'ιε' : '15', 'ΙΕ' : '15',
    'ιστ' : '16', 'ΙΣΤ' : '16', 'ιζ' : '17', 'ΙΖ' : '17', 'ιη' : '18', 'ΙΗ' : '18',
    'ιθ' : '19',  'ΙΘ' : '19', 'κ' : '20', 'Κ' : '20', 'κα' : '21', 'ΚΑ' : '21',
    'πρώτος' : '1', 'πρώτου' : '1', 'πρώτης' : '1', 'πρώτη' : '1', 'μόνο' : '1', 'ΜΟΝΟ' : '1',
    'πρώτο' : '1', 'μόνου': '1',
    'δεύτερος' : '2', 'δεύτερο' : '2', 'δεύτερου' : '2', 'δεύτερης' : '2', 'δεύτερη' : '2',
    'τρίτο' : '3', 'τρίτου' : '3', 'τρίτη' : '3', 'τρίτης' : '3',
    'τέταρτο' : '4', 'τέταρτου' : '4', 'τέταρτη' : '4', 'τέταρτης' : '4',
    'πέμπτο' : '5', 'πέμπτης' : '5', 'πέμπτου' : '5', 'πέμπτη' : '5',
    'έκτο' : '6', 'έκτου' : '6', 'έκτη' : '6', 'έκτης' : '6'
    }


"""Roles that can be found in legal judgments"""
roles = {
    'Αντιπροέδρους': 'deputy.president',
    'Αντιπρόεδρο': 'deputy.president',
    'Αντεισαγγελέας': 'deputy.prosecutor',
    'Αντεισαγγελέα': 'deputy.prosecutor',
    'Αντεισαγγελέως': 'deputy.prosecutor',
    'Αρεοπαγίτες': 'supreme.judge',
    'Αρεοπαγίτης': 'supreme.judge',
    'Αναιρεσείων': 'appellant',
    'αναιρεσείων': 'appellant',
    'αναιρεσειόντων': 'appellant',
    'αναιρεσείοντα': 'appellant',
    'αναιρεσείουσας': 'appellant',
    'αναιρεσειουσών': 'appellant',
    'αναιρεσείοντος': 'appellant',
    'αναιρεσείουσες': 'appellant', 
    'αναιρεσιβλήτων': 'defendant',
    'αναιρεσιβλήτου': 'defendant',
    'Γραμματέα': 'secretary',
    'Γραμματέας': 'secretary',
    'Γραμματείς': 'secretary',
    'Γραμματέως': 'secretary',
    'γραμματέως': 'secretary',
    'γραμματέας': 'secretary',
    'Δικαστές': 'judge',
    'Δικαστών': 'judge',
    'δικαστών': 'judge',
    'δικηγόρο': 'lawyer',
    'δικηγόρους': 'lawyer',
    'δικηγόρος': 'lawyer',
    'Διευθυντές': 'director',
    'Εισηγητής': 'rapporteur',
    'Εισηγητή': 'rapporteur',
    'Εισηγήτρια': 'rapporteur',
    'Εισαγγελέα': 'prosecutor',
    'Εισαγγελέας': 'prosecutor',
    'Εισαγγελεύς': 'prosecutor',
    'Εφεσίβλητος': 'respondent',
    'εφεσιβλήτου': 'respondent',
    'εφεσιβλήτων': 'respondent',
    'Μέλος': 'member',
    'Μέλη': 'member',
    'Πρόεδρος': 'president',
    'Πρόεδρο': 'president',
    'Προέδρου': 'president',
    'Προεδρεύων': 'president',
    'Προεδρεύοντα': 'president',
    'Πάρεδρο': 'associate.judge',
    'Πάρεδροι': 'associate.judge',
    'Πάρεδρος': 'associate.judge',
    'Προϊσταμένου': 'chief',
    'Προϊστάμενος': 'chief',
    'Σύμβουλοι': 'privy.councillor',
    'Σύμβουλος': 'privy.councillor',
    'Σύμβουλο': 'privy.councillor',
    'Συμβούλου': 'privy.councillor',
    }


"""A dictionary that converts a month phrase to the corresponding number"""
months = {
    'Ιανουαρίου' : 1,
    'Iανουαρίου' : 1,   #English character 'I'
    'Ιαναουαρίου' : 1, 
    'Φεβρουαρίου' : 2,
    'Μαρτίου' : 3,
    'Απριλίου' : 4,
    'Μαΐου' : 5,
    'Μαϊου' : 5,
    'Μαίου' : 5,
    'Ιουνίου' : 6,
    'Iουνίου' : 6,  #English character 'I'
    'Ιουλίου' : 7,
    'Αυγούστου' : 8,
    'Σεπτεμβρίου' : 9,
    'Οκτωβρίου' : 10,
    'Νοεμβρίου' : 11,
    'Δεκεμβρίου' : 12,
    '1' : 1, '01' : 1, '2' : 2, '02' : 2, '3' : 3,  '03' : 3,
    '4': 4, '04': 4, '5' : 5, '05' : 5, '6' : 6, '06' : 6,
    '7' : 7, '07' : 7, '8' : 8, '08' : 8, '9' : 9, '09' : 9,
    '10' : 10, '11' : 11, '12' : 12
    }


"""This dictionary is used only to create 'ShowAs' attribute of
TLCEvent element based on the name of the corresponding date"""
importantDates = {
    'publicHearingDate': 'Ημερομηνία δημόσιας συνεδρίασης',
    'decisionPublicationDate': 'Ημερομηνία δημοσίευσης απόφασης',
    'courtConferenceDate': 'Ημερομηνία διάσκεψης',
    'councilConferenceDate' : 'Ημερομηνία συνεδρίασης',
    'opinionSignatureDate' : 'Ημερομηνία θεώρησης γνωμοδότησης'
    }


"""Lists of rules for removing garbages for every type of legal text"""
ClarityGarbages=[
    (r'\n\s*ΑΝΑΡΤΗΤΕ[ΑΟ]\s*ΣΤΟ\s*ΔΙΑΔΙΚΤΥΟ\n', '\n'),
    (r'(\n+\s*ΑΔΑ\s*[:]\s*[Α-Ω0-9-]*\n*)', '\n'), #ADA
    (r'(ΑΔΑ\s*[:]\s*[__]+\n*)', '\n'), #ADA
    (r'\n+(\s*[-]*\d+[-]*\s*)\n+', '\n\n'), #paging
    (r'', ''), #another type of paging 762Ω6-ΓΟΑ
    (r'\n(\s*[………]+\s*)\n', '\n\n'),
    (r'\n(\s*[***]+\s*)\n', '\n\n'),
    (r'\s*(Σελίδα|Σελ[.])\s*\d*\s*από\s*\d*\s*', '\n\n'), #paging
    (r'\n(΄){1,2}', '\n'), #ΝΣΚ 4ΧΔ6ΟΡΡΕ-8ΞΘ
    (r'\n\s*[.][/]+[.]\n', '\n'),
    (r'(\d+)\|(\d+)\|(\d+)', r'\1/\2/\3'), #correction of decision using '|' character
    (r'(\d+)\|(\d+)', r'\1/\2'), #correction of decision using '|' character
    (r'(\d+)\\(\d+)', r'\1/\2'), #correction of decision using '\' character
    (r'\n\s+\n','\n\n'), #lines with whitespaces only
    (r'Σελίδα\s*\d+\s*από\s*\d+.*?(\n*ΑΔΑ\s*[:]\s*[Α-Ω0-9-]*\n*)', '\n'), #check Β4ΜΨ46ΨΧΞΧ-ΔΘΛ
    (r'(\n)\s*[==]+(\n)', r'\1\2'), #check Ω168ΟΡΡΕ-Δ61
    ('\n([0-9a-zA-Zα-ωΑ-Ωάέίόύώ\s\d()\'.-:\\]+[.](docx|DOCX|DOC|doc))', '\n'),#check 6ΔΨΝ465ΦΘΘ-ΗΚ2
    (r'\n((\s\S+)+[.](docx|DOCX|DOC|doc))\n', '\n'),
    (r'(\n)\n+', r'\1\n')
    ]

SteGarbages=[
    (r'\n([?]+)', '\n'),
    (r'(\d+[/])[ ]+(\d+)', r'\1\2'),    # space correction in ids 1223/ 2019 -> 122/2019
    (r'\n([.][/][.])', '\n'),
    (r'\n[@]+\n', '\n'),    #A86_1996
    (r'\n([-]+|[** ]+)(?=\n)', '\n'),
    (r'Αριθμός\s\d+[/]\d+\s[-]\d{1,2}[-]\s*', r''), #page numbering
    (r'\n[-]\s*\d+\s*[-]\n', ''),
    (r'^\s+\n(\S+)', r'\1'),     #empty text at the beginning of judgment
    (r'(\n)\s*\n+', r'\1'),  #multiple empty lines
    (r'\n\d+(\n)', r'\1'),      #page numbering as standalone number
    (r'(\d+)\|(\d+)\|(\d+)', r'\1/\2/\3'), #correction of decision using '|' character
    (r'(\d+)\|(\d+)', r'\1/\2'), #correction of decision using '|' character
    (r'(\d+)\\(\d+)', r'\1/\2'), #correction of decision using '\' character
    (r'Αριθμός\s*\d+[/]\d+$', r''),     #judgment number at the end of the document
    (r'\s+$', ''),   # empty lines before end of document
    (r'\n\d+$', r''),      #page numbering at the end of the document
    (r'(\n)\s+(\S+)', r'\1\2'),
    (r'\n[_]+\n', '\n')
    ]

AreiosPagosGarbages=[
    (r'(ΓΙΑ ΤΟΥΣ ΛΟΓΟΥΣ ΑΥΤΟΥΣ)\s(.*?\n)', r'\1\n\2'),  #check Areios pagos 1593/2007
    (r'^(.*?)(Αριθμός|ΑΡΙΘΜΟΣ)(\s\d+[/]\d+)', r'\2\3'), #abstract at the beginning of court decision 
    (r'^\s\n(\S+)', r'\1'),     #empty text at the beginning of judgment
    (r'(\d+)\|(\d+)\|(\d+)', r'\1/\2/\3'), #correction of decision using '|' character
    (r'(\d+)\|(\d+)', r'\1/\2'), #correction of decision using '|' character
    (r'(\d+)\\(\d+)', r'\1/\2'), #correction of decision using '\' character
    (r'(\d+[/])[ ]+(\d+)', r'\1\2'),    # space correction in ids 1223/ 2019 -> 122/2019
    (r'(\n|^)[ ]{1,2}(\S+)', r'\1\2'),  # double space in empty lines
    (r'(\n)\s*\n+', r'\1'),     # multiple empty lines
    (r'\s+$', '')   # empty lines before end of document
    ]

#Check dehyphenation for words   
FekGarbages=[
    (r'Signature\s*Not(.*?)Typografio', '\n'),
    (r'\n+\s*\d+\n+','\n'), #pdf page numberin
    (r'\n\d+[-]*\d*\n', '\n'),
    (r'\n[F]\n', '\n'),
    (r'Αρ[.]\s*Φύλλου\s*\d+\n', '\n'),
    (r'\s*ΕΦΗΜΕΡΙ∆Α\s*TΗΣ\s*ΚΥΒΕΡΝΗΣΕΩΣ\n', '\n'),
    (r'^(\d+|\S{1}|s*)\n', ''), #page numbering 1 -> invalid character at the start of text
    (r'[*]\d+[*]\n','\n'),
    (r'\n[-]\d+[-]\n', '\n'),
    (r'Digitally signed by.*?(Verified|Athens\n)','\n'), #digital signed
    (r'\n*Τεύχος\s*Α’\s\d+/(\d+[.]*)+', '\n'),
    (r'\d*\s*(ΕΦΗΜΕΡΙΣ|ΕΦΗΜΕΡΙ∆Α)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ\s\(ΤΕΥΧΟΣ\s+(ΠΡΩΤΟ|ΔΕΥΤΕΡΟ)\)\s*\d*\n', '\n'),
    (r'(ΕΦΗΜΕΡΙΣ|ΕΦΗΜΕΡΙ∆Α)\s*ΤΗΣ\s*ΚΥΒΕΡΝΗΣΕΩΣ\s*(ΤΗΣ\s*ΕΛΛΗΝΙΚΗΣ\s* ΔΗΜΟΚΡΑΤΙΑΣ)', '\n'),
    (r'\s*Την\s*ευθύνη\s*για\s*την\s*εκτύπωση.*$', '\n'),
    (r'\n*Σε\s*έντυπη\s*μορφή[:]\n.*$', '\n'),
    (r'Φ.Ε.Κ. \d+ ', r''),
    (r'º','Ι'),
    (r'(\d+)\|(\d+)', r'\1/\2'), #correction of decision using '|' character
    (r'(\d+)\\(\d+)', r'\1/\2'), #correction of decision using '\' character
    (r'\n*(ΑΠΟ\s*ΤΟ\s*){0,1}ΕΘΝΙΚΟ\s*ΤΥΠΟ\s*ΓΡΑΦΕΙΟ\n.*$', '\n'),
    (r'\n\d+[-]{1}\d*\n', '\n'),
    (r'\n+', '\n'),
    (r'^\s*', ''),
    (r'\n\s*$', '')
    ]

nskGarbages = [
    (r'(\n)\s+(\S+)', r'\1\2'), #empty lines
    (r'(\S)([ ]){2,}(\S)', r'\1\2\3'), #Large space between words
    (r'(\n)\s*\[*\d+\]*\s*(ΓΝΩΜ. 5086[*]*)?\n', r'\1'), #Page numbering
    (r'\n\s*\d+\s*ΕΙΣΗΓ[.]\s*\d+[*]*\n', r'\n'),
    (r'(\n)\s*[-]+\s*\n', r'\1'), # special case of "---------" in text
    (r'\n(……………………………….)\n', r'\n'),
    (r'\n(……………………………….…………)\n', r'\n'),
    (r'\n(……………………..*………………………)\n', r'\n'),
    (r'\n(…)+([.]?)\n', r'\n'),
    (r'\n(--------------------------------------------------//---------------------------------------------------)\n', r'\n'),
    (r'\n(---*---)\n', r'\n'),
    (r'\n\d+\s*\n', r'\n'), #Page numbering alternative
    (r'\n(Σελίδα\s*[|]\s*\d+)\n',r'\n'),
    (r'(\d+[-]\d+[-])\n(\d+[.])\s?', r'\1\2\n'),
    (r'\n[:]\s*\d+[-]\d*\s*', r'\n'),
    (r'\n([:]\s*[-]\d+)\n', r'\n'),
    (r'\n(ι)\n', r'\n'),
    (r'(\d+)\|(\d+)', r'\1/\2'), #correction of decision using '|' character
    (r'(\d+)\\(\d+)', r'\1/\2'), #correction of decision using '\' character
    (r'\n(Φ[.]\s*[Εε]ρωτ[.]\s*\d+[/]\d+)\s*', r'\n'),
    (r'\n(Σύ\s*β\s*λ)$', r''),
    (r'\n[-]\s*\d+\s*[-]\n', r'\n'),
    (r'\n([-][/]*[-])\n', r'\n'),
    (r'[.]\s[*]+\n', r''),
    (r'(\d+[/])[ ]+(\d+)', r'\1\2'),    # space correction in ids 1223/ 2019 -> 122/2019
    (r'\n\s*ΠΕΡΙΛΗΨΗ\s*ΓΝΩΜΟΔΟΤΗΣΕΩΣ.*?$', r''), #abstract in the end of legal opinion
    (r'\n(Αθήνα\s*\d{2}[-]\s{0,2}[-]\d{4})(\S+)', r'\n\1\n\2'),
    #(r'\n(Α|Β|Γ|Δ|Ε)([.])\s*(\d{1,2}[.])', r'\n\1\2 \n\3'),
    (r'\n(ΙΙ[.]\s*)(Α)΄(Στο)', r'\n\1\2. \3'),
    (r'\n(Ι|ΙΙ|II|ΙΙΙ|ΙV)([.])\s*(Α[.])', r'\n\1\2\n\3'),
    (r'\n(Ι|ΙΙ|II|ΙΙΙ|ΙV)([.])\s*(α[.])', r'\n\1\2\n\3'),
    (r'\n(Ι|ΙΙ|ΙΙΙ|IV|V)([.])\s*(1[.])', r'\n\1\2\n\3'),
    (r'\n(\d{1,2})([.])([Α-Ω]+)', r'\n\1\2 \3'),
    (r'\n(Ι|ΙΙ|ΙΙΙ|ΙV)([.])\s*(Α[.])', r'\n\1\2\n\3'),
    #(r'(Ι|II|ΙΙΙ|ΙV|V|VΙ)([.])(\s*)((Α|Β|Γ|Δ)[.])', r'\1\2\n\4'),
    (r'\nΑΝΑΡΤΗΣΗ ΣΤΟ ΠΡΟΓΡΑΜΜΑ ΔΙΑΥΓΕΙΑ\n', r'\n'),
    (r'\nΑΝΑΡΤΗΤΕΑ ΣΤΟ ΔΙΑΔΙΚΤΥΟ\n', r'\n'),
    (r'(ΘΕΩΡΗΘΗΚΕ\n)(.*?)\n(ΝΟΜΙΚΟ\sΣΥΜΒΟΥΛΙΟ\sΤΟΥ\sΚΡΑΤΟΥΣ.*?$)', r'\1\2'),
    (r'(\n)\s*$', r'') #EOF empty next line
    ]


"""basic patterns for matching important dates in legal texts"""
# publicHearingDate
publicHearingDatePattern = r'(?P<dd>\d{1,2})(?P<numSpecialLektiko>(ας|ης|η|ής)*)(?P<keno_1>\s*[.]*)(?P<mm>Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Μαϊου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου|\d{1,2})(?P<keno_2>\s*[.]*)(?P<yyyy>\d{4})'
# decisionPublicationDate
decisionPublicationDatePattern = r'(?P<string>Δημοσιεύθηκε|Εκδόθηκε|δημοσιεύθηκε|δημοσιεύτηκε|δημόσια\sσυνεδρίαση)(?P<garbage>.*?)(?P<dd>\d{1,2})(?P<numSpecialLektiko>(ας|ης|η|ής)*)(?P<keno_1>\s*[.]*)(?P<mm>Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Μαϊου|Μαίου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου|\d{1,2})(?P<keno_2>\s*[.]*)(?P<yyyy>\d{4})'
# courtConferenceDate
courtConferenceDatePattern = r'(?P<string>αποφασίστηκε|αποφασίσθηκε|διάσκεψη\s*έγινε)(?P<garbage>.*?)(?P<dd>\d{1,2})(?P<numSpecialLektiko>(ας|ης|η|ής)*)(?P<keno_1>\s*[.]*)(?P<mm>Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Μαϊου|Μαίου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου|\d{1,2})(?P<keno_2>\s*[.]*)(?P<yyyy>\d{4})'
# councilConferenceDate
councilConferenceDatePattern = r'(?P<string>Συνεδρίαση)(?P<garbage>.*?)(?P<dd>\d{1,2})(?P<numSpecialLektiko>(ας|ης|η|ής)*)(?P<keno_1>\s*[.]*\s*)(?P<mm>[ΙI]ανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Μαϊου|Μαίου|[IΙ]ουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου|\d{1,2})(?P<keno_2>\s*[.]*\s*)(?P<yyyy>\d{4})'
# opinionSignatureDate
opinionSignatureDatePattern = r'(?P<string>Θεωρήθηκε\s*|Αθήνα[,]?\s*)(?P<garbage>.*?)(?P<dd>\d{1,2})(?P<numSpecialLektiko>(ας|ης|η|ής)*)(?P<keno_1>\s*[.]*[-]*\s*)(?P<mm>Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Μαϊου|Μαίου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου|\d{1,2})(?P<keno_2>\s*[.]*[-]*\s*)(?P<yyyy>\d{4})'
# paragraph pattern
paragraphPattern = r'([<][/]p[>][<]p[>])'
