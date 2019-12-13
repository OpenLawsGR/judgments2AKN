grammar Legal_ref;

all_text : legal_text EOF;

legal_text : (legal_reference|other_text)+;

other_text : (
     .
);

legal_reference :
    courtDecision |
    legislation |
    //administrativeDoc |
    legalOpinion |
    euLegislation //|
    //incompleteUnknown
    ;

/*
incompleteUnknown :
    ((special|lektiko_id) SPACE)+ (decision | praksi) |
    (decision SPACE special) |
    (YP_ARITHM SPACE)? (btrimeles SPACE)? ids SPACE decision |
    implicitKwdikas |
    implicitLegalType |
    explicitLegalElement SPACE (OF SPACE)? decision SPACE special |
    explicitArthro_1 SPACE sxetiko SPACE AND SPACE arthro_id SPACE sxetiko|
    (explicitLegalElement|explicitArthro_1) ~(SLASH|DOT)   //Μήπως θελει σπάσιμο για τις παραγρ που έχουν λεκτικό αριθμό (κανει conflict με τα πινάκια)
        (SPACE? (OF SPACE)? ((explicitLegalElement|explicitArthro_1) ~(SLASH|DOT) | implicitLegalElement))*
        (SPACE? sxetiko | SPACE? implicitKwdikas | SPACE? (OF SPACE)? special)? |
    implicitLegalElement |

    // (Politikh_Ypouesh_Olomeleias_Areioy_Pagoy__Ar_14_2004,_18_3_2004)
    arthro_id SPACE (OF SPACE)? explicitKwdikas |

    ids SPACE praksi |
    sxetiko
    ;
*/
//--------------------------EU LEGISLATION ----------------------//
euLegislation :
    singleEULegislation
    ;

singleEULegislation :
    completeEULegislation
    ;

completeEULegislation:
    explicitLegalElement
        (SPACE? ((OF|COMMA) SPACE)? explicitLegalElement)*
        SPACE (OF SPACE)? (eu_regulation | eu_directive) SPACE ids|
    ((eu_regulation | eu_directive) SPACE) ids (SLASH (eu_regulation|eok))? (SPACE OF SPACE EE_COUNCIL)? |
    eu_regulation SPACE PAR_TEXT SPACE ids |
    eu_directive SPACE 'ης' SPACE ids (SLASH (eu_regulation|eok))
    ;

eu_regulation : EU_REGULATION;
eu_directive : EU_DIRECTIVE;
eu : EU_TEXT;
//eu_id : NUM ((DOT|HYPHEN|COMMA) SPACE? NUM)? (SLASH SPACE? NUM ((DOT|HYPHEN) NUM)*)+ (SLASH EU_REGULATION)?;
eok : EOK;
EOK: 'ΕΟΚ' | 'ΕΚ';
EE_COUNCIL : 'Συμβουλίου' SPACE OF SPACE 'ΕΕ';

//------------------------GNOMODOTISEIS------------------------------//
legalOpinion :
    singleLegalOpinion
    ;

singleLegalOpinion :
    completeLegalOpinion
    ;

completeLegalOpinion :
    nsk SPACE? ids ((COMMA SPACE | SPACE AND SPACE) ids)* |
    ids SPACE LEGAL_OPINION_TEXT SPACE nsk |
    nsk SPACE YP_ARITHM SPACE ids COMMA SPACE ids |
    nsk SPACE WITH SPACE LEGAL_OPINION_TEXT SPACE ids |
    LEGAL_OPINION_TEXT SPACE ids SPACE nsk |
    LEGAL_OPINION_TEXT SPACE nsk SPACE ids COMMA SPACE ids |
    nsk COMMA SPACE WITH SPACE ids SPACE LEGAL_OPINION_TEXT |
    YP_ARITHM SPACE ids SPACE LEGAL_OPINION_TEXT |
    LEGAL_OPINION_TEXT SPACE ids ((COMMA SPACE | SPACE AND SPACE) ids)* |
    LEGAL_OPINION_TEXT SPACE YP_ARITHM SPACE ids SPACE nsk |
    nsk SPACE YP_ARITHM SPACE ids |
    LEGAL_OPINION_TEXT SPACE nsk SPACE YP_ARITHM SPACE ids ((COMMA SPACE | SPACE AND SPACE) ids)*

    ;

nsk : NSK;

//-----------------------EGGRAFA------------------------------------//
/*administrativeDoc :
    singleAdministrativeDoc
    ;

singleAdministrativeDoc :
    completeAdministrativeDoc |
    incompleteAdministrativeDoc
    ;

completeAdministrativeDoc :
    YP_ARITHM SPACE ids SPACE decision SPACE foreas|
    egkyklios_id_complete |
    egkyklios SPACE YP_ARITHM SPACE ids SPACE foreas |
    ids SPACE (egkyklios|decision) SPACE foreas |
    PAD SPACE egkyklios_id_complete|
    egkyklios_id_incomplete SPACE decision SPACE (foreas|ministries) |
    egkyklios_id_incomplete SPACE kya SPACE ministries SPACE AND SPACE ministries |
    (egkyklios|decision) SPACE aade SPACE ids |
    aade SPACE? ids (COMMA SPACE ids)* |
    PROTOCOL_TEXT SPACE ids SPACE egkyklios SPACE ministries |
    (YP_ARITHM SPACE)? ids SPACE praksi SPACE explicitCourt |
    decision SPACE egkyklios_id_complete
    ;

incompleteAdministrativeDoc :
    (PROTOCOL_TEXT SPACE)? ids SPACE egkyklios |
    egkyklios_id_incomplete SPACE (kya |decision) |
    //egkyklios_id_incomplete|
    //egkyklios_id_complete |
    ada
    ;

aade : POL ;
egkyklios : EGKYKLIOS_TEXT;
praksi: PRAKSI_TEXT;
foreas : FOREAS;
ada : ADA_TEXT COLON SPACE ada_id ;

//στις εγκυκλίους αν υπάρχει ο φορέας στο ID θεωρείται complete!
egkyklios_id_complete :
    (ALL_CHARS | IONIKO_SYSTEM)? DOT? NUM ((DOT|HYPHEN) NUM)* //Πριν το πρώτο '/'
        (SLASH (NUM|ALL_CHARS|DOT|HYPHEN|IONIKO_SYSTEM|SPACE|EGKYKLIOS_TEXT|COLON)+)*  //Ενδιάμεσα
        (SLASH (foreas|ministries))     //Καπου θα υπάρχει ο φορέας ή το Υπουργείο
        (SLASH (NUM|ALL_CHARS|DOT|HYPHEN|IONIKO_SYSTEM| SPACE|EGKYKLIOS_TEXT|COLON)+)*  //Ενδιάμεσα
    SLASH NUM ((HYPHEN|DOT) NUM)* IONIKO_SYSTEM?    |   //Τελευταίο '/'

    (ALL_CHARS | IONIKO_SYSTEM)? DOT? NUM ((DOT|HYPHEN) NUM)*
        (SLASH (NUM|ALL_CHARS|DOT|HYPHEN|IONIKO_SYSTEM|SPACE)+)*
        SLASH (aade SPACE? ids | ministries)
    //px Π.2869/2389/ΠΟΛ 137/4.5.1987
    ;

//Θελουν φτιάξιμο τα ids των εγκυκλίων και αποφάσεων (κυα κτλ)
egkyklios_id_incomplete :
    (ALL_CHARS | IONIKO_SYSTEM) DOT? NUM (DOT NUM)* //Πριν το πρώτο '/'
        (SLASH (NUM|ALL_CHARS|DOT|HYPHEN|IONIKO_SYSTEM)+)*  //Ενδιάμεσα
    SLASH NUM ((HYPHEN|DOT) NUM)* IONIKO_SYSTEM?    //Τελευταίο '/'
    ;
*/
//-----------------------------legislation--------------------------------------//
legislation:
    multipleLegislation |
    singleLegislation
    ;

singleLegislation :
    completeLegislation //|
    //incompleteLegislation
    ;

//Τα multiple στηρίζονται στο ΑΡΘΡΑ! Δημιουργία ξεχωριστού κανόνα!
//Μην αλλάξει η σειρά των κανόνων την έκατσες!!
/*multipleLegislation1:
    arthra SPACE m1 (COMMA SPACE m1)* SPACE AND SPACE m1 SPACE explicitKwdikas
        (COMMA SPACE m1)+ COMMA SPACE m3 SPACE AND SPACE m1 SPACE
        (OF SPACE)? (explicitLegalType | explicitKwdikas) |

    arthra SPACE m1 (COMMA SPACE (m1|m4))* SPACE AND SPACE m1 SPACE explicitKwdikas
        (COMMA SPACE 'καθώς' SPACE AND SPACE m1 SPACE (OF SPACE)? (explicitLegalType|explicitKwdikas))? |

    arthra SPACE m1 SPACE AND SPACE arthro_id SPACE explicitKwdikas |

    arthra SPACE m1 (COMMA SPACE (m1|m2))* SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas)
        (SPACE? (COMMA|AND) SPACE m1 SPACE explicitKwdikas)* |

    arthra SPACE m1 SPACE AND SPACE m1 SPACE (OF SPACE)? explicitLegalType |

    arthra SPACE m3 SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas)
        SPACE AND SPACE m1 SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas)|

    arthra SPACE m3 SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas)
        SPACE AND SPACE arthro_id SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas) |

    arthra SPACE m2 SPACE explicitKwdikas COMMA SPACE (arthro_id COMMA? SPACE)+ SPACE? explicitKwdikas
        SPACE AND SPACE m2 SPACE (OF SPACE)? explicitLegalType |

    arthra SPACE m1 SPACE AND SPACE m3 SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas) |

    singleLegislation (COMMA? SPACE AND SPACE (arthro_id|m1) SPACE (OF SPACE)? (explicitLegalType | explicitKwdikas))+ |

    arthra SPACE m3 COMMA (SPACE arthro_id COMMA)+
        SPACE arthro_id SPACE AND SPACE arthro_id
        SPACE (OF SPACE)? explicitKwdikas |

    arthra SPACE m3 (COMMA SPACE m1)+ SPACE AND SPACE arthro_id SPACE explicitKwdikas |

    arthra SPACE m2 SPACE explicitKwdikas
    ;
*/

par_mult : arthro_id SPACE PAR_TEXT SPACE? singleLegalElementId (SPACE (case_mult | passage_mult | element_mult))?;
case_mult : PERIPTWSI_TEXT SPACE singleLegalElementId;
passage_mult: EDAFIO_TEXT SPACE? singleLegalElementId;
element_mult: STOIXEIO_TEXT SPACE? singleLegalElementId;
//test : (arthro_id|mult_1) SPACE (OF SPACE)? explicitLegalType | arthro_id SPACE AND SPACE arthro_id;
/*multipleLegislation:
arthra SPACE par_mult SPACE (case_mult SPACE)? AND SPACE par_mult SPACE (OF SPACE)? explicitLegalType |
arthra SPACE par_mult COMMA? SPACE par_mult SPACE (OF SPACE)? explicitLegalType |
arthra SPACE par_mult SPACE (case_mult SPACE)? AND SPACE arthro_id SPACE (OF SPACE)? explicitLegalType |
arthra SPACE (par_mult COMMA? SPACE)+ AND SPACE par_mult SPACE (OF SPACE)? explicitLegalType
;*/


multipleLegislation :
    arthra SPACE par_mult (COMMA SPACE arthro_id)+ SPACE AND SPACE arthro_id SPACE (OF SPACE)? explicitLegalType |
    arthra SPACE par_mult SPACE (case_mult SPACE)? AND SPACE par_mult SPACE (OF SPACE)? explicitLegalType |
    arthra SPACE par_mult COMMA? SPACE par_mult SPACE (OF SPACE)? explicitLegalType |
    arthra SPACE par_mult SPACE (case_mult SPACE)? AND SPACE arthro_id SPACE (OF SPACE)? explicitLegalType|
    arthra SPACE (par_mult COMMA? SPACE)+ AND SPACE par_mult SPACE (OF SPACE)? explicitLegalType |
    arthra SPACE par_mult COMMA SPACE par_mult COMMA SPACE arthro_id COMMA SPACE arthro_id SPACE explicitPar SPACE (OF SPACE)? explicitLegalType |
    arthra SPACE par_mult COMMA SPACE arthro_id SPACE explicitPar SPACE (OF SPACE)? explicitLegalType|
    arthra SPACE arthro_id SPACE AND SPACE par_mult SPACE (OF SPACE)? explicitLegalType|
    //arthra SPACE arthro_id (COMMA arthro_id)+ SPACE (OF SPACE)? explicitLegalType|
    arthra SPACE arthro_id (COMMA SPACE? arthro_id)+ (SPACE AND SPACE arthro_id)? SPACE (OF SPACE explicitLegalElement SPACE)? (OF SPACE)? explicitLegalType |
    arthra SPACE arthro_id SPACE AND SPACE arthro_id SPACE (OF SPACE)? explicitLegalType |
    arthra SPACE multipleCompleteLegislation_1 COMMA SPACE multipleCompleteLegislation_1 |
    arthra SPACE multipleCompleteLegislation_1 SPACE AND SPACE multipleCompleteLegislation_1
    arthra SPACE multipleCompleteLegislation_1 (COMMA SPACE SINCE SPACE AND SPACE multipleCompleteLegislation_1)? |
    arthra SPACE multipleCompleteLegislation_1 (SPACE? (COMMA|AND) SPACE multipleCompleteLegislation_1)+ |
    arthra SPACE multipleCompleteLegislation_1 SPACE AND SPACE multipleCompleteLegislation_1 |
    arthra SPACE multipleCompleteLegislation_1 COMMA SPACE multipleCompleteLegislation_1
        SPACE AND SPACE multipleCompleteLegislation_1 |
    singleLegislation (multipleCompleteLegislation_1)+
    //|
    //explicitLegalType SPACE AND SPACE law_id

    ;

multipleCompleteLegislation_1:
    m1 (COMMA SPACE m1)* SPACE AND SPACE m1 SPACE explicitLegalType |
    //(m1)+ COMMA SPACE m3 SPACE AND SPACE m1 SPACE (OF SPACE)? explicitLegalType |
    m1 (COMMA SPACE m1)* SPACE AND SPACE m1 SPACE explicitLegalType |
    m1 SPACE (OF SPACE)? explicitLegalType |
    m1 SPACE AND SPACE arthro_id SPACE explicitLegalType |
    m1 (COMMA SPACE? (m1|m2))* SPACE (OF SPACE)? explicitLegalType |
    m1 SPACE AND SPACE m1 SPACE (OF SPACE)? explicitLegalType |
    //m3 SPACE (OF SPACE)? explicitLegalType |
    arthro_id SPACE (OF SPACE)? explicitLegalType |
    m2 SPACE (OF SPACE)? explicitLegalType |
    //m1 SPACE AND SPACE m3 SPACE (OF SPACE)? explicitLegalType |
    COMMA? SPACE AND SPACE (arthro_id|m1) SPACE (OF SPACE)? explicitLegalType |
    //m3 COMMA (SPACE arthro_id COMMA)+ SPACE arthro_id SPACE AND SPACE arthro_id SPACE (OF SPACE)? explicitLegalType |
    //m3 (COMMA SPACE m1)+ SPACE AND SPACE arthro_id SPACE explicitLegalType |
    arthra SPACE arthro_id SPACE AND SPACE arthro_id SPACE OF SPACE SPECIAL_TEXT SPACE explicitLegalType
    ;

completeLegislation :
    //explicitLegalElement SPACE explicitLegalElement SPACE OF SPACE explicitLegalElement SPACE OF SPACE explicitLegalType|
    explicitLegalElement
        (SPACE? ((STO | OF | BRACKET) SPACE?)? explicitLegalElement BRACKET?)*
        //SPACE (OF SPACE)? (explicitLegalType|ypourgApof_id) (SPACE ME_TO SPACE explicitLegalElement)? |
        SPACE? (OF SPACE)? explicitLegalType (SPACE ME_TO SPACE explicitLegalElement)? |
    BRACKET (explicitLegalType) SPACE arthro_id BRACKET |
    explicitLegalType SPACE STO SPACE explicitLegalElement |
    explicitLegalType |
    explicitLegalType (SPACE BRACKET explicitLegalElement BRACKET)? |
    //fek |
    BRACKET explicitLegalType COMMA SPACE explicitLegalElement BRACKET |
    arthra SPACE range_id SPACE (OF SPACE)? explicitLegalType |
    explicitLegalElement SPACE AND SPACE 'στις' SPACE explicitLegalElement SPACE OF SPACE explicitLegalType |
    explicitLegalElement (COMMA SPACE explicitLegalElement)+ SPACE (OF SPACE)? explicitLegalType
;

incompleteLegislation:
    explicitLegalElement (SPACE? ((STO | OF | BRACKET) SPACE?)? explicitLegalElement BRACKET?)* SPACE (OF SPACE)? (implicitKwdikas|implicitLegalType) |
    explicitLegalElement (SPACE (OF SPACE)? (implicitLegalElement)) SPACE AND SPACE legislative_type //|
    //explicitLegalElement SPACE possible_title SPACE (OF SPACE)? implicitLegalType
;

explicitLegalElement :
    explicitParartima |
    explicitPart |
    explicitChapter|
    explicitArthro |
    explicitPar |
    explicitSubPar |
    explicitPeriptwsi |
    explicitStoixeio |
    explicitEdafio |
    explicitPoint
    ;

implicitLegalElement :
    implicitChapter |
    implicitArthro |
    implicitPar |
    implicitSubPar |
    implicitPeriptwsi |
    implicitStoixeio |
    implicitEdafio
    ;

explicitPoint : POINT_TEXT SPACE singleLegalElementId;
explicitPart : PART_TEXT SPACE singleLegalElementId;

implicitChapter : special SPACE (OF SPACE)? CHAPTER_TEXT | CHAPTER_TEXT SPACE special;
explicitChapter : CHAPTER_TEXT SPACE singleLegalElementId ;

implicitArthro : special (COMMA? SPACE special COMMA?)? SPACE (OF SPACE)? ARTHRO_TEXT | ARTHRO_TEXT SPACE special;
explicitArthro :
    (special SPACE)? ARTHRO_TEXT SPACE ((range_id|multipleLegalElementIds|singleLegalElementId) (SPACE next_all)?)
        (SPACE? (COMMA|AND) SPACE? (range_id|multipleLegalElementIds|singleLegalElementId))*;
explicitArthro_1 :
    (special SPACE)? ARTHRA_PLURAL SPACE ((range_id|arthro_id) (SPACE next_all)?)
        (SPACE? (COMMA|AND) SPACE? (range_id|arthro_id))*;

implicitPar: special SPACE (OF SPACE)? PAR_TEXT | PAR_TEXT SPACE special;
explicitPar: PAR_TEXT SPACE? (multipleLegalElementIds|singleLegalElementId|range_id);

implicitSubPar : special SPACE (OF SPACE)? SUBPAR_TEXT | SUBPAR_TEXT SPACE special;
explicitSubPar : SUBPAR_TEXT SPACE? (multipleLegalElementIds|singleLegalElementId);

implicitPeriptwsi : special SPACE (OF SPACE)? PERIPTWSI_TEXT | PERIPTWSI_TEXT SPACE special;
explicitPeriptwsi : PERIPTWSI_TEXT SPACE? (multipleLegalElementIds|singleLegalElementId);

implicitStoixeio : special SPACE (OF SPACE)? STOIXEIO_TEXT | STOIXEIO_TEXT SPACE special;
explicitStoixeio : STOIXEIO_TEXT SPACE (multipleLegalElementIds|singleLegalElementId);

implicitEdafio : special SPACE (OF SPACE)? EDAFIO_TEXT | EDAFIO_TEXT SPACE special;
explicitEdafio : (multipleLegalElementIds|singleLegalElementId) SPACE EDAFIO_TEXT | EDAFIO_TEXT SPACE? (multipleLegalElementIds|singleLegalElementId) ;

explicitParartima : parartima SPACE latin_id;

implicitLegalType : (OF SPACE)? special SPACE (OF SPACE)? legislative_type | legislative_type SPACE special;
explicitLegalType :
    legislative_type SPACE? (OF SPACE)? law_id |//(SPACE? (COMMA | AND) SPACE? law_id)* |//(SPACE fek)? |
    (OF SPACE)? special SPACE syntagma |
    syntagma |
    law_id SPACE legislative_type |
    explicitKwdikas
    ;

implicitKwdikas: (OF SPACE)? special SPACE KWDIKAS_TEXT;
explicitKwdikas:
KWDIKAS_FOROLOGIKIS_DIADIKASIAS
|YPALLILIKOS_KWDIKAS
|AGROTIKOS_KWDIKAS
|ALIEUTIKOS_KWDIKAS
|ASTIKOS_KWDIKAS
|AGORANOMIKOS_KWDIKAS
|GENIKOS_OIKODOMIKOS_KANONISMOS
|NEOS_OIKODOMIKOS_KANONISMOS
|KWDIKAS_ADEIWN_FORTIGWN_AUTOKINITWN
|KWDIKAS_APODIMIAS_METANASTEUSIS_DIAVATIRIA
|KWDIKAS_DEONTOLOGIAS_DIKIGORIKOU_LEITOURGIMATOS
|KWDIKAS_DIATAGMATWN_GIA_DIMOTOLOGIA
|KWDIKAS_DIATAKSEWN_STRATOLOGIKIS_FISIS
|KWDIKAS_ELLINIKIS_ITHAGENEIAS
|KWDIKAS_ESODWN_DIMWN_KAI_KOINOTITWN
|DASIKOS_KWDIKAS
|KWDIKAS_AEROPORIKOY_DIKAIOY
|KWDIKAS_KATASKEUIS_DIMOSIWN_ERGWN
|KWDIKAS_NOMOTHESIAS_KUVERNISIS
|KWDIKAS_NOMWN_GIA_NARKWTIKA
|KWDIKAS_PAROXIS_EPENDITIKWN_KINITRWN
|KWDIKAS_PERI_ARXAIOTITWN
|KWDIKAS_SYNALLAGWN_HLEKTRIKIS_ENERGEIAS
|KWDIKAS_TAMEIOU_NOMIKWN
|KWDIKAS_TROFIMWN_KAI_POTWN
|KWDIKAS_FOROLOGIAS_KAPNOU
|KWDIKAS_FOROLOGIKWN_STOIXEIWN
|KWDIKAS_ANAGK_APAL_AKINITWN
|KWDIKAS_BIBLIWN_KAI_STOIXEIWN
|KWDIKAS_POINIKIS_DIKONOMIAS
|POINIKOS_KWDIKAS
|ETHNIKOS_TELWNIAKOS_KWDIKAS
|KWDIKAS_FOROLOGIAS_EISODIMATOS
|KWDIKAS_BASIKIS_POLEODOMIKIS_NOMOTHESIAS
|KTINOTROFIKOS_KWDIKAS
|KWDIKAS_TELWN_XARTOSIMOU
|KWDIKAS_BASIKWN_KANONWN_KRATOUMENWN
|KWDIKAS_FOROLOGIKIS_DIKONOMIAS
|KWDIKAS_DIKIGORWN
|KWDIKAS_DIMOSIOU_LOGISTIKOU
|KWDIKAS_DIMOSIOU_NAUTIKOU_DIKAIOU
|KWDIKAS_FOROY_PROSTITHEMENIS_AKSIAS
|KWDIKAS_POLITIKIS_DIKONOMIAS
|KWDIKAS_DHMWN_KAI_KOINOTITWN
|KWDIKAS_ODIKIS_KYKLOFORIAS
|KWDIKAS_DIKASTIKOU_SWMATOS_ENOPLWN_DINAMEWN
|KWDIKAS_DIKASTIKWN_EPIMELITWN
|KWDIKAS_ORGANISMOU_DIKASTIRIWN
|KWDIKAS_DIKASTIKWN_YPALLHLWN
|KWDIKAS_DIKWN_DIMOSIOU
|KWDIKAS_DIOIKITIKIS_DIADIKASIAS
|KWDIKAS_DIOIKITIKIS_DIKONOMIAS
|KWDIKAS_EISPRAKSEWN_DHMOSIWN_ESODWN
|KWDIKAS_FARMAKEUTIKIS_DEONTOLOGIAS
|KWDIKAS_IDIWTIKOU_NAUTIKOU_DIKAIOU
|KWDIKAS_POLEMIKWN_SYNTAKSEWN
|KWDIKAS_METOXIKOU_TAMEIOU_POLITIKWN_YPALLHLWN
|KWDIKAS_METOXIKOU_TAMEIOU_STRATOU
|KWDIKAS_PROSOPIKOU_LIMENIKOU_SWMATOS
|KWDIKAS_SYMVOLEOGRAFWN
|KWDIKAS_SYNTAKSEWN_PROSOPIKOU_OSE
|KWDIKAS_ANOTATOU_EIDIKOU_DIKASTIRIOU
|KWDIKAS_FOROLOGIAS_KLIRONOMIWN
|KWDIKAS_FOROLOGIKIS_APEIKONISIS_SYNALLAGWN
|KWDIKAS_POLITIKWN_KAI_STRATIWTIKWN_SUNTAKSEWN

;
/*explicitKwdikas:
    kwdikasForologikisDiadikasias |
    ypallilikosKwdikas |
    agrotikosKwdikas |
    alieutikosKwdikas |
    astikosKwdikas |
    agoranomikosKwdikas |
    genikosOikodomikosKanonismos |
    neosOikodomikosKanonismos |
    kwdikasAdeiwnFortigwnAutokinitwn |
    kwdikasApodimiasMetanasteusisDiavatiria |
    kwdikasDeontologiasDikigorikouLeitourgimatos |
    kwdikasDiatagmatwnGiaDimotologia |
    kwdikasDiataksewnStratologikisFisis |
    kwdikasEllinikisIthageneias |
    kwdikasEsodwnDimwnKaiKoinotitwn |
    dasikosKwdikas |
    kwdikasAeroporikouDikaiou |
    kwdikasKataskeuisDimosiwnErgwn |
    kwdikasNomothesiasKuvernisis |
    kwdikasNomwnGiaNarkwtika |
    kwdikasParoxisEpenditikwnKinitrwn |
    kwdikasPeriArxaiotitwn |
    kwdikasSynallagwnHlektrikisEnergeias |
    kwdikasTameiouNomikwn |
    kwdikasTrofimwnKaiPotwn |
    kwdikasForologiasKapnou |
    kwdikasForologikwnStoixeiwn |
    kwdikasAnagkApalSeon |
    kwdikasBibliwnKaiStoixeiwn |
    kwdikasPoinikisDikonomias |
    poinikosKwdikas |
    ethnikosTelwniakosKwdikas |
    kwdikasForologiasEisodimatos |
    kwdikasBasikisPoleodomNomothesias |
    ktinotrofikosKwdikas |
    kwdikasTelwnXartosimou |
    kwdikasBasikwnKanonwnKratoumenwn |
    kwdikasForologikisDikonomias |
    kwdikasDikigorwn |
    kwdikasDimosiouLogistikou |
    kwdikasDimosiouNautikouDikaiou |
    kwdikasForouProstithemenisAksias |
    kwdikasPolitikisDikonomias |
    kwdikasDhmwnKaiKoinotitwn |
    kwdikasOdikisKykloforias |
    kwdikasDikastikouSwmatosEnoplwnDinamewn |
    kwdikasDikastikwnEpimelitwn |
    kwdikasOrganismouDikastiriwn |
    kwdikasDikastikwnYpallhlwn |
    kwdikasDikwnDimosiou |
    kwdikasDioikitikisDiadikasias |
    kwdikasDioikitikisDikonomias |
    kwdikasEispraksewnDhmosiwnEsodwn |
    kwdikasFarmakeutikisDeontologias |
    kwdikasIdiwtikouNautikouDikaiou |
    kwdikasPolemikwnSyntaksewn |
    kwdikasMetoxikouTameiouPolitikwnYpallhlwnContext |
    kwdikasMetoxikouTameiouStratou |
    kwdikasProsopikouLimenikouSwmatos |
    kwdikasSymvoleografwn |
    kwdikasSyntaksewnProsopikouOse |
    kwdikasAnotatouEidikouDikastiriou |
    kwdikasForologiasKlironomiwn |
    kwdikasForologikisApeikonisisSynallagwn|
    kwdikasPolitikwnKaiStratiwtikwnSyntaksewn
    ;


kwdikasForologikisDiadikasias : KWDIKAS_FOROLOGIKIS_DIADIKASIAS;
ypallilikosKwdikas : YPALLILIKOS_KWDIKAS;
agrotikosKwdikas : AGROTIKOS_KWDIKAS;
alieutikosKwdikas : ALIEUTIKOS_KWDIKAS;
astikosKwdikas : ASTIKOS_KWDIKAS;
agoranomikosKwdikas : AGORANOMIKOS_KWDIKAS;
genikosOikodomikosKanonismos : GENIKOS_OIKODOMIKOS_KANONISMOS;
neosOikodomikosKanonismos : NEOS_OIKODOMIKOS_KANONISMOS;
kwdikasAdeiwnFortigwnAutokinitwn : KWDIKAS_ADEIWN_FORTIGWN_AUTOKINITWN;
kwdikasApodimiasMetanasteusisDiavatiria : KWDIKAS_APODIMIAS_METANASTEUSIS_DIAVATIRIA;
kwdikasDeontologiasDikigorikouLeitourgimatos : KWDIKAS_DEONTOLOGIAS_DIKIGORIKOU_LEITOURGIMATOS;
kwdikasDiatagmatwnGiaDimotologia : KWDIKAS_DIATAGMATWN_GIA_DIMOTOLOGIA;
kwdikasDiataksewnStratologikisFisis : KWDIKAS_DIATAKSEWN_STRATOLOGIKIS_FISIS;
kwdikasEllinikisIthageneias : KWDIKAS_ELLINIKIS_ITHAGENEIAS;
kwdikasEsodwnDimwnKaiKoinotitwn : KWDIKAS_ESODWN_DIMWN_KAI_KOINOTITWN;
dasikosKwdikas : DASIKOS_KWDIKAS;
kwdikasAeroporikouDikaiou : KWDIKAS_AEROPORIKOY_DIKAIOY;
kwdikasKataskeuisDimosiwnErgwn : KWDIKAS_KATASKEUIS_DIMOSIWN_ERGWN;
kwdikasNomothesiasKuvernisis : KWDIKAS_NOMOTHESIAS_KUVERNISIS;
kwdikasNomwnGiaNarkwtika : KWDIKAS_NOMWN_GIA_NARKWTIKA;
kwdikasParoxisEpenditikwnKinitrwn : KWDIKAS_PAROXIS_EPENDITIKWN_KINITRWN;
kwdikasPeriArxaiotitwn : KWDIKAS_PERI_ARXAIOTITWN;
kwdikasSynallagwnHlektrikisEnergeias: KWDIKAS_SYNALLAGWN_HLEKTRIKIS_ENERGEIAS;
kwdikasTameiouNomikwn : KWDIKAS_TAMEIOU_NOMIKWN;
kwdikasTrofimwnKaiPotwn : KWDIKAS_TROFIMWN_KAI_POTWN;
kwdikasForologiasKapnou : KWDIKAS_FOROLOGIAS_KAPNOU;
kwdikasForologikwnStoixeiwn : KWDIKAS_FOROLOGIKWN_STOIXEIWN;
kwdikasAnagkApalSeon : KWDIKAS_ANAGK_APAL_AKINITWN;
kwdikasBibliwnKaiStoixeiwn : KWDIKAS_BIBLIWN_KAI_STOIXEIWN;
kwdikasPoinikisDikonomias : KWDIKAS_POINIKIS_DIKONOMIAS;
poinikosKwdikas : POINIKOS_KWDIKAS;
ethnikosTelwniakosKwdikas : ETHNIKOS_TELWNIAKOS_KWDIKAS;
kwdikasForologiasEisodimatos : KWDIKAS_FOROLOGIAS_EISODIMATOS;
kwdikasBasikisPoleodomNomothesias : KWDIKAS_BASIKIS_POLEODOMIKIS_NOMOTHESIAS;
ktinotrofikosKwdikas : KTINOTROFIKOS_KWDIKAS;
kwdikasTelwnXartosimou : KWDIKAS_TELWN_XARTOSIMOU;
kwdikasBasikwnKanonwnKratoumenwn : KWDIKAS_BASIKWN_KANONWN_KRATOUMENWN;
kwdikasForologikisDikonomias : KWDIKAS_FOROLOGIKIS_DIKONOMIAS;
kwdikasDikigorwn : KWDIKAS_DIKIGORWN;
kwdikasDimosiouLogistikou : KWDIKAS_DIMOSIOU_LOGISTIKOU;
kwdikasDimosiouNautikouDikaiou : KWDIKAS_DIMOSIOU_NAUTIKOU_DIKAIOU;
kwdikasForouProstithemenisAksias : KWDIKAS_FOROY_PROSTITHEMENIS_AKSIAS;
kwdikasPolitikisDikonomias : KWDIKAS_POLITIKIS_DIKONOMIAS;
kwdikasDhmwnKaiKoinotitwn : KWDIKAS_DHMWN_KAI_KOINOTITWN;
kwdikasOdikisKykloforias : KWDIKAS_ODIKIS_KYKLOFORIAS;
kwdikasDikastikouSwmatosEnoplwnDinamewn : KWDIKAS_DIKASTIKOU_SWMATOS_ENOPLWN_DINAMEWN;
kwdikasDikastikwnEpimelitwn : KWDIKAS_DIKASTIKWN_EPIMELITWN;
kwdikasOrganismouDikastiriwn : KWDIKAS_ORGANISMOU_DIKASTIRIWN;
kwdikasDikastikwnYpallhlwn : KWDIKAS_DIKASTIKWN_YPALLHLWN;
kwdikasDikwnDimosiou : KWDIKAS_DIKWN_DIMOSIOU;
kwdikasDioikitikisDiadikasias : KWDIKAS_DIOIKITIKIS_DIADIKASIAS;
kwdikasDioikitikisDikonomias : KWDIKAS_DIOIKITIKIS_DIKONOMIAS;
kwdikasEispraksewnDhmosiwnEsodwn : KWDIKAS_EISPRAKSEWN_DHMOSIWN_ESODWN;
kwdikasFarmakeutikisDeontologias : KWDIKAS_FARMAKEUTIKIS_DEONTOLOGIAS;
kwdikasIdiwtikouNautikouDikaiou : KWDIKAS_IDIWTIKOU_NAUTIKOU_DIKAIOU;
kwdikasPolemikwnSyntaksewn : KWDIKAS_POLEMIKWN_SYNTAKSEWN;
kwdikasMetoxikouTameiouPolitikwnYpallhlwnContext : KWDIKAS_METOXIKOU_TAMEIOU_POLITIKWN_YPALLHLWN;
kwdikasMetoxikouTameiouStratou : KWDIKAS_METOXIKOU_TAMEIOU_STRATOU;
kwdikasProsopikouLimenikouSwmatos : KWDIKAS_PROSOPIKOU_LIMENIKOU_SWMATOS;
kwdikasSymvoleografwn : KWDIKAS_SYMVOLEOGRAFWN;
kwdikasSyntaksewnProsopikouOse : KWDIKAS_SYNTAKSEWN_PROSOPIKOU_OSE;
kwdikasAnotatouEidikouDikastiriou : KWDIKAS_ANOTATOU_EIDIKOU_DIKASTIRIOU;
kwdikasForologiasKlironomiwn : KWDIKAS_FOROLOGIAS_KLIRONOMIWN;
kwdikasForologikisApeikonisisSynallagwn :KWDIKAS_FOROLOGIKIS_APEIKONISIS_SYNALLAGWN;
*/
legislative_type :
    acts |
    presidential_decree |
    compulsory_law |
    decree_law |
    decree |
    royal_decree
    ;

acts : ACTS;
presidential_decree: PRESIDENTIAL_DECREE;
compulsory_law: COMPULSORY_LAW;
decree_law : DECREE_LAW;
decree: DECREE;
royal_decree: ROYAL_DECREE;
syntagma : SYNTAGMA;
/*ypourgApof_id :
    (ALL_CHARS) NUM //Πριν το πρώτο '/'
        (SLASH (NUM|ALL_CHARS|DOT|HYPHEN|IONIKO_SYSTEM)+)*  //Ενδιάμεσα
    SLASH NUM ((HYPHEN|DOT) NUM)*     //Τελευταίο '/'
    ;*/
//kya : KYA;
//possible_title : '«'.*?'»' ;
//fek: FEK;
special : COMMA? SPECIAL_TEXT (SPACE COMMA)?;
range_id : (singleLegalElementId|arthro_id) SPACE? (RANGE|HYPHEN) SPACE? (singleLegalElementId|arthro_id);
arthra : ARTHRA_PLURAL;

m1 : arthro_id COMMA? (SPACE explicitLegalElement)+ | arthro_id (SPACE AND SPACE arthro_id)?;
m2 : arthro_id (SPACE next_all)? ;
//m3 : arthro_id (SPACE explicitLegalElement)+;
//m4 : arthro_id COMMA SPACE explicitLegalElement;
//m5 : arthro_id;
next_all : NEXT_ALL;


//--------------------courtDecision----------------------------------//
courtDecision:
    singleCourtDec |
    multipleCourtsDec
    ;

singleCourtDec :
    completeCourtDec //|
    //incompleteCourtDec
    ;

multipleCourtsDec:
    decision SPACE? COLON? SPACE? (incompleteCourtDecAlt|completeCourtDecAlt)
        (SPACE AND SPACE (incompleteCourtDecAlt|completeCourtDecAlt))*
    ;

completeCourtDec :
    completeCourtMultipleDecisions |
    completeCourtSingleDecision
    ;

completeCourtMultipleDecisions :
    explicitCourt SPACE multiple_ids SPACE AND SPACE multiple_ids |
    explicitCourt SPACE multiple_ids (COMMA SPACE multiple_ids (SPACE (OLOMELEIA|MELI))?)+ |
    explicitCourt SPACE multiple_ids (SPACE special)?
            ((COMMA SPACE (MELI|OLOMELEIA))? SPACE? COMMA? SPACE? (multiple_ids) (SPACE OLOMELEIA)?)+ |
    explicitCourt SPACE (multiple_ids (SPACE (OLOMELEIA|MELI))? COMMA SPACE)+ multiple_ids? |
    explicitCourt COMMA? SPACE? multiple_ids (SPACE (OLOMELEIA|MELI))? (SPACE? COMMA SPACE? multiple_ids)+ |
    multiple_ids COMMA SPACE multiple_ids SPACE* explicitCourt |
    multiple_ids SPACE AND SPACE multiple_ids SPACE decision SPACE? explicitCourt |
    decision SPACE multiple_ids SPACE AND SPACE multiple_ids SPACE explicitCourt |
    explicitCourt SPACE BRACKET multiple_ids (COMMA SPACE multiple_ids)+ BRACKET?

    ;


completeCourtSingleDecision :
    (YP_ARITHM SPACE)? (btrimeles SPACE)? ids SPACE (special SPACE)? decision SPACE explicitCourt |
    decision SPACE ids SPACE explicitCourt |
    explicitCourt SPACE ids (SPACE special)? |
    explicitCourt SPACE? ids (SPACE OLOMELEIA)? |
    decision SPACE YP_ARITHM SPACE ids COMMA SPACE explicitCourt
    ;


incompleteCourtDec :
    ids SPACE special SPACE decision SPACE implicitCourt
    ;

completeCourtDecAlt :
    (ids (SPACE | COMMA? SPACE special COMMA? SPACE))+ explicitCourt
    ;

incompleteCourtDecAlt :
    (ids (SPACE | COMMA? SPACE special COMMA? SPACE))+ implicitCourt
    ;

decision: DECISION_ELEMENT;

//---------------------------------IDs------------------------------------------//
//NUM ~SLASH: Στις παραγράφους χρησιμοποιείται ίδιο λεκτικό (αριθμό) με το αριθμό
// για ανέβασμα απόφασης σε πινάκιο σε δικαστικές αποφάσεις

singleLegalElementId : (NUM SPACE? IONIKO_SYSTEM | NUM '°'? | IONIKO_SYSTEM | LEKTIKO_ID | IONIKO_SYSTEM NUM);
multipleLegalElementIds : (singleLegalElementId|range_id) (SPACE? (COMMA|AND|COMMA SPACE AND) SPACE (singleLegalElementId|range_id))+;
arthro_id : (NUM SPACE? IONIKO_SYSTEM | NUM | LEKTIKO_ID);
ids: NUM SPACE? ((DOT|HYPHEN|COMMA) SPACE? NUM DOT?)? ((SLASH|BACKSLASH) SPACE? NUM (SPACE? (DOT|HYPHEN) NUM)*)+ ;//(SLASH EOK)? | date_id;
multiple_ids :  NUM ( SPACE? (DOT|HYPHEN|COMMA) SPACE? NUM)* SLASH NUM; //Δες στο ΣΤΕ τρόπο γραφής (ΣτΕ 1317, 1318/1979)
date_id : NUM (HYPHEN NUM)+;
law_id : ids | ALL_CHARS SLASH NUM;
latin_id : LATIN_ID;
//ada_id : (NUM|ALL_CHARS|IONIKO_SYSTEM)+ HYPHEN (NUM|ALL_CHARS|IONIKO_SYSTEM)+;
//lektiko_id : LEKTIKO_ID;

//---------------------------------------------------------------------------------//
explicitCourt: (OF SPACE ((ALL_CHARS|IONIKO_SYSTEM NUM?) SPACE)+)? (OF SPACE)? dikastirio; //EDW allagi tou "COURT" me (ste | dikastirio)

//dikastirio:
//COURT
//;
//  MAGISTRATE_COURT: Πλημμελειοδικεία
//  APELLATE_COURT : Εφετεία
//  FIRST_INSTANCE_COURT : Πρωτοδικεία
//  COUNTY_COURT: Ειρηνοδικεία
//  DISTRICT_COURT: Πταισματοδικεία
dikastirio :
(OLOMELEIA SPACE)? STE SPACE? OLOMELEIA?
|SUPREME_COURT
|AED
|MAGISTRATE_COURT_OF_THESSALONIKI
|MAGISTRATE_COURT_OF_LAMIA
|MAGISTRATE_COURT_OF_PIRAEUS
|MAGISTRATE_COURT_OF_ATHENS
|APELLATE_COURT_OF_ATHENS
|APELLATE_COURT_OF_LAMIA
|APELLATE_COURT_OF_PIRAEUS
|APELLATE_COURT_OF_THESSALONIKI
|APELLATE_COURT_OF_CORFU
|APELLATE_COURT_OF_THRAKI
|APELLATE_COURT_OF_IOANNINA
|APELLATE_COURT_OF_DODEKANISA
|APELLATE_COURT_OF_AEGEAN
|APELLATE_COURT_OF_CRETE
|APELLATE_COURT_OF_WEST_MACEDONIA
|APELLATE_COURT_OF_LARISA
|APELLATE_COURT_OF_NAFPLIO
|APELLATE_COURT_OF_PATRAS
|APELLATE_COURT_OF_WEST_STEREAS
|APELLATE_COURT_OF_NORTH_AEGEAN
|APELLATE_COURT_OF_EAST_CRETE
|APELLATE_COURT_OF_KALAMATA
|APELLATE_COURT_OF_EVOIA
|FIRST_INSTANCE_COURT_OF_ATHENS
|FIRST_INSTANCE_COURT_OF_LAMIA
|FIRST_INSTANCE_COURT_OF_AMFISSA
|FIRST_INSTANCE_COURT_OF_EVRITANIA
|FIRST_INSTANCE_COURT_OF_LIVADIA
|FIRST_INSTANCE_COURT_OF_PIRAEUS
|FIRST_INSTANCE_COURT_OF_THESSALONIKI
|FIRST_INSTANCE_COURT_OF_VEROIA
|FIRST_INSTANCE_COURT_OF_EDESSA
|FIRST_INSTANCE_COURT_OF_KATERINI
|FIRST_INSTANCE_COURT_OF_KILKIS
|FIRST_INSTANCE_COURT_OF_SERRES
|FIRST_INSTANCE_COURT_OF_XALKIDIKI
|FIRST_INSTANCE_COURT_OF_CORFU
|FIRST_INSTANCE_COURT_OF_GIANNITSA
|FIRST_INSTANCE_COURT_OF_THESPRWTIA
|FIRST_INSTANCE_COURT_OF_RODOPI
|FIRST_INSTANCE_COURT_OF_DRAMA
|FIRST_INSTANCE_COURT_OF_EVROS
|FIRST_INSTANCE_COURT_OF_KAVALA
|FIRST_INSTANCE_COURT_OF_XANTHI
|FIRST_INSTANCE_COURT_OF_ORESTIADA
|FIRST_INSTANCE_COURT_OF_IOANNINA
|FIRST_INSTANCE_COURT_OF_ARTA
|FIRST_INSTANCE_COURT_OF_PREVEZA
|FIRST_INSTANCE_COURT_OF_RODOS
|FIRST_INSTANCE_COURT_OF_KOS
|FIRST_INSTANCE_COURT_OF_SYROS
|FIRST_INSTANCE_COURT_OF_SAMOS
|FIRST_INSTANCE_COURT_OF_NAXOS
|FIRST_INSTANCE_COURT_OF_CHANIA
|FIRST_INSTANCE_COURT_OF_RETHYMNO
|FIRST_INSTANCE_COURT_OF_KOZANI
|FIRST_INSTANCE_COURT_OF_GREVENA
|FIRST_INSTANCE_COURT_OF_KASTORIA
|FIRST_INSTANCE_COURT_OF_FLORINA
|FIRST_INSTANCE_COURT_OF_LARISA
|FIRST_INSTANCE_COURT_OF_VOLOS
|FIRST_INSTANCE_COURT_OF_KARDITSA
|FIRST_INSTANCE_COURT_OF_TRIKALA
|FIRST_INSTANCE_COURT_OF_NAFPLIO
|FIRST_INSTANCE_COURT_OF_CORINTH
|FIRST_INSTANCE_COURT_OF_SPARTI
|FIRST_INSTANCE_COURT_OF_TRIPOLI
|FIRST_INSTANCE_COURT_OF_KALAMATA
|FIRST_INSTANCE_COURT_OF_KIPARISSIA
|FIRST_INSTANCE_COURT_OF_GYHTEIO
|FIRST_INSTANCE_COURT_OF_PATRAS
|FIRST_INSTANCE_COURT_OF_AIGIO
|FIRST_INSTANCE_COURT_OF_KALAVRITA
|FIRST_INSTANCE_COURT_OF_HLEIAS
|FIRST_INSTANCE_COURT_OF_AMALIADA
|FIRST_INSTANCE_COURT_OF_ZAKINTHOS
|FIRST_INSTANCE_COURT_OF_KEFALLONIA
|FIRST_INSTANCE_COURT_OF_AGRINIO
|FIRST_INSTANCE_COURT_OF_LEFKADA
|FIRST_INSTANCE_COURT_OF_MESOLOGGI
|FIRST_INSTANCE_COURT_OF_MITILINI
|FIRST_INSTANCE_COURT_OF_CHIOS
|FIRST_INSTANCE_COURT_OF_HRAKLEIO
|FIRST_INSTANCE_COURT_OF_LASITHI
|FIRST_INSTANCE_COURT_OF_THIVA
|FIRST_INSTANCE_COURT_OF_CHALKIDA
|COUNTY_COURT_OF_ATHENS
|COUNTY_COURT_OF_MAROUSSI
|COUNTY_COURT_OF_AXARNON
|COUNTY_COURT_OF_ELEFSINA
|COUNTY_COURT_OF_KALLITHEA
|COUNTY_COURT_OF_KROPIA
|COUNTY_COURT_OF_LAVRIO
|COUNTY_COURT_OF_NEAS_IONIAS
|COUNTY_COURT_OF_NEA_LIOSIA
|COUNTY_COURT_OF_MARATHONA
|COUNTY_COURT_OF_MEGARA
|COUNTY_COURT_OF_PERISTERI
|COUNTY_COURT_OF_CHALANDRI
|COUNTY_COURT_OF_LAMIA
|COUNTY_COURT_OF_ATALANTI
|COUNTY_COURT_OF_AMFISSA
|COUNTY_COURT_OF_EVRITANIA
|COUNTY_COURT_OF_LIVADIA
|COUNTY_COURT_OF_AIGINA
|COUNTY_COURT_OF_KALAVRIA
|COUNTY_COURT_OF_KITHIRA
|COUNTY_COURT_OF_NIKAIAS
|COUNTY_COURT_OF_SALAMINA
|COUNTY_COURT_OF_SPETSES
|COUNTY_COURT_OF_THESSALONIKI
|COUNTY_COURT_OF_PIRAEUS
|COUNTY_COURT_OF_VASILIKON
|COUNTY_COURT_OF_KOUFALION
|COUNTY_COURT_OF_LAGKADA
|COUNTY_COURT_OF_ALEXANDRIA
|COUNTY_COURT_OF_NAOUSA
|COUNTY_COURT_OF_EDESSA
|COUNTY_COURT_OF_ALMOPIA
|COUNTY_COURT_OF_SKYDRA
|COUNTY_COURT_OF_PIERIA
|COUNTY_COURT_OF_KOLINDROU
|COUNTY_COURT_OF_POLIKASTRO
|COUNTY_COURT_OF_SERRES
|COUNTY_COURT_OF_NIGRITA
|COUNTY_COURT_OF_RODOLIVON
|COUNTY_COURT_OF_SINTIKIS
|COUNTY_COURT_OF_POLIGIROU
|COUNTY_COURT_OF_ARNAIA
|COUNTY_COURT_OF_KASSANDRA
|COUNTY_COURT_OF_NEA_MOUDANIA
|COUNTY_COURT_OF_CORFU
|COUNTY_COURT_OF_IGOUMENITSA
|COUNTY_COURT_OF_KOMOTINI
|COUNTY_COURT_OF_DRAMA
|COUNTY_COURT_OF_THASOS
|COUNTY_COURT_OF_PAGGAIOU
|COUNTY_COURT_OF_ORESTIADA
|COUNTY_COURT_OF_ALEXANDROUPOLI
|COUNTY_COURT_OF_KAVALA
|COUNTY_COURT_OF_DIDIMOTEIXO
|COUNTY_COURT_OF_IOANNINA
|COUNTY_COURT_OF_KONITSA
|COUNTY_COURT_OF_ARTA
|COUNTY_COURT_OF_PREVEZA
|COUNTY_COURT_OF_RODOS
|COUNTY_COURT_OF_KARPATHOS
|COUNTY_COURT_OF_KALIMNOS
|COUNTY_COURT_OF_KOS
|COUNTY_COURT_OF_LEROS
|COUNTY_COURT_OF_ANDROS
|COUNTY_COURT_OF_ERMOUPOLI
|COUNTY_COURT_OF_MILOS
|COUNTY_COURT_OF_MYKONOS
|COUNTY_COURT_OF_PAROS
|COUNTY_COURT_OF_TINOS
|COUNTY_COURT_OF_SAMOS
|COUNTY_COURT_OF_IKARIA
|COUNTY_COURT_OF_KARLOVASI
|COUNTY_COURT_OF_NAXOS
|COUNTY_COURT_OF_CHANIA
|COUNTY_COURT_OF_VAMOU
|COUNTY_COURT_OF_RETHYMNO
|COUNTY_COURT_OF_KOZANI
|COUNTY_COURT_OF_EORDAIA
|COUNTY_COURT_OF_GREVENA
|COUNTY_COURT_OF_KASTORIA
|COUNTY_COURT_OF_FLORINA
|COUNTY_COURT_OF_AMUNTAIO
|COUNTY_COURT_OF_LARISA
|COUNTY_COURT_OF_ELASSONAS
|COUNTY_COURT_OF_FARSALA
|COUNTY_COURT_OF_VOLOS
|COUNTY_COURT_OF_ALMIROS
|COUNTY_COURT_OF_SKOPELOS
|COUNTY_COURT_OF_KARDITSA
|COUNTY_COURT_OF_TRIKALA
|COUNTY_COURT_OF_KALAMPAKA
|COUNTY_COURT_OF_NAFPLIO
|COUNTY_COURT_OF_ASTROS
|COUNTY_COURT_OF_ARGOS
|COUNTY_COURT_OF_MASSITOS
|COUNTY_COURT_OF_THIRA
|COUNTY_COURT_OF_CORINTH
|COUNTY_COURT_OF_SIKIONOS
|COUNTY_COURT_OF_NEMEA
|COUNTY_COURT_OF_XYLOKASTRO
|COUNTY_COURT_OF_SPARTI
|COUNTY_COURT_OF_EPIDAVROS_LIMIRAS
|COUNTY_COURT_OF_TRIPOLI
|COUNTY_COURT_OF_MEGALOPOLI
|COUNTY_COURT_OF_PSOFIDA
|COUNTY_COURT_OF_KALAMATA
|COUNTY_COURT_OF_PILOS
|COUNTY_COURT_OF_KIPARISSIA
|COUNTY_COURT_OF_PLATAMODA
|COUNTY_COURT_OF_GYTHEIO
|COUNTY_COURT_OF_NEAPOLI_VOIWN
|COUNTY_COURT_OF_PATRAS
|COUNTY_COURT_OF_DIMI
|COUNTY_COURT_OF_AIGIALIA
|COUNTY_COURT_OF_KALAVRITA
|COUNTY_COURT_OF_AKRATA
|COUNTY_COURT_OF_PIRGOS
|COUNTY_COURT_OF_OLYMPIA
|COUNTY_COURT_OF_ARINI
|COUNTY_COURT_OF_AMALIADA
|COUNTY_COURT_OF_GASTOUNI
|COUNTY_COURT_OF_MYRTOUNTION
|COUNTY_COURT_OF_ZAKINTHOS
|COUNTY_COURT_OF_ARGOSTOLI
|COUNTY_COURT_OF_SAMEON
|COUNTY_COURT_OF_AGRINIO
|COUNTY_COURT_OF_VALTOS
|COUNTY_COURT_OF_LEFKADA
|COUNTY_COURT_OF_VONITSA
|COUNTY_COURT_OF_MESOLOGGI
|COUNTY_COURT_OF_NAFPAKTOS
|COUNTY_COURT_OF_MITILINI
|COUNTY_COURT_OF_KALLONI
|COUNTY_COURT_OF_CHIOS
|COUNTY_COURT_OF_HRAKLEIO
|COUNTY_COURT_OF_KASTELI
|COUNTY_COURT_OF_LASITHI
|COUNTY_COURT_OF_IERAPETRA
|COUNTY_COURT_OF_SITEIA
|COUNTY_COURT_OF_THIVA
|COUNTY_COURT_OF_CHALKIDA
|COUNTY_COURT_OF_ISTIAIA
|COUNTY_COURT_OF_KARYSTOS
|COUNTY_COURT_OF_KIMI
|COUNTY_COURT_OF_TAMINEON
|DISTRICT_COURT_OF_ATHENS
|DISTRICT_COURT_OF_LAMIA
|DISTRICT_COURT_OF_LIVADIA
|DISTRICT_COURT_OF_PIRAEUS
|DISTRICT_COURT_OF_THESSALONIKI
|DISTRICT_COURT_OF_VEROIA
|DISTRICT_COURT_OF_PIERIA
|DISTRICT_COURT_OF_SERRES
|DISTRICT_COURT_OF_CORFU
|DISTRICT_COURT_OF_KOMOTINI
|DISTRICT_COURT_OF_KAVALA
|DISTRICT_COURT_OF_DRAMA
|DISTRICT_COURT_OF_ARTA
|DISTRICT_COURT_OF_RODOS
|DISTRICT_COURT_OF_CHANIA
|DISTRICT_COURT_OF_RETHYMNO
|DISTRICT_COURT_OF_KOZANI
|DISTRICT_COURT_OF_KLEISOURA
|DISTRICT_COURT_OF_LARISA
|DISTRICT_COURT_OF_ELASSONAS
|DISTRICT_COURT_OF_VOLOS
|DISTRICT_COURT_OF_KARDITSA
|DISTRICT_COURT_OF_TRIKALA
|DISTRICT_COURT_OF_NAFPLIO
|DISTRICT_COURT_OF_ARGOS
|DISTRICT_COURT_OF_CORINTH
|DISTRICT_COURT_OF_SIKIONOS
|DISTRICT_COURT_OF_SPARTI
|DISTRICT_COURT_OF_TRIPOLI
|DISTRICT_COURT_OF_KALAMATA
|DISTRICT_COURT_OF_PATRAS
|DISTRICT_COURT_OF_AIGIALIA
|DISTRICT_COURT_OF_PIRGOS
|DISTRICT_COURT_OF_AMALIADA
|DISTRICT_COURT_OF_AGRINIO
|DISTRICT_COURT_OF_VALTOS
|DISTRICT_COURT_OF_MESOLOGGI
|DISTRICT_COURT_OF_MITILINI
|DISTRICT_COURT_OF_LIMNOS
|DISTRICT_COURT_OF_PLOMARI
|DISTRICT_COURT_OF_HRAKLEIO
|DISTRICT_COURT_OF_MOIRES
|DISTRICT_COURT_OF_PIRGOS_KRITIS
|DISTRICT_COURT_OF_THIVA
|DISTRICT_COURT_OF_CHALKIDA

;

/*
dikastirio :
    ste |
    supremeCourt |
    superiorSpecialCourt |
    magistrateCourtThessaloniki |
    magistrateCourtLamia |
    magistrateCourtPiraeus |
    magistrateCourtAthens |
    appelateCourtAthens |
    appelateCourtLamia |
    appelateCourtPiraeus |
    appelateCourtThessaloniki |
    appelateCourtCorfu |
    appelateCourtThraki |
    appelateCourtIoannina |
    appelateCourtDodekanisa |
    appelateCourtAegean |
    appelateCourtCrete |
    appelateCourtWestMacedonia |
    appelateCourtLarisa |
    appelateCourtNafplio |
    appelateCourtPatras |
    appelateCourtWestStereas |
    appelateCourtNorthAegean |
    appelateCourtEastCrete |
    appelateCourtKalamata |
    appelateCourtEvoia |
    firstInstanceCourtAthens |
    firstInstanceCourtLamia |
    firstInstanceCourtAmfissa |
    firstInstanceCourtEvritania |
    firstInstanceCourtLivadia |
    firstInstanceCourtPiraeus |
    firstInstanceCourtThessaloniki |
    firstInstanceCourtVeroia |
    firstInstanceCourtEdessa |
    firstInstanceCourtKaterini |
    firstInstanceCourtKilkis |
    firstInstanceCourtSerres |
    firstInstanceCourtXalkidiki |
    firstInstanceCourtCorfu |
    firstInstanceCourtGiannitsa |
    firstInstanceCourtThesprwtia |
    firstInstanceCourtRodopi |
    firstInstanceCourtDrama |
    firstInstanceCourtEvros|
    firstInstanceCourtKavala |
    firstInstanceCourtXanthi |
    firstInstanceCourtOrestiada|
    firstInstanceCourtIoannina |
    firstInstanceCourtArta |
    firstInstanceCourtPreveza |
    firstInstanceCourtRodos |
    firstInstanceCourtKos |
    firstInstanceCourtSyros |
    firstInstanceCourtSamos |
    firstInstanceCourtNaxos |
    firstInstanceCourtChania |
    firstInstanceCourtRethymno |
    firstInstanceCourtKozani |
    firstInstanceCourtGrevena |
    firstInstanceCourtKastoria |
    firstInstanceCourtFlorina |
    firstInstanceCourtLarisa |
    firstInstanceCourtVolos |
    firstInstanceCourtKarditsa |
    firstInstanceCourtTrikala |
    firstInstanceCourtNafplio |
    firstInstanceCourtCorinth |
    firstInstanceCourtSparti |
    firstInstanceCourtTripoli |
    firstInstanceCourtKalamata |
    firstInstanceCourtKiparissia |
    firstInstanceCourtGytheio |
    firstInstanceCourtPatras |
    firstInstanceCourtAigio |
    firstInstanceCourtKalavrita |
    firstInstanceCourtHleias |
    firstInstanceCourtAmaliada |
    firstInstanceCourtZakinthos |
    firstInstanceCourtKefallonia |
    firstInstanceCourtAgrinio |
    firstInstanceCourtLefkada |
    firstInstanceCourtMesologgi |
    firstInstanceCourtMitilini |
    firstInstanceCourtChios |
    firstInstanceCourtHrakleio |
    firstInstanceCourtLasithi |
    firstInstanceCourtThiva |
    firstInstanceCourtChalkida |
    countyCourtAthens |
    countyCourtMaroussi |
    countyCourtAxarnon |
    countyCourtElefsina |
    countyCourtKallithea |
    countyCourtKropia |
    countyCourtLavrio |
    countyCourtNeasIonias |
    countyCourtNeaLiosia |
    countyCourtMarathona |
    countyCourtMegara |
    countyCourtPeristeri |
    countyCourtChalandri |
    countyCourtLamia |
    countyCourtAtalanti |
    countyCourtAmfissa |
    countyCourtEvritania |
    countyCourtLivadia |
    countyCourtAigina |
    countyCourtKalavria |
    countyCourtKithira |
    countyCourtNikaias |
    countyCourtSalamina |
    countyCourtSpetses |
    countyCourtThessaloniki |
    countyCourtPiraeus |
    countyCourtVasilikon |
    countyCourtKoufalion |
    countyCourtLagkada |
    countyCourtAlexandria |
    countyCourtNaousa |
    countyCourtEdessa |
    countyCourtAlmopia |
    countyCourtSkydra |
    countyCourtPieria |
    countyCourtKolindrou |
    countyCourtPolikastro |
    countyCourtSerres |
    countyCourtNigrita |
    countyCourtRodolivon |
    countyCourtSintikis |
    countyCourtPoligirou |
    countyCourtArnaia |
    countyCourtKassandra |
    countyCourtNeaMoudania |
    countyCourtCorfu |
    countyCourtIgoumenitsa |
    countyCourtKomotini |
    countyCourtDrama |
    countyCourtThasos |
    countyCourtPaggaiou |
    countyCourtOrestiada|
    countyCourtAlexandroupoli |
    countyCourtKavala |
    countyCourtDidimoteixo |
    countyCourtIoannina |
    countyCourtKonitsa |
    countyCourtArta |
    countyCourtPreveza |
    countyCourtRodos |
    countyCourtKarpathos |
    countyCourtKalimnos |
    countyCourtKos |
    countyCourtLeros |
    countyCourtAndros |
    countyCourtErmoupoli |
    countyCourtMilos |
    countyCourtMykonos |
    countyCourtParos |
    countyCourtTinos |
    countyCourtSamos |
    countyCourtIkaria |
    countyCourtKarlovasi |
    countyCourtNaxos |
    countyCourtChania |
    countyCourtVamos |
    countyCourtRethymno |
    countyCourtKozani |
    countyCourtEordaia |
    countyCourtGrevena |
    countyCourtKastoria |
    countyCourtFlorina |
    countyCourtAmuntaio |
    countyCourtLarisa |
    countyCourtElassona |
    countyCourtFarsala |
    countyCourtVolos |
    countyCourtAlmiros |
    countyCourtSkopelos |
    countyCourtKarditsa |
    countyCourtTrikala |
    countyCourtKalampaka |
    countyCourtNafplio |
    countyCourtAstros |
    countyCourtArgos |
    countyCourtMassitos |
    countyCourtThira |
    countyCourtCorinth |
    countyCourtSikionos |
    countyCourtNemea |
    countyCourtXylokastro |
    countyCourtSparti |
    countyCourtEpidavrosLimiras |
    countyCourtTripoli |
    countyCourtMegalopoli |
    countyCourtPsofida |
    countyCourtKalamata |
    countyCourtPilos |
    countyCourtKiparissia |
    countyCourtPlatamoda |
    countyCourtGytheio |
    countyCourtNeapoliVoiwn |
    countyCourtPatras |
    countyCourtDimi |
    countyCourtAigialia |
    countyCourtKalavrita |
    countyCourtAkrata |
    countyCourtPirgos |
    countyCourtOlympia |
    countyCourtArini |
    countyCourtAmaliada |
    countyCourtGastouni |
    countyCourtMyrtountion |
    countyCourtZakinthos |
    countyCourtArgostoli |
    countyCourtSameon |
    countyCourtAgrinio |
    countyCourtValtos |
    countyCourtLefkada |
    countyCourtVonitsa |
    countyCourtMesologgi |
    countyCourtNafpaktos |
    countyCourtMitilini |
    countyCourtKalloni |
    countyCourtChios |
    countyCourtHrakleio |
    countyCourtKasteli |
    countyCourtLasithi |
    countyCourtIerapetra |
    countyCourtSiteia |
    countyCourtThiva |
    countyCourtChalkida |
    countyCourtIstiaia |
    countyCourtKarystos |
    countyCourtKimi |
    countyCourtTamineon |
    districtCourtAthens |
    districtCourtLamia |
    districtCourtLivadia |
    districtCourtPiraeus|
    districtCourtThessaloniki |
    districtCourtVeroia |
    districtCourtPieria |
    districtCourtSerres |
    districtCourtCorfu |
    districtCourtKomotini |
    districtCourtDrama|
    districtCourtKavala |
    districtCourtArta|
    districtCourtRodos |
    districtCourtChania |
    districtCourtRethymno |
    districtCourtKozani |
    districtCourtKleisoura |
    districtCourtLarisa |
    districtCourtElassona |
    districtCourtVolos |
    districtCourtKarditsa |
    districtCourtTrikala |
    districtCourtNafplio |
    districtCourtArgos |
    districtCourtCorinth |
    districtCourtSikionos |
    districtCourtSparti |
    districtCourtTripoli |
    districtCourtKalamata |
    districtCourtPatras |
    districtCourtAigialia |
    districtCourtPirgos |
    districtCourtAmaliada |
    districtCourtAgrinio |
    districtCourtValtos |
    districtCourtMesologgi |
    districtCourtMitilini |
    districtCourtLimnos |
    districtCourtPlomari |
    districtCourtHrakleio |
    districtCourtMoires |
    districtCourtPirgosCrete |
    districtCourtThiva |
    districtCourtChalkida //|
    //COURT
    ;

ste: OLOMELEIA? SPACE? STE SPACE? OLOMELEIA?;
supremeCourt: SUPREME_COURT;
superiorSpecialCourt: AED;
magistrateCourtThessaloniki: MAGISTRATE_COURT_OF_THESSALONIKI;
magistrateCourtLamia: MAGISTRATE_COURT_OF_LAMIA;
magistrateCourtPiraeus: MAGISTRATE_COURT_OF_PIRAEUS;
magistrateCourtAthens: MAGISTRATE_COURT_OF_ATHENS;
appelateCourtAthens: APELLATE_COURT_OF_ATHENS;
appelateCourtLamia: APELLATE_COURT_OF_LAMIA;
appelateCourtPiraeus: APELLATE_COURT_OF_PIRAEUS;
appelateCourtThessaloniki: APELLATE_COURT_OF_THESSALONIKI;
appelateCourtCorfu : APELLATE_COURT_OF_CORFU;
appelateCourtThraki : APELLATE_COURT_OF_THRAKI;
appelateCourtIoannina : APELLATE_COURT_OF_IOANNINA;
appelateCourtDodekanisa : APELLATE_COURT_OF_DODEKANISA;
appelateCourtAegean : APELLATE_COURT_OF_AEGEAN;
appelateCourtCrete : APELLATE_COURT_OF_CRETE;
appelateCourtWestMacedonia : APELLATE_COURT_OF_WEST_MACEDONIA;
appelateCourtLarisa : APELLATE_COURT_OF_LARISA;
appelateCourtNafplio : APELLATE_COURT_OF_NAFPLIO;
appelateCourtPatras: APELLATE_COURT_OF_PATRAS;
appelateCourtWestStereas: APELLATE_COURT_OF_WEST_STEREAS;
appelateCourtNorthAegean: APELLATE_COURT_OF_NORTH_AEGEAN;
appelateCourtEastCrete: APELLATE_COURT_OF_EAST_CRETE;
appelateCourtKalamata: APELLATE_COURT_OF_KALAMATA;
appelateCourtEvoia: APELLATE_COURT_OF_EVOIA;
firstInstanceCourtAthens: FIRST_INSTANCE_COURT_OF_ATHENS;
firstInstanceCourtLamia: FIRST_INSTANCE_COURT_OF_LAMIA;
firstInstanceCourtAmfissa: FIRST_INSTANCE_COURT_OF_AMFISSA;
firstInstanceCourtEvritania: FIRST_INSTANCE_COURT_OF_EVRITANIA;
firstInstanceCourtLivadia: FIRST_INSTANCE_COURT_OF_LIVADIA;
firstInstanceCourtPiraeus: FIRST_INSTANCE_COURT_OF_PIRAEUS;
firstInstanceCourtThessaloniki: FIRST_INSTANCE_COURT_OF_THESSALONIKI;
firstInstanceCourtVeroia: FIRST_INSTANCE_COURT_OF_VEROIA;
firstInstanceCourtEdessa: FIRST_INSTANCE_COURT_OF_EDESSA;
firstInstanceCourtKaterini: FIRST_INSTANCE_COURT_OF_KATERINI;
firstInstanceCourtKilkis: FIRST_INSTANCE_COURT_OF_KILKIS;
firstInstanceCourtSerres: FIRST_INSTANCE_COURT_OF_SERRES;
firstInstanceCourtXalkidiki: FIRST_INSTANCE_COURT_OF_XALKIDIKI;
firstInstanceCourtCorfu: FIRST_INSTANCE_COURT_OF_CORFU;
firstInstanceCourtGiannitsa: FIRST_INSTANCE_COURT_OF_GIANNITSA;
firstInstanceCourtThesprwtia: FIRST_INSTANCE_COURT_OF_THESPRWTIA;
firstInstanceCourtRodopi: FIRST_INSTANCE_COURT_OF_RODOPI;
firstInstanceCourtDrama: FIRST_INSTANCE_COURT_OF_DRAMA;
firstInstanceCourtEvros: FIRST_INSTANCE_COURT_OF_EVROS;
firstInstanceCourtKavala: FIRST_INSTANCE_COURT_OF_KAVALA;
firstInstanceCourtXanthi: FIRST_INSTANCE_COURT_OF_XANTHI;
firstInstanceCourtOrestiada: FIRST_INSTANCE_COURT_OF_ORESTIADA;
firstInstanceCourtIoannina: FIRST_INSTANCE_COURT_OF_IOANNINA;
firstInstanceCourtArta: FIRST_INSTANCE_COURT_OF_ARTA;
firstInstanceCourtPreveza: FIRST_INSTANCE_COURT_OF_PREVEZA;
firstInstanceCourtRodos: FIRST_INSTANCE_COURT_OF_RODOS;
firstInstanceCourtKos: FIRST_INSTANCE_COURT_OF_KOS;
firstInstanceCourtSyros: FIRST_INSTANCE_COURT_OF_SYROS;
firstInstanceCourtSamos: FIRST_INSTANCE_COURT_OF_SAMOS;
firstInstanceCourtNaxos: FIRST_INSTANCE_COURT_OF_NAXOS;
firstInstanceCourtChania: FIRST_INSTANCE_COURT_OF_CHANIA;
firstInstanceCourtRethymno: FIRST_INSTANCE_COURT_OF_RETHYMNO;
firstInstanceCourtKozani: FIRST_INSTANCE_COURT_OF_KOZANI;
firstInstanceCourtGrevena: FIRST_INSTANCE_COURT_OF_GREVENA;
firstInstanceCourtKastoria: FIRST_INSTANCE_COURT_OF_KASTORIA;
firstInstanceCourtFlorina: FIRST_INSTANCE_COURT_OF_FLORINA;
firstInstanceCourtLarisa: FIRST_INSTANCE_COURT_OF_LARISA;
firstInstanceCourtVolos: FIRST_INSTANCE_COURT_OF_VOLOS;
firstInstanceCourtKarditsa: FIRST_INSTANCE_COURT_OF_KARDITSA;
firstInstanceCourtTrikala: FIRST_INSTANCE_COURT_OF_TRIKALA;
firstInstanceCourtNafplio: FIRST_INSTANCE_COURT_OF_NAFPLIO;
firstInstanceCourtCorinth: FIRST_INSTANCE_COURT_OF_CORINTH;
firstInstanceCourtSparti: FIRST_INSTANCE_COURT_OF_SPARTI;
firstInstanceCourtTripoli: FIRST_INSTANCE_COURT_OF_TRIPOLI;
firstInstanceCourtKalamata: FIRST_INSTANCE_COURT_OF_KALAMATA;
firstInstanceCourtKiparissia: FIRST_INSTANCE_COURT_OF_KIPARISSIA;
firstInstanceCourtGytheio: FIRST_INSTANCE_COURT_OF_GYHTEIO;
firstInstanceCourtPatras: FIRST_INSTANCE_COURT_OF_PATRAS;
firstInstanceCourtAigio: FIRST_INSTANCE_COURT_OF_AIGIO;
firstInstanceCourtKalavrita: FIRST_INSTANCE_COURT_OF_KALAVRITA;
firstInstanceCourtHleias: FIRST_INSTANCE_COURT_OF_HLEIAS;
firstInstanceCourtAmaliada: FIRST_INSTANCE_COURT_OF_AMALIADA;
firstInstanceCourtZakinthos: FIRST_INSTANCE_COURT_OF_ZAKINTHOS;
firstInstanceCourtKefallonia: FIRST_INSTANCE_COURT_OF_KEFALLONIA;
firstInstanceCourtAgrinio: FIRST_INSTANCE_COURT_OF_AGRINIO;
firstInstanceCourtLefkada: FIRST_INSTANCE_COURT_OF_LEFKADA;
firstInstanceCourtMesologgi: FIRST_INSTANCE_COURT_OF_MESOLOGGI;
firstInstanceCourtMitilini: FIRST_INSTANCE_COURT_OF_MITILINI;
firstInstanceCourtChios: FIRST_INSTANCE_COURT_OF_CHIOS;
firstInstanceCourtHrakleio: FIRST_INSTANCE_COURT_OF_HRAKLEIO;
firstInstanceCourtLasithi: FIRST_INSTANCE_COURT_OF_LASITHI;
firstInstanceCourtThiva: FIRST_INSTANCE_COURT_OF_THIVA;
firstInstanceCourtChalkida: FIRST_INSTANCE_COURT_OF_CHALKIDA;
countyCourtAthens: COUNTY_COURT_OF_ATHENS;
countyCourtMaroussi: COUNTY_COURT_OF_MAROUSSI;
countyCourtAxarnon: COUNTY_COURT_OF_AXARNON;
countyCourtElefsina: COUNTY_COURT_OF_ELEFSINA;
countyCourtKallithea: COUNTY_COURT_OF_KALLITHEA;
countyCourtKropia: COUNTY_COURT_OF_KROPIA;
countyCourtLavrio: COUNTY_COURT_OF_LAVRIO;
countyCourtNeasIonias: COUNTY_COURT_OF_NEAS_IONIAS;
countyCourtNeaLiosia: COUNTY_COURT_OF_NEA_LIOSIA;
countyCourtMarathona: COUNTY_COURT_OF_MARATHONA;
countyCourtMegara: COUNTY_COURT_OF_MEGARA;
countyCourtPeristeri: COUNTY_COURT_OF_PERISTERI;
countyCourtChalandri: COUNTY_COURT_OF_CHALANDRI;
countyCourtLamia: COUNTY_COURT_OF_LAMIA;
countyCourtAtalanti: COUNTY_COURT_OF_ATALANTI;
countyCourtAmfissa: COUNTY_COURT_OF_AMFISSA;
countyCourtEvritania: COUNTY_COURT_OF_EVRITANIA;
countyCourtLivadia: COUNTY_COURT_OF_LIVADIA;
countyCourtAigina: COUNTY_COURT_OF_AIGINA;
countyCourtKalavria: COUNTY_COURT_OF_KALAVRIA;
countyCourtKithira: COUNTY_COURT_OF_KITHIRA;
countyCourtNikaias: COUNTY_COURT_OF_NIKAIAS;
countyCourtSalamina: COUNTY_COURT_OF_SALAMINA;
countyCourtSpetses: COUNTY_COURT_OF_SPETSES;
countyCourtThessaloniki: COUNTY_COURT_OF_THESSALONIKI;
countyCourtPiraeus: COUNTY_COURT_OF_PIRAEUS;
countyCourtVasilikon: COUNTY_COURT_OF_VASILIKON;
countyCourtKoufalion: COUNTY_COURT_OF_KOUFALION;
countyCourtLagkada: COUNTY_COURT_OF_LAGKADA;
countyCourtAlexandria: COUNTY_COURT_OF_ALEXANDRIA;
countyCourtNaousa: COUNTY_COURT_OF_NAOUSA;
countyCourtEdessa: COUNTY_COURT_OF_EDESSA;
countyCourtAlmopia: COUNTY_COURT_OF_ALMOPIA;
countyCourtSkydra: COUNTY_COURT_OF_SKYDRA;
countyCourtPieria: COUNTY_COURT_OF_PIERIA;
countyCourtKolindrou: COUNTY_COURT_OF_KOLINDROU;
countyCourtPolikastro: COUNTY_COURT_OF_POLIKASTRO;
countyCourtSerres: COUNTY_COURT_OF_SERRES;
countyCourtNigrita: COUNTY_COURT_OF_NIGRITA;
countyCourtRodolivon: COUNTY_COURT_OF_RODOLIVON;
countyCourtSintikis: COUNTY_COURT_OF_SINTIKIS;
countyCourtPoligirou: COUNTY_COURT_OF_POLIGIROU;
countyCourtArnaia: COUNTY_COURT_OF_ARNAIA;
countyCourtKassandra: COUNTY_COURT_OF_KASSANDRA;
countyCourtNeaMoudania: COUNTY_COURT_OF_NEA_MOUDANIA;
countyCourtCorfu: COUNTY_COURT_OF_CORFU;
countyCourtIgoumenitsa: COUNTY_COURT_OF_IGOUMENITSA;
countyCourtKomotini: COUNTY_COURT_OF_KOMOTINI;
countyCourtDrama: COUNTY_COURT_OF_DRAMA;
countyCourtThasos: COUNTY_COURT_OF_THASOS;
countyCourtPaggaiou: COUNTY_COURT_OF_PAGGAIOU;
countyCourtOrestiada: COUNTY_COURT_OF_ORESTIADA;
countyCourtAlexandroupoli: COUNTY_COURT_OF_ALEXANDROUPOLI;
countyCourtKavala: COUNTY_COURT_OF_KAVALA;
countyCourtDidimoteixo: COUNTY_COURT_OF_DIDIMOTEIXO;
countyCourtIoannina: COUNTY_COURT_OF_IOANNINA;
countyCourtKonitsa: COUNTY_COURT_OF_KONITSA;
countyCourtArta: COUNTY_COURT_OF_ARTA;
countyCourtPreveza: COUNTY_COURT_OF_PREVEZA;
countyCourtRodos: COUNTY_COURT_OF_RODOS;
countyCourtKarpathos: COUNTY_COURT_OF_KARPATHOS;
countyCourtKalimnos: COUNTY_COURT_OF_KALIMNOS;
countyCourtKos: COUNTY_COURT_OF_KOS;
countyCourtLeros: COUNTY_COURT_OF_LEROS;
countyCourtAndros: COUNTY_COURT_OF_ANDROS;
countyCourtErmoupoli: COUNTY_COURT_OF_ERMOUPOLI;
countyCourtMilos: COUNTY_COURT_OF_MILOS;
countyCourtMykonos: COUNTY_COURT_OF_MYKONOS;
countyCourtParos: COUNTY_COURT_OF_PAROS;
countyCourtTinos: COUNTY_COURT_OF_TINOS;
countyCourtSamos: COUNTY_COURT_OF_SAMOS;
countyCourtIkaria: COUNTY_COURT_OF_IKARIA;
countyCourtKarlovasi: COUNTY_COURT_OF_KARLOVASI;
countyCourtNaxos: COUNTY_COURT_OF_NAXOS;
countyCourtChania: COUNTY_COURT_OF_CHANIA;
countyCourtVamos: COUNTY_COURT_OF_VAMOU;
countyCourtRethymno: COUNTY_COURT_OF_RETHYMNO;
countyCourtKozani: COUNTY_COURT_OF_KOZANI;
countyCourtEordaia: COUNTY_COURT_OF_EORDAIA;
countyCourtGrevena: COUNTY_COURT_OF_GREVENA;
countyCourtKastoria: COUNTY_COURT_OF_KASTORIA;
countyCourtFlorina: COUNTY_COURT_OF_FLORINA;
countyCourtAmuntaio: COUNTY_COURT_OF_AMUNTAIO;
countyCourtLarisa: COUNTY_COURT_OF_LARISA;
countyCourtElassona: COUNTY_COURT_OF_ELASSONAS;
countyCourtFarsala: COUNTY_COURT_OF_FARSALA;
countyCourtVolos: COUNTY_COURT_OF_VOLOS;
countyCourtAlmiros: COUNTY_COURT_OF_ALMIROS;
countyCourtSkopelos: COUNTY_COURT_OF_SKOPELOS;
countyCourtKarditsa: COUNTY_COURT_OF_KARDITSA;
countyCourtTrikala: COUNTY_COURT_OF_TRIKALA;
countyCourtKalampaka: COUNTY_COURT_OF_KALAMPAKA;
countyCourtNafplio: COUNTY_COURT_OF_NAFPLIO;
countyCourtAstros: COUNTY_COURT_OF_ASTROS;
countyCourtArgos: COUNTY_COURT_OF_ARGOS;
countyCourtMassitos: COUNTY_COURT_OF_MASSITOS;
countyCourtThira: COUNTY_COURT_OF_THIRA;
countyCourtCorinth: COUNTY_COURT_OF_CORINTH;
countyCourtSikionos: COUNTY_COURT_OF_SIKIONOS;
countyCourtNemea: COUNTY_COURT_OF_NEMEA;
countyCourtXylokastro: COUNTY_COURT_OF_XYLOKASTRO;
countyCourtSparti: COUNTY_COURT_OF_SPARTI;
countyCourtEpidavrosLimiras: COUNTY_COURT_OF_EPIDAVROS_LIMIRAS;
countyCourtTripoli: COUNTY_COURT_OF_TRIPOLI;
countyCourtMegalopoli: COUNTY_COURT_OF_MEGALOPOLI;
countyCourtPsofida: COUNTY_COURT_OF_PSOFIDA;
countyCourtKalamata: COUNTY_COURT_OF_KALAMATA;
countyCourtPilos: COUNTY_COURT_OF_PILOS;
countyCourtKiparissia: COUNTY_COURT_OF_KIPARISSIA;
countyCourtPlatamoda: COUNTY_COURT_OF_PLATAMODA;
countyCourtGytheio: COUNTY_COURT_OF_GYTHEIO;
countyCourtNeapoliVoiwn: COUNTY_COURT_OF_NEAPOLI_VOIWN;
countyCourtPatras: COUNTY_COURT_OF_PATRAS;
countyCourtDimi: COUNTY_COURT_OF_DIMI;
countyCourtAigialia: COUNTY_COURT_OF_AIGIALIA;
countyCourtKalavrita: COUNTY_COURT_OF_KALAVRITA;
countyCourtAkrata: COUNTY_COURT_OF_AKRATA;
countyCourtPirgos: COUNTY_COURT_OF_PIRGOS;
countyCourtOlympia: COUNTY_COURT_OF_OLYMPIA;
countyCourtArini: COUNTY_COURT_OF_ARINI;
countyCourtAmaliada: COUNTY_COURT_OF_AMALIADA;
countyCourtGastouni: COUNTY_COURT_OF_GASTOUNI;
countyCourtMyrtountion: COUNTY_COURT_OF_MYRTOUNTION;
countyCourtZakinthos: COUNTY_COURT_OF_ZAKINTHOS;
countyCourtArgostoli: COUNTY_COURT_OF_ARGOSTOLI;
countyCourtSameon: COUNTY_COURT_OF_SAMEON;
countyCourtAgrinio: COUNTY_COURT_OF_AGRINIO;
countyCourtValtos: COUNTY_COURT_OF_VALTOS;
countyCourtLefkada: COUNTY_COURT_OF_LEFKADA;
countyCourtVonitsa: COUNTY_COURT_OF_VONITSA;
countyCourtMesologgi: COUNTY_COURT_OF_MESOLOGGI;
countyCourtNafpaktos: COUNTY_COURT_OF_NAFPAKTOS;
countyCourtMitilini: COUNTY_COURT_OF_MITILINI;
countyCourtKalloni: COUNTY_COURT_OF_KALLONI;
countyCourtChios: COUNTY_COURT_OF_CHIOS;
countyCourtHrakleio: COUNTY_COURT_OF_HRAKLEIO;
countyCourtKasteli: COUNTY_COURT_OF_KASTELI;
countyCourtLasithi: COUNTY_COURT_OF_LASITHI;
countyCourtIerapetra: COUNTY_COURT_OF_IERAPETRA;
countyCourtSiteia: COUNTY_COURT_OF_SITEIA;
countyCourtThiva: COUNTY_COURT_OF_THIVA;
countyCourtChalkida: COUNTY_COURT_OF_CHALKIDA;
countyCourtIstiaia: COUNTY_COURT_OF_ISTIAIA;
countyCourtKarystos: COUNTY_COURT_OF_KARYSTOS;
countyCourtKimi: COUNTY_COURT_OF_KIMI;
countyCourtTamineon: COUNTY_COURT_OF_TAMINEON;
districtCourtAthens: DISTRICT_COURT_OF_ATHENS;
districtCourtLamia: DISTRICT_COURT_OF_LAMIA;
districtCourtLivadia: DISTRICT_COURT_OF_LIVADIA;
districtCourtPiraeus: DISTRICT_COURT_OF_PIRAEUS;
districtCourtThessaloniki: DISTRICT_COURT_OF_THESSALONIKI;
districtCourtVeroia: DISTRICT_COURT_OF_VEROIA;
districtCourtPieria: DISTRICT_COURT_OF_PIERIA;
districtCourtSerres: DISTRICT_COURT_OF_SERRES;
districtCourtCorfu: DISTRICT_COURT_OF_CORFU;
districtCourtKomotini: DISTRICT_COURT_OF_KOMOTINI;
districtCourtKavala: DISTRICT_COURT_OF_KAVALA;
districtCourtDrama: DISTRICT_COURT_OF_DRAMA;
districtCourtArta: DISTRICT_COURT_OF_ARTA;
districtCourtRodos: DISTRICT_COURT_OF_RODOS;
districtCourtChania: DISTRICT_COURT_OF_CHANIA;
districtCourtRethymno: DISTRICT_COURT_OF_RETHYMNO;
districtCourtKozani: DISTRICT_COURT_OF_KOZANI;
districtCourtKleisoura: DISTRICT_COURT_OF_KLEISOURA;
districtCourtLarisa: DISTRICT_COURT_OF_LARISA;
districtCourtElassona: DISTRICT_COURT_OF_ELASSONAS;
districtCourtVolos: DISTRICT_COURT_OF_VOLOS;
districtCourtKarditsa: DISTRICT_COURT_OF_KARDITSA;
districtCourtTrikala: DISTRICT_COURT_OF_TRIKALA;
districtCourtNafplio: DISTRICT_COURT_OF_NAFPLIO;
districtCourtArgos: DISTRICT_COURT_OF_ARGOS;
districtCourtCorinth: DISTRICT_COURT_OF_CORINTH;
districtCourtSikionos: DISTRICT_COURT_OF_SIKIONOS;
districtCourtSparti: DISTRICT_COURT_OF_SPARTI;
districtCourtTripoli: DISTRICT_COURT_OF_TRIPOLI;
districtCourtKalamata: DISTRICT_COURT_OF_KALAMATA;
districtCourtPatras: DISTRICT_COURT_OF_PATRAS;
districtCourtAigialia: DISTRICT_COURT_OF_AIGIALIA;
districtCourtPirgos: DISTRICT_COURT_OF_PIRGOS;
districtCourtAmaliada: DISTRICT_COURT_OF_AMALIADA;
districtCourtAgrinio: DISTRICT_COURT_OF_AGRINIO;
districtCourtValtos: DISTRICT_COURT_OF_VALTOS;
districtCourtMesologgi: DISTRICT_COURT_OF_MESOLOGGI;
districtCourtMitilini: DISTRICT_COURT_OF_MITILINI;
districtCourtLimnos: DISTRICT_COURT_OF_LIMNOS;
districtCourtPlomari: DISTRICT_COURT_OF_PLOMARI;
districtCourtHrakleio: DISTRICT_COURT_OF_HRAKLEIO;
districtCourtMoires: DISTRICT_COURT_OF_MOIRES;
districtCourtPirgosCrete: DISTRICT_COURT_OF_PIRGOS_KRITIS;
districtCourtThiva: DISTRICT_COURT_OF_THIVA;
districtCourtChalkida: DISTRICT_COURT_OF_CHALKIDA;
*/

//implicitCourt: OF SPACE special SPACE COURT;
implicitCourt: OF SPACE special SPACE COURT_TEXT;
//ministries : MINISTRIES;
//sxetiko: SXETIKO_TEXT;
parartima : PARARTIMA_TEXT;
btrimeles : BT;

//----------------------LEXER -- TOKENS-----------------------------------//
//FEK: BRACKET FEK_REF BRACKET;
//MINISTRIES : (OF SPACE (ALL_CHARS SPACE)* OF? SPACE?)? GREEK_MINISTRY;
//FOREAS : (OF SPACE (ALL_CHARS SPACE)* OF? SPACE?)? FOREIS;
NSK : (OLOMELEIA SPACE)? (OF SPACE OF? SPACE?)? NOMIKO_SYMB_KRATOUS;
//COURT : GREEK_COURTS;
COURT_TEXT : 'Δικαστηρίου' | 'δικαστηρίου';
//COURT : (OF SPACE (ALL_CHARS SPACE)* OF? SPACE?)? GREEK_COURTS;
//ADA_TEXT : 'ΑΔΑ';

OLOMELEIA : 'Ολ.' | 'Ολ' | 'Ολομ.' | 'της Ολομέλειας';
MELI : NUM ('μελούς'| 'μ.') | 'επταμ.' | 'επταμ' | 'επτ.' ;
//Θέλει συμπλήρωση!!
IONIKO_SYSTEM : ('α' | 'β' | 'γ' | 'δ' | 'ε' | 'στ' | 'ζ' | 'η' | 'θ' | 'ι' | 'ια' |
    'ιβ' | 'ιγ' | 'ιδ' | 'ιε' | 'ιστ' | 'ιζ' | 'ιη' | 'ιθ' | 'κα' | 'κβ' | 'κγ' |
    'κδ' | 'κε' | 'κστ' | 'κζ' | 'κη' | 'κθ' | 'Α' | 'Β' | 'Γ' |
    '∆' | 'Δ' | 'Ε' | 'ΣΤ' | 'Ζ' | 'Η' | 'Θ' | 'Ι' | 'ΙΑ' | 'ΙΒ' | 'ΙΓ' |
     'ΙΔ' | 'ΙΕ' | 'ΙΣΤ' | 'ΙΖ' | 'ΙΗ' | 'ΙΘ' | 'ΚΑ' | 'ΚΒ' | 'ΚΓ' |
     'ΚΔ' | 'ΚΕ' | 'ΚΣΤ' | 'ΚΖ' | 'ΚΗ' | 'ΚΘ') APOSTROPHE?; //θελει και τα κεφαλαία!

//Θέλει συμπλήρωση!!
LEKTIKO_ID:
    'πρώτο' | 'πρώτου' | 'πρώτη' | 'πρώτης' |
    'δεύτερο' | 'δεύτερου' | 'δεύτερη' | 'δεύτερης' |
    'τρίτο' | 'τρίτης' | 'τρίτου' | 'τρίτη' |
    'τέταρτο' | 'τετάρτου' | 'τέταρτης' | 'τέταρτη' |
    'πέμπτο' | 'πέμπτης' | 'πέμπτου' | 'πέμπτη' |
    'έκτο' | 'έκτου' | 'έκτης' | 'έκτη' |
    'έβδομο' | 'έβδομη' | 'εβδόμου' | 'έβδομης' |
    'όγδοο' | 'όγδοου' | 'όγδοη' | 'όγδοης' |
    'ένατο' | 'ένατη' | 'ένατου' | 'ένατης' |
    'τελευταίο' | 'τελ.' | 'τελευταίας' |
    'μόνου'
    ;

LATIN_ID : ('I' | 'ΙΙ' | 'III' | 'IV' | 'V' | 'VI' | 'VII' | 'VIII' | 'IX');
WITH : 'με την';
SINCE : 'καθώς';
NEXT_ALL: 'επ.' | 'επομ.';
NUM : [0-9]+ ;
HYPHEN: ('-' | '–' | '−');
SLASH : '/' | '|'; // το [|] χρησιμοποιείται σε αποφάσεις αρείου Πάγου (1997 κ.α.)
COMMA: ',' | '‚';
DOT:'.';
COLON: ':';
BACKSLASH : '\\';
BRACKET: ('(' | '[' | ')' | ']');
APOSTROPHE : [’΄'`ʹ];
OF : ('του' | 'της') ;
AND : 'και' | '&';
RANGE : ('έως' (SPACE AND)?);

/*KYA :
    'Κ.Υ.Α.' |
    'κοινής' SPACE 'υπουργικής' SPACE 'απόφασης' |
    'Κοινή' SPACE 'Απόφαση' SPACE 'Υπουργών'|
    'Κοινής Υπουργικής Απόφασης'
    ;
*/
/*EGKYKLIOS_TEXT :
    'εγκύκλιός' |
    'εγκύκλιος' |
    'εγκυκλίου' |
    'εγκύκλιο' |
    'Αρ. Εγκυκλίου' |
    'Εγκύκλιος'
    ;
*/

//PROTOCOL_TEXT:
//    (('αρ.' | 'αριθ.') SPACE)? 'πρωτ.'
//    ;

//SXETIKO_TEXT : (OF | 'το') SPACE BRACKET IONIKO_SYSTEM BRACKET SPACE ('σχετικού' | 'σχετικό' | 'όμοιου');
BT : 'ΒΤ' | 'Β.Τ.';
//PAD : 'ΠαΔ';

ACTS:
    'Ν.' | 'Ν' |
    'ν.' | 'ν'|
    'νόμου' |
    'νόµου' |
    'νόμος'|
    'νόμο' |
    'νόμων'
    ;

ROYAL_DECREE:
    'β.' SPACE? 'δ.' |
    'Β.Δ.' | 'ΒΔ'
    ;

COMPULSORY_LAW:
    'Α'[.]?'Ν'[.]? |
    'α.ν.' |
    'αν.' (SPACE? 'ν.')?
    ;

DECREE_LAW:
    'Ν'[.]?'Δ'[.]? |
    'ν'[.]?'δ'[.]? |
    'Ν∆' |
    'ν.' SPACE? 'δ/τος' |
    'Ν.' SPACE? 'Δ/τος' |
    'νομοθετικού διατάγματος' |
    'νομοθετικό διάταγμα' |
    'Ν .Δ.' |
    'N.Δ.'
    ;

PRESIDENTIAL_DECREE:
    'π.δ.' | 'π.δ' |
    'Π.' SPACE* 'Δ/τος' |
    'Π.Δ.' | 'Π.∆.'| 'ΠΔ.' |
    'Π∆' | 'ΠΔ' |
    'π.δ/τος' |
    'Π/Δτος'
    ;

DECREE: 'δ/τος' | 'Διατάγματος';

SYNTAGMA :
    'Συντάγματος' |
    'Σύνταγμα'
    ;

KWDIKAS_TEXT : ('Κώδικα' | 'κώδικα');
KWDIKAS_FOROLOGIKIS_DIADIKASIAS : 'Κώδικα' SPACE 'Φορολογικής' SPACE 'Διαδικασίας' | 'ΚΦΔ';
YPALLILIKOS_KWDIKAS : ('Υπαλληλικού' | 'Υπαλληλικό') SPACE 'Κώδικα' | 'ΥΚ' | ~('E')~('.')'Υ.Κ.' ;
AGROTIKOS_KWDIKAS : 'Αγροτικού' SPACE 'Κώδικα' | 'ΑΓΡΚ' ;
ALIEUTIKOS_KWDIKAS : 'Αλιευτικού' SPACE 'Κώδικα';
ASTIKOS_KWDIKAS : 'ΑΚ' | 'Α.Κ.'| ([αΑ]'στικό'[ς]? | 'Αστικού')  SPACE ('Κώδικα' | 'Κώδικας');
AGORANOMIKOS_KWDIKAS : 'Αγορανομικού' SPACE 'Κώδικα';
GENIKOS_OIKODOMIKOS_KANONISMOS : 'ΓΟΚ' | 'Γ.Ο.Κ.' | 'Γενικού' SPACE 'Οικοδομικού' SPACE 'Κανονισμού';
NEOS_OIKODOMIKOS_KANONISMOS: 'Νέου' SPACE 'Οικοδομικού' SPACE 'Κανονισμού' | 'ΝΟΚ' | 'Ν.Ο.Κ.';
KWDIKAS_ADEIWN_FORTIGWN_AUTOKINITWN : 'Κώδικα' SPACE 'Αδειών' SPACE 'Φορτηγών' SPACE 'Αυτοκινήτων' | 'ΚΑΦΑ' | 'Κ.Α.Φ.Α.';
KWDIKAS_APODIMIAS_METANASTEUSIS_DIAVATIRIA: 'Κώδικα' SPACE 'Αποδημίας' SPACE 'Μετανάστευσης' SPACE 'και' SPACE 'Διαβατηρίων';
KWDIKAS_DEONTOLOGIAS_DIKIGORIKOU_LEITOURGIMATOS : 'ΚΔΔΛ' | 'Κ.Δ.Δ.Λ.' | 'Κώδικα' SPACE 'Δεοντολογίας' SPACE 'Δικηγορικού' SPACE 'Λειτουργήματος';
KWDIKAS_DIATAGMATWN_GIA_DIMOTOLOGIA : 'Κώδικα' SPACE 'Διαταγμάτων' SPACE 'για' SPACE 'τα' SPACE 'Δημοτολόγια';
KWDIKAS_DIATAKSEWN_STRATOLOGIKIS_FISIS : 'Κώδικα' SPACE 'Διατάξεων' SPACE 'Στρατολογικής' SPACE 'Φύσης';
KWDIKAS_ELLINIKIS_ITHAGENEIAS : 'Κώδικα' SPACE 'Ελληνικής' SPACE 'Ιθαγένειας';
KWDIKAS_ESODWN_DIMWN_KAI_KOINOTITWN : 'Κώδικα' SPACE 'Εσόδων' SPACE 'Δήμων' SPACE 'και' SPACE 'Κοινοτήτων';
DASIKOS_KWDIKAS : 'Δασικός' SPACE 'Κώδικας' | 'Δασικού' SPACE 'Κώδικα';
KWDIKAS_AEROPORIKOY_DIKAIOY : 'Κώδικα' SPACE 'Αεροπορικού' SPACE 'Δικαίου' ;
KWDIKAS_KATASKEUIS_DIMOSIWN_ERGWN : 'Κώδικα' SPACE 'Κατασκευής' SPACE 'Δημοσίων' SPACE 'Έργων';
KWDIKAS_NOMOTHESIAS_KUVERNISIS : 'Κώδικα' SPACE 'Νομοθεσίας' SPACE 'Κυβέρνησης';
KWDIKAS_NOMWN_GIA_NARKWTIKA : 'Κώδικα' SPACE 'Νόμων' SPACE 'για' SPACE 'τα' SPACE 'Ναρκωτικά' | 'Κ.Ν.Ν.';
KWDIKAS_PAROXIS_EPENDITIKWN_KINITRWN : 'Κώδικα' SPACE 'Παροχής' SPACE 'Επενδυτικών' SPACE 'Κινήτρων';
KWDIKAS_PERI_ARXAIOTITWN : 'Κώδικα' SPACE 'περί' SPACE 'Αρχαιοτήτων';
KWDIKAS_SYNALLAGWN_HLEKTRIKIS_ENERGEIAS : 'Κώδικα' SPACE 'Συναλλαγών' SPACE 'Ηλεκτρικής' SPACE 'Ενέργειας';
KWDIKAS_TAMEIOU_NOMIKWN : 'Κώδικα' SPACE 'Ταμείου' SPACE 'Νομικών';
KWDIKAS_TROFIMWN_KAI_POTWN : 'Κώδικα' SPACE 'Τροφίμων' SPACE 'και' SPACE 'Ποτών';
KWDIKAS_FOROLOGIAS_KAPNOU : 'Κώδικα' SPACE 'Φορολογίας' SPACE 'Καπνού' ;
KWDIKAS_FOROLOGIKWN_STOIXEIWN : 'Κ.Φ.Σ.';
KWDIKAS_ANAGK_APAL_AKINITWN : ('Κώδικα' | 'Κώδικας') SPACE 'Αναγκαστικών' SPACE 'Απαλλοτριώσεων' SPACE 'Ακινήτων';
KWDIKAS_BIBLIWN_KAI_STOIXEIWN : 'Κ.Β.Σ.' | 'Κώδικα' SPACE 'Βιβλίων' SPACE 'και' SPACE 'Στοιχείων';
KWDIKAS_POINIKIS_DIKONOMIAS : 'ΚΠΔ' | 'Κ.Π.Δ.' | 'ΚΠοινΔ' | 'Κ.Ποιν.Δ' | 'Κώδικα' SPACE 'Ποινικής' SPACE 'Δικονομίας';
POINIKOS_KWDIKAS : 'ΠΚ' | 'Π.Κ.' | 'Ποινικού' SPACE 'Κώδικα';
ETHNIKOS_TELWNIAKOS_KWDIKAS : ('Εθνικού' SPACE)? 'Τελωνειακού' SPACE 'Κώδικα';
KWDIKAS_FOROLOGIAS_EISODIMATOS : 'Κώδικα' SPACE 'Φορολογίας' SPACE 'Εισοδήματος' | 'Κ.Φ.Ε.' | 'ΚΦΕ';
KWDIKAS_BASIKIS_POLEODOMIKIS_NOMOTHESIAS : ('Κώδικα' | 'Κώδικας') SPACE 'Βασικής' SPACE 'Πολεοδομικής' SPACE 'Νομοθεσίας' | 'Κ.Β.Π.Ν.';
KTINOTROFIKOS_KWDIKAS : 'Κτηνοτροφικού' SPACE 'Κώδικα';
KWDIKAS_TELWN_XARTOSIMOU : 'Κ.Ν.Τ.Χ.' | 'Κώδικα' SPACE 'Τελών' SPACE 'Χαρτοσήμου';
KWDIKAS_BASIKWN_KANONWN_KRATOUMENWN : 'Κώδικα' SPACE 'Βασικών' SPACE 'Κανόνων' SPACE 'Κρατουμένων';
KWDIKAS_FOROLOGIKIS_DIKONOMIAS : 'Κώδικα' SPACE 'Φορολογικής' SPACE 'Δικονομίας' ;
KWDIKAS_DIKIGORWN: 'Κώδικα' SPACE 'περί' SPACE 'δικηγόρων' | 'Δικηγ. Κ.' | 'Κώδικα Δικηγόρων';
KWDIKAS_DIMOSIOU_LOGISTIKOU : 'Κώδικα' SPACE 'Δημόσιου' SPACE 'Λογιστικού' ;
KWDIKAS_DIMOSIOU_NAUTIKOU_DIKAIOU : 'Κώδικα' SPACE 'Δημόσιου' SPACE 'Ναυτικού' SPACE 'Δικαίου' | 'ΚΔΝΔ' | 'Κ.Δ.Ν.Δ.' ;
KWDIKAS_FOROY_PROSTITHEMENIS_AKSIAS : 'Κώδικα' SPACE 'Φ.Π.Α.' | 'Κώδικα' SPACE 'ΦΠΑ';
KWDIKAS_POLITIKIS_DIKONOMIAS: 'Κ'[.]?[Ππ]'ολ'[.]?'Δ'('ικ'[α]?|[.])? | 'Κ.Πολ.Δ.';
KWDIKAS_DHMWN_KAI_KOINOTITWN : ('Κώδικα' | 'Κώδικας') SPACE 'Δήμων' SPACE 'και' SPACE 'Κοινοτήτων';
KWDIKAS_ODIKIS_KYKLOFORIAS : ('Κώδικα' | 'Κώδικας') SPACE 'Οδικής' SPACE 'Κυκλοφορίας' | 'Κ.Ο.Κ.' ;
KWDIKAS_DIKASTIKOU_SWMATOS_ENOPLWN_DINAMEWN : 'Κώδικα' SPACE 'Δικαστικού' SPACE 'Σώματος' SPACE 'Ενόπλων' SPACE 'Δυνάμεων' | 'ΚΔΣΕΔ' | 'Κ.Δ.Σ.Ε.Δ.';
KWDIKAS_DIKASTIKWN_EPIMELITWN : 'Κώδικα' SPACE 'Δικαστικών' SPACE 'Επιμελητών';
KWDIKAS_ORGANISMOU_DIKASTIRIWN : 'Κώδικα' SPACE 'Οργανισμού' SPACE 'Δικαστηρίων';
KWDIKAS_DIKASTIKWN_YPALLHLWN : 'Κώδικα' SPACE 'Δικαστικών' SPACE 'Υπαλλήλων';
KWDIKAS_DIKWN_DIMOSIOU : 'Κώδικα' SPACE 'Δικών' SPACE 'Δημοσίου' | [Κκ]'ώδικα' SPACE 'περί' SPACE 'δικών' SPACE 'του' SPACE 'Δημοσίου';
KWDIKAS_DIOIKITIKIS_DIADIKASIAS : ('Κώδικα' | 'Κώδικας') SPACE 'Διοικητικής' SPACE 'Διαδικασίας' | 'Κώδικα' SPACE '∆ιοικ.' SPACE '∆ιαδικασίας' | 'Κ∆∆' | 'ΚΔΔ' | 'Κ.Δ.Δ.' | 'ΚΔΔιαδ.';
KWDIKAS_DIOIKITIKIS_DIKONOMIAS : 'Κώδικα' SPACE 'Διοικητικής' SPACE 'Δικονομίας';
KWDIKAS_EISPRAKSEWN_DHMOSIWN_ESODWN : 'Κώδικα' SPACE 'Εισπράξεων' SPACE 'Δημοσίων' SPACE 'Εσόδων' | 'ΚΕΔΕ' | 'Κ.Ε.Δ.Ε.';
KWDIKAS_FARMAKEUTIKIS_DEONTOLOGIAS : 'Κώδικα' SPACE 'Φαρμακευτικής' SPACE 'Δεοντολογίας';
KWDIKAS_IDIWTIKOU_NAUTIKOU_DIKAIOU : 'Κώδικα' SPACE 'Ιδιωτικού' SPACE 'Ναυτικού' SPACE 'Δικαίου';
KWDIKAS_POLEMIKWN_SYNTAKSEWN : 'Κώδικα' SPACE 'Πολεμικών' SPACE 'Συντάξεων' ;
KWDIKAS_POLITIKWN_KAI_STRATIWTIKWN_SUNTAKSEWN : 'Κώδικα' SPACE 'Πολιτικών' SPACE AND SPACE 'Στρατιωτικών' SPACE 'Συντάξεων';
KWDIKAS_METOXIKOU_TAMEIOU_POLITIKWN_YPALLHLWN : 'Κώδικα' SPACE 'Μετοχικού' SPACE 'Ταμείου' SPACE 'Πολιτικών' SPACE 'Υπαλλήλων' | 'ΚΜΤΠΥ';
KWDIKAS_METOXIKOU_TAMEIOU_STRATOU : 'Κώδικα' SPACE 'Μετοχικού' SPACE 'Ταμείου' SPACE 'Στρατού' | 'ΚΜΤΣ';
KWDIKAS_PROSOPIKOU_LIMENIKOU_SWMATOS : 'Κώδικα' SPACE 'Προσωπικού' SPACE 'Λιμενικού' SPACE 'Σώματος' ;
KWDIKAS_SYMVOLEOGRAFWN : 'Κώδικα' SPACE 'Συμβολαιογράφων';
KWDIKAS_SYNTAKSEWN_PROSOPIKOU_OSE : 'Κώδικα' SPACE 'Συντάξεων' SPACE 'Προσωπικού' SPACE 'ΟΣΕ' ;
KWDIKAS_ANOTATOU_EIDIKOU_DIKASTIRIOU : 'Κώδικα' SPACE 'ΑΕΔ';
KWDIKAS_FOROLOGIAS_KLIRONOMIWN : 'Κώδικα' SPACE 'Φορολογίας' SPACE 'Κληρονομιών' | 'ΚΦΚ' | 'Κώδικας' SPACE 'Διατάξεων' SPACE 'Φορολογίας' SPACE 'Κληρονομιών' COMMA SPACE 'Δωρεών' COMMA SPACE 'Γονικών' SPACE 'Παροχών';
KWDIKAS_FOROLOGIKIS_APEIKONISIS_SYNALLAGWN: 'Κ.Φ.Α.Σ.';

PARARTIMA_TEXT: 'παράρτημα' | 'παραρτήµατος' | 'παράρτηµα' | 'Παράρτημα' ;
PART_TEXT: 'μέρος' | 'µέρος' ;

CHAPTER_TEXT :
    'Κεφ.' |
    'Κεφ' |
    'Κεφαλαίου' |
    'κεφαλαίου' |
    SPECIAL_TEXT SPACE 'Κεφαλαίου'
    ;

ARTHRA_PLURAL :
    'άρθρων' |
    'των άρθρ.' |
    'άρθρα';

ARTHRO_TEXT :
    'άρθρ.' |
    'αρθ.' | 'αρθ'|
    'Άρθρο' |
    'Άρθρου' |
    'άρθρο' |
    //'άρθρων' |
    'άρθρον' |
    'άρθρου' |
    'αρθρ.' |
    'ʼρθρο' |
    'Αρθρο' |
    'άρθρo'
    ;

//θέμα με dehyphenation των λέξεων
PAR_TEXT :
    'παράγραφος' |
    'παραγράφου' |
    'παράγραφο' |
    'παρα-γράφους' |
    '§' | '§§'|
    'παραγράφους' |
    'παράγραφοι' |
    'παραγράφων' |
    'παρ.' | 'παρ,'|
    'παραγ.' |
    'παράγ.' |
    'παραγρ.' |
    'παρα-' SPACE* 'γράφους' |
    'Παρ.'
    ;

//Χρησιμοποιούνται για αναφορά σε λόγους αναιρέσεως
//Δες αρειο πάγο 259_2012
POINT_TEXT :
    'αρ.' |
    'άρ.'|
    //'αρ.'|
    'αριθ.' |
    'αρίθ.' |
    'αριθμό' | //ΑΠ 1695 2008 δημιουργείται conflict
    'αριθμ.' |
    'αριθμού'
    ;

SUBPAR_TEXT:
    'υποπαραγράφου' |
    'υποπαράγραφο' |
    'υποπαράγραφος'
    ;

PERIPTWSI_TEXT :
    'περ.' |
    'περίπτωση' |
    'περίπτωσης' |
    'περίπτ.'
    ;

//SUBPERIPTWSI_TEXT : 'υποπερίπτ.';

EDAFIO_TEXT :
    'εδαφίοις' |
    'εδ.' |
    'εδ' |
    'εδάφιο' |
    'εδάφ.' |
    'εδαφ.' |
    'εδαφίου' |
    'εδάφια'
    ;

STOIXEIO_TEXT :
    'στοιχ.' |
    'στοιχείον' |
    'στοιχείων' |
    //'στοιχ.' |
    'στ.'
    ;

SPECIAL_TEXT : (
    'αυτής' | 'αυτή' | 'αυτού' |
    'άνω' | 'ως άνω' | 'ανωτέρω' | 'πάνω' | 'παραπάνω' |
    'προηγούμενο'| 'προηγούμενες'| 'προηγούμενου' |
    'προσβαλλομένη' | 'προσβαλλομένης'| 'προσβαλλόμενης' | 'προσβαλλόμενη' | 'αναιρεσιβαλλόμενης' |
    'πρωτόδικης' | 'προδικαστική'| 'συγχωνευτικής' | 'παραπεμπτικής' | 'καταδικαστική'| 'οριστική' | 'αναιρετική' |
    'παρόντος' | 'παρούσα' | 'παρούσας' |
    'εκκαλούμενη' | 'υπόψη' | 'ισχύοντος' | 'εν λόγω' |  'ισχύοντος' |
    'ίδιου' | 'ίδιος' | 'ιδίου' | 'Ποινική' |  'αποσπάσεων' | 'ισχύον' |
    'Πρωτοβάθμιου' | 'παραπεμπτική' | 'εκκαλουμένης' | 'πρωτοβάθμιας' |
    'μη οριστική'
    );

DECISION_ELEMENT:
    'αποφάσεως' |
    'απόφασή' |
    'απόφασης' |
    'απόφαση' |
    'αποφάσεις' |
    'αποφάσεώς' |
    //'αποφάσεις' |
    'Απόφαση' |
    'Απόφ.'
    ;

YP_ARITHM :
    'με' SPACE 'αριθμό' |
    'υπ\'' SPACE? 'αριθμ.' |
    'υπ\'' SPACE 'αριθ.' |
    'την' SPACE 'αριθ.' |
    'υπ’' SPACE 'αριθμ.' |
    'υπ\'' SPACE 'αριθμό' |
    'υπ΄' SPACE? 'αριθμ.' |
    'με' SPACE 'αριθ.' |
    'υπ\'' SPACE 'αρ.' |
    'υπ\'' SPACE 'αριθμ' |
    'υπ΄' SPACE? 'αρίθ.' |
    'υπ` αριθμ.' |
    'υπ’' SPACE 'αριθ.' |
    'υπ΄αριθ.'
    ;

EU_REGULATION :
    'Εκτελεστικός Κανονισµός' |
    'κανονισµού' | 'Κανονισμού' |
    (('ΚΑΝ' | 'κανονισµού' | 'Κανονισμού') SPACE)?  '(ΕΚ)' |
    'Κανονισμό'
    ;

EU_DIRECTIVE :
    'Οδηγίας' (SPACE '-' SPACE 'Πλαίσιο')? |
    'Οδηγία' | 'οδηγία'|
    'οδηγίας' |
    'Οδηγίες';

EU_TEXT : '(ΕΕ)' ;

LEGAL_OPINION_TEXT:
    'γνωμοδότηση' |
    'γνωµοδότηση' |
    //'Γνωμοδότησης' |
    'γνωμοδότησιν' |
    'Γνωμοδ.' |
    'Γνωμ/ση' |
    'Γνωμ.' |
    'Γνωμοδότηση' |
    'γνωμοδοτήσεων' |
    'ΓνωμΝΣΚ'
    ;

NOMIKO_SYMB_KRATOUS : ('OλΝ.Σ.Κ.' | 'ολΝ.Σ.Κ.' | 'Ν.Σ.Κ.' | 'ΝΣΚ' | 'ΟλΝΣΚ' | 'Νομικού Συμβουλίου του Κράτους');
STO : 'στο';
ME_TO : 'με το';
//ISSUE : (('τ.' SPACE?)? ALL_CHARS APOSTROPHE) | (('τ.' SPACE?)? 'ΑΕ και ΕΠΕ') ;


STE: ('Συμβουλίου' SPACE 'της' SPACE 'Επικρατείας' | 'ΣτΕ' | 'Σ.τ.Ε.' | 'Σ.Ε.' | 'ΣΕ' | 'ΣΤΕ' | 'Σ.τ.Ε' | 'ΣτΕ' | 'ΟλΣτΕ');
AED: 'Α.Ε.Δ.' | 'ΑΕΔ';
SUPREME_COURT: OLOMELEIA? SPACE? ('ΑΠ' | 'Α.Π.') | 'Αρείου' SPACE 'Πάγου' | ('ΑΠ' | 'Α.Π.') SPACE? OLOMELEIA?;
MAGISTRATE_COURT_OF_THESSALONIKI: 'Πλημμελειοδικείου' SPACE 'Θεσσαλονίκης';
MAGISTRATE_COURT_OF_LAMIA: 'Πλημμελειοδικείου' SPACE 'Λαμίας';
MAGISTRATE_COURT_OF_PIRAEUS: 'Πλημμελειοδικείου' SPACE ('Πειραιώς' | 'Πειραιά');
MAGISTRATE_COURT_OF_ATHENS: 'Πλημμελειοδικείου' SPACE 'Αθηνών' | 'Πλημ/κείου' SPACE 'Αθηνών';
APELLATE_COURT_OF_ATHENS: 'Εφετείου' SPACE ('Αθηνών' | 'Αθήνας') | 'Εφετείου' SPACE '(Πλημμελημάτων)' SPACE 'Αθηνών' | 'ΕφΑθ' | 'Εφ.Αθ.';
APELLATE_COURT_OF_LAMIA : 'Εφετείου' SPACE 'Λαμίας';
APELLATE_COURT_OF_PIRAEUS: 'Εφετείου' SPACE ('Πειραιώς' | 'Πειραιά') | 'ΕφΠειρ';
APELLATE_COURT_OF_THESSALONIKI : 'Μον. '? 'Εφετείου' SPACE 'Θεσσαλονίκης' | 'ΕφΘεσ' | 'Εφ.Θεσ.';
APELLATE_COURT_OF_CORFU : 'Εφετείου' SPACE 'Κέρκυρας';
APELLATE_COURT_OF_THRAKI : 'Εφετείου' SPACE 'Θράκης';
APELLATE_COURT_OF_IOANNINA : 'Εφετείου' SPACE ('Iωαvvίvωv' | 'Ιωαννίνων');
APELLATE_COURT_OF_DODEKANISA : 'Εφετείου' SPACE ('Δωδεκαvήσoυ' | 'Δωδεκανήσου') | 'ΕφΔωδ';
APELLATE_COURT_OF_AEGEAN : 'Εφετείου' SPACE 'Αιγαίoυ';
APELLATE_COURT_OF_CRETE : 'Εφετείου' SPACE 'Κρήτης';
APELLATE_COURT_OF_WEST_MACEDONIA : 'Εφετείου' SPACE 'Δυτ. Μακεδονίας' | 'ΕφΔυτΜακ';
APELLATE_COURT_OF_LARISA : 'Διοικητικού Εφετείου Λάρισας' | 'Εφετείου' SPACE ('Λάρισας' | 'Λαρίσης') | 'ΔΕ' SPACE? 'Λάρισας' ;
APELLATE_COURT_OF_NAFPLIO : 'Εφετείου' SPACE 'Ναυπλίoυ';
APELLATE_COURT_OF_PATRAS : 'Εφετείου' SPACE 'Πατρώv' | 'Εφετείου' SPACE 'Πατρών';
APELLATE_COURT_OF_WEST_STEREAS : 'Εφετείου' SPACE 'Δυτ. Στερεάς';
APELLATE_COURT_OF_NORTH_AEGEAN : 'Εφετείου' SPACE 'Βορείου' SPACE 'Αιγαίου';
APELLATE_COURT_OF_EAST_CRETE : 'Εφετείου' SPACE 'Αν.' SPACE 'Κρήτης';
APELLATE_COURT_OF_KALAMATA : 'Εφετείου' SPACE 'Καλαμάτας';
APELLATE_COURT_OF_EVOIA : 'Εφετείου' SPACE 'Ευβοίας';
FIRST_INSTANCE_COURT_OF_ATHENS: 'Πρωτοδικείου' SPACE 'Αθηνών' | 'ΠΠΑθ' DOT;
FIRST_INSTANCE_COURT_OF_LAMIA: 'Πρωτοδικείου' SPACE 'Λαμίας';
FIRST_INSTANCE_COURT_OF_AMFISSA: 'Πρωτοδικείου' SPACE 'Αμφισσας';
FIRST_INSTANCE_COURT_OF_EVRITANIA: 'Πρωτοδικείου' SPACE 'Ευρυταvίας';
FIRST_INSTANCE_COURT_OF_LIVADIA: 'Πρωτοδικείου' SPACE 'Λιβαδειάς';
FIRST_INSTANCE_COURT_OF_PIRAEUS: ('Μον.' SPACE)? 'Πρωτοδικείου' SPACE ('Πειραιώς' | 'Πειραιά');
FIRST_INSTANCE_COURT_OF_THESSALONIKI: 'Πρωτοδικείου' SPACE 'Θεσσαλονίκης';
FIRST_INSTANCE_COURT_OF_VEROIA : 'Πρωτοδικείου' SPACE 'Βέρoιας';
FIRST_INSTANCE_COURT_OF_EDESSA: 'Πρωτοδικείου' SPACE 'Εδεσσας';
FIRST_INSTANCE_COURT_OF_KATERINI : 'Πρωτοδικείου' SPACE 'Κατερίvης';
FIRST_INSTANCE_COURT_OF_KILKIS : 'Πρωτοδικείου' SPACE 'Κιλκίς';
FIRST_INSTANCE_COURT_OF_SERRES : 'Πρωτοδικείου' SPACE 'Σερρώv';
FIRST_INSTANCE_COURT_OF_XALKIDIKI: 'Πρωτοδικείου' SPACE 'Χαλκιδικής';
FIRST_INSTANCE_COURT_OF_CORFU: 'Πρωτοδικείου' SPACE 'Κέρκυρας';
FIRST_INSTANCE_COURT_OF_GIANNITSA: 'Πρωτοδικείου' SPACE 'Γιαvvιτσώv';
FIRST_INSTANCE_COURT_OF_THESPRWTIA: 'Πρωτοδικείου' SPACE 'Θεσπρωτίας';
FIRST_INSTANCE_COURT_OF_RODOPI: 'Πρωτοδικείου' SPACE 'Ρoδόπης';
FIRST_INSTANCE_COURT_OF_DRAMA: 'Πρωτοδικείου' SPACE 'Δράμας';
FIRST_INSTANCE_COURT_OF_EVROS: 'Πρωτοδικείου' SPACE 'Εβρου';
FIRST_INSTANCE_COURT_OF_KAVALA: 'Πρωτοδικείου' SPACE 'Καβάλας';
FIRST_INSTANCE_COURT_OF_XANTHI: 'Πρωτοδικείου' SPACE 'Ξάvθης';
FIRST_INSTANCE_COURT_OF_ORESTIADA: 'Πρωτοδικείου' SPACE 'Ορεστιάδας';
FIRST_INSTANCE_COURT_OF_IOANNINA: 'Πρωτοδικείου' SPACE 'Iωαvvίvωv';
FIRST_INSTANCE_COURT_OF_ARTA: 'Πρωτοδικείου' SPACE 'Αρτας';
FIRST_INSTANCE_COURT_OF_PREVEZA: 'Πρωτοδικείου' SPACE 'Πρέβεζας';
FIRST_INSTANCE_COURT_OF_RODOS: 'Πρωτοδικείου' SPACE 'Ρόδoυ';
FIRST_INSTANCE_COURT_OF_KOS: 'Πρωτοδικείου' SPACE 'Κω';
FIRST_INSTANCE_COURT_OF_SYROS: 'Πρωτοδικείου' SPACE 'Σύρoυ';
FIRST_INSTANCE_COURT_OF_SAMOS: 'Πρωτοδικείου' SPACE 'Σάμoυ';
FIRST_INSTANCE_COURT_OF_NAXOS: 'Πρωτοδικείου' SPACE 'Νάξου';
FIRST_INSTANCE_COURT_OF_CHANIA: 'Πρωτοδικείου' SPACE 'Χαvίωv';
FIRST_INSTANCE_COURT_OF_RETHYMNO: 'Πρωτοδικείου' SPACE 'Ρεθύμvης';
FIRST_INSTANCE_COURT_OF_KOZANI: 'Πρωτοδικείου' SPACE 'Κoζάvης';
FIRST_INSTANCE_COURT_OF_GREVENA: 'Πρωτοδικείου' SPACE 'Γρεβεvώv';
FIRST_INSTANCE_COURT_OF_KASTORIA: 'Πρωτοδικείου' SPACE 'Καστοριάς';
FIRST_INSTANCE_COURT_OF_FLORINA: 'Πρωτοδικείου' SPACE 'Φλώριvας';
FIRST_INSTANCE_COURT_OF_LARISA: 'Πρωτοδικείου' SPACE 'Λάρισας';
FIRST_INSTANCE_COURT_OF_VOLOS: 'Πρωτοδικείου' SPACE 'Βόλoυ';
FIRST_INSTANCE_COURT_OF_KARDITSA: 'Πρωτοδικείου' SPACE 'Καρδίτσας';
FIRST_INSTANCE_COURT_OF_TRIKALA: 'Πρωτοδικείου' SPACE 'Τρικάλωv';
FIRST_INSTANCE_COURT_OF_NAFPLIO: 'Πρωτοδικείου' SPACE 'Ναυπλίoυ';
FIRST_INSTANCE_COURT_OF_CORINTH: 'Πρωτοδικείου' SPACE 'Κoρίvθoυ';
FIRST_INSTANCE_COURT_OF_SPARTI: 'Πρωτοδικείου' SPACE 'Σπάρτης';
FIRST_INSTANCE_COURT_OF_TRIPOLI: 'Πρωτοδικείου' SPACE 'Τρίπoλης';
FIRST_INSTANCE_COURT_OF_KALAMATA: 'Πρωτοδικείου' SPACE 'Καλαμάτας';
FIRST_INSTANCE_COURT_OF_KIPARISSIA: 'Πρωτοδικείου' SPACE 'Κυπαρισσίας';
FIRST_INSTANCE_COURT_OF_GYHTEIO: 'Πρωτοδικείου' SPACE 'Γυθείου';
FIRST_INSTANCE_COURT_OF_PATRAS: 'Πρωτοδικείου' SPACE 'Πατρώv';
FIRST_INSTANCE_COURT_OF_AIGIO: 'Πρωτοδικείου' SPACE 'Αιγίoυ';
FIRST_INSTANCE_COURT_OF_KALAVRITA: 'Πρωτοδικείου' SPACE 'Καλαβρύτωv';
FIRST_INSTANCE_COURT_OF_HLEIAS: 'Πρωτοδικείου' SPACE 'Ηλείας';
FIRST_INSTANCE_COURT_OF_AMALIADA: 'Πρωτοδικείου' SPACE 'Αμαλιάδας';
FIRST_INSTANCE_COURT_OF_ZAKINTHOS: 'Πρωτοδικείου' SPACE 'Ζακύvθoυ';
FIRST_INSTANCE_COURT_OF_KEFALLONIA: 'Πρωτοδικείου' SPACE 'Κεφαλληvίας';
FIRST_INSTANCE_COURT_OF_AGRINIO: ('Πρωτοδικείου' | 'Πρωτοδικείου') SPACE ('Αγριvίoυ' | 'Αγρινίου');
FIRST_INSTANCE_COURT_OF_LEFKADA: 'Πρωτοδικείου' SPACE 'Λευκάδας';
FIRST_INSTANCE_COURT_OF_MESOLOGGI: 'Πρωτοδικείου' SPACE 'Μεσoλoγγίoυ';
FIRST_INSTANCE_COURT_OF_MITILINI: 'Πρωτοδικείου' SPACE 'Μυτιλήvης';
FIRST_INSTANCE_COURT_OF_CHIOS: 'Πρωτοδικείου' SPACE ('Χίoυ' | 'Χίου') | 'ΜονΠρωτΧίου' | 'ΠολΠρωτΧίου';
FIRST_INSTANCE_COURT_OF_HRAKLEIO: 'Πρωτοδικείου' SPACE 'Ηρακλείoυ';
FIRST_INSTANCE_COURT_OF_LASITHI: 'Πρωτοδικείου' SPACE 'Λασιθίoυ';
FIRST_INSTANCE_COURT_OF_THIVA: 'Πρωτοδικείου' SPACE 'Θηβώv';
FIRST_INSTANCE_COURT_OF_CHALKIDA: 'Πρωτοδικείου' SPACE 'Χαλκίδας';
COUNTY_COURT_OF_ATHENS: 'Ειρηvoδικείου' SPACE 'Αθηνών';
COUNTY_COURT_OF_MAROUSSI : 'Ειρηvoδικείoυ' SPACE 'Αμαρoυσίoυ';
COUNTY_COURT_OF_AXARNON: 'Ειρηvoδικείoυ' SPACE 'Αχαρνών';
COUNTY_COURT_OF_ELEFSINA: 'Ειρηvoδικείoυ' SPACE 'Ελευσίνας';
COUNTY_COURT_OF_KALLITHEA: 'Ειρηvoδικείoυ' SPACE 'Καλλιθέας';
COUNTY_COURT_OF_KROPIA: 'Ειρηvoδικείoυ' SPACE 'Κρωπίας';
COUNTY_COURT_OF_LAVRIO: 'Ειρηvoδικείoυ' SPACE 'Λαυρίoυ';
COUNTY_COURT_OF_NEAS_IONIAS: 'Ειρηvoδικείoυ' SPACE 'Ν. Iωvίας';
COUNTY_COURT_OF_NEA_LIOSIA: 'Ειρηvoδικείoυ' SPACE 'Ν. Λιoσίωv';
COUNTY_COURT_OF_MARATHONA: 'Ειρηvoδικείoυ' SPACE 'Μαραθώvoς';
COUNTY_COURT_OF_MEGARA: 'Ειρηvoδικείoυ' SPACE 'Μεγάρωv';
COUNTY_COURT_OF_PERISTERI: 'Ειρηvoδικείoυ' SPACE 'Περιστερίoυ';
COUNTY_COURT_OF_CHALANDRI: 'Ειρηvoδικείoυ' SPACE 'Χαλαvδρίoυ';
COUNTY_COURT_OF_LAMIA : 'Ειρηvoδικείoυ' SPACE 'Λαμίας';
COUNTY_COURT_OF_ATALANTI: 'Ειρηvoδικείoυ' SPACE 'Αταλάvτης';
COUNTY_COURT_OF_AMFISSA : 'Ειρηvoδικείoυ' SPACE 'Αμφισσας';
COUNTY_COURT_OF_EVRITANIA : 'Ειρηvoδικείoυ' SPACE 'Ευρυταvίας';
COUNTY_COURT_OF_LIVADIA : 'Ειρηvoδικείoυ' SPACE 'Λιβαδειάς';
COUNTY_COURT_OF_AIGINA : 'Ειρηvoδικείoυ' SPACE 'Αιγίvης';
COUNTY_COURT_OF_KALAVRIA: 'Ειρηvoδικείoυ' SPACE 'Καλαυρίας';
COUNTY_COURT_OF_KITHIRA: 'Ειρηvoδικείoυ' SPACE 'Κυθήρωv';
COUNTY_COURT_OF_NIKAIAS: 'Ειρηvoδικείoυ' SPACE 'Νίκαιας';
COUNTY_COURT_OF_SALAMINA: 'Ειρηvoδικείoυ' SPACE 'Σαλαμίvας';
COUNTY_COURT_OF_SPETSES: 'Ειρηvoδικείoυ' SPACE 'Σπετσώv';
COUNTY_COURT_OF_THESSALONIKI: 'Ειρηvoδικείoυ' SPACE 'Θεσσαλονίκης';
COUNTY_COURT_OF_PIRAEUS : 'Ειρηvoδικείoυ' SPACE ('Πειραιώς' | 'Πειραιά');
COUNTY_COURT_OF_VASILIKON: 'Ειρηvoδικείoυ' SPACE 'Βασιλικώv';
COUNTY_COURT_OF_KOUFALION: 'Ειρηvoδικείoυ' SPACE 'Κoυφαλίωv';
COUNTY_COURT_OF_LAGKADA: 'Ειρηvoδικείoυ' SPACE 'Λαγκαδά';
COUNTY_COURT_OF_ALEXANDRIA: 'Ειρηvoδικείoυ' SPACE 'Αλεξάvδρειας';
COUNTY_COURT_OF_NAOUSA: 'Ειρηvoδικείoυ' SPACE 'Νάoυσας';
COUNTY_COURT_OF_EDESSA: 'Ειρηvoδικείoυ' SPACE 'Έδεσσας';
COUNTY_COURT_OF_ALMOPIA: 'Ειρηvoδικείoυ' SPACE 'Αλμωπίας';
COUNTY_COURT_OF_SKYDRA: 'Ειρηvoδικείoυ' SPACE 'Σκύδρας';
COUNTY_COURT_OF_PIERIA: 'Ειρηvoδικείoυ' SPACE 'Πιερίας';
COUNTY_COURT_OF_KOLINDROU: 'Ειρηvoδικείoυ' SPACE 'Κολινδρού';
COUNTY_COURT_OF_POLIKASTRO: 'Ειρηvoδικείoυ' SPACE 'Πoλυκάστρoυ';
COUNTY_COURT_OF_SERRES: 'Ειρηvoδικείoυ' SPACE 'Σερρώv';
COUNTY_COURT_OF_NIGRITA: 'Ειρηvoδικείoυ' SPACE 'Νιγρίτας';
COUNTY_COURT_OF_RODOLIVON: 'Ειρηvoδικείoυ' SPACE 'Ρoδoλίβoυς';
COUNTY_COURT_OF_SINTIKIS: 'Ειρηvoδικείoυ' SPACE 'Συvτικής';
COUNTY_COURT_OF_POLIGIROU: 'Ειρηvoδικείoυ' SPACE 'Πoλυγύρoυ';
COUNTY_COURT_OF_ARNAIA: 'Ειρηvoδικείoυ' SPACE 'Αρvαίας';
COUNTY_COURT_OF_KASSANDRA: 'Ειρηvoδικείoυ' SPACE 'Κασσάvδρας';
COUNTY_COURT_OF_NEA_MOUDANIA: 'Ειρηvoδικείoυ' SPACE 'Ν. Μουδανιών';
COUNTY_COURT_OF_CORFU: 'Ειρηvoδικείoυ' SPACE 'Κέρκυρας';
COUNTY_COURT_OF_IGOUMENITSA: 'Ειρηvoδικείoυ' SPACE 'Ηγoυμεvίτσας';
COUNTY_COURT_OF_KOMOTINI: 'Ειρηvoδικείoυ' SPACE 'Κoμoτηvής';
COUNTY_COURT_OF_DRAMA: 'Ειρηvoδικείoυ' SPACE 'Δράμας';
COUNTY_COURT_OF_THASOS: 'Ειρηvoδικείoυ' SPACE 'Θάσoυ';
COUNTY_COURT_OF_PAGGAIOU: 'Ειρηvoδικείoυ' SPACE 'Παγγαίoυ';
COUNTY_COURT_OF_ORESTIADA: 'Ειρηvoδικείoυ' SPACE 'Ορεστιάδας';
COUNTY_COURT_OF_ALEXANDROUPOLI: 'Ειρηvoδικείoυ' SPACE 'Αλεξαvδρoύπoλης';
COUNTY_COURT_OF_KAVALA: 'Ειρηvoδικείoυ' SPACE 'Καβάλας';
COUNTY_COURT_OF_DIDIMOTEIXO: 'Ειρηvoδικείoυ' SPACE 'Διδυμoτείχoυ';
COUNTY_COURT_OF_IOANNINA: 'Ειρηvoδικείoυ' SPACE 'Iωαvvίvωv';
COUNTY_COURT_OF_KONITSA: 'Ειρηvoδικείoυ' SPACE 'Κovίτσης';
COUNTY_COURT_OF_ARTA: 'Ειρηνοδικείου' SPACE 'Αρτας';
COUNTY_COURT_OF_PREVEZA: 'Ειρηνοδικείου' SPACE 'Πρέβεζας';
COUNTY_COURT_OF_RODOS: 'Ειρηvoδικείoυ' SPACE 'Ρόδoυ';
COUNTY_COURT_OF_KARPATHOS: 'Ειρηvoδικείoυ' SPACE 'Καρπάθoυ';
COUNTY_COURT_OF_KALIMNOS: 'Ειρηvoδικείoυ' SPACE 'Καλύμvoυ';
COUNTY_COURT_OF_KOS: 'Ειρηvoδικείoυ' SPACE 'Κω';
COUNTY_COURT_OF_LEROS: 'Ειρηvoδικείoυ' SPACE 'Λέρoυ';
COUNTY_COURT_OF_ANDROS: 'Ειρηvoδικείoυ' SPACE 'Αvδρoυ';
COUNTY_COURT_OF_ERMOUPOLI: 'Ειρηvoδικείoυ' SPACE 'Ερμoύπoλης';
COUNTY_COURT_OF_MILOS: 'Ειρηvoδικείoυ' SPACE 'Μήλoυ';
COUNTY_COURT_OF_MYKONOS: 'Ειρηvoδικείoυ' SPACE 'Μυκόvoυ';
COUNTY_COURT_OF_PAROS: 'Ειρηvoδικείoυ' SPACE 'Πάρoυ';
COUNTY_COURT_OF_TINOS: 'Ειρηvoδικείoυ' SPACE 'Τήvoυ';
COUNTY_COURT_OF_SAMOS: 'Ειρηvoδικείoυ' SPACE 'Σάμoυ';
COUNTY_COURT_OF_IKARIA: 'Ειρηvoδικείoυ' SPACE 'Iκαρίας';
COUNTY_COURT_OF_KARLOVASI: 'Ειρηvoδικείoυ' SPACE 'Καρλoβασίoυ';
COUNTY_COURT_OF_NAXOS: 'Ειρηvoδικείoυ' SPACE 'Νάξoυ';
COUNTY_COURT_OF_CHANIA: 'Ειρηvoδικείoυ' SPACE 'Χαvίωv';
COUNTY_COURT_OF_VAMOU: 'Ειρηvoδικείoυ' SPACE 'Βάμoυ';
COUNTY_COURT_OF_RETHYMNO: 'Ειρηvoδικείoυ' SPACE 'Ρεθύμvης';
COUNTY_COURT_OF_KOZANI: 'Ειρηvoδικείoυ' SPACE 'Κoζάvης';
COUNTY_COURT_OF_EORDAIA: 'Ειρηvoδικείoυ' SPACE 'Εoρδαίας';
COUNTY_COURT_OF_GREVENA: 'Ειρηvoδικείoυ' SPACE 'Γρεβεvώv';
COUNTY_COURT_OF_KASTORIA: 'Ειρηvoδικείoυ' SPACE 'Καστoριάς';
COUNTY_COURT_OF_FLORINA: 'Ειρηvoδικείoυ' SPACE 'Φλώριvας';
COUNTY_COURT_OF_AMUNTAIO: 'Ειρηvoδικείoυ' SPACE 'Αμυvταίoυ';
COUNTY_COURT_OF_LARISA: 'Ειρηvoδικείoυ' SPACE 'Λάρισας';
COUNTY_COURT_OF_ELASSONAS: 'Ειρηvoδικείoυ' SPACE 'Ελασσόvας';
COUNTY_COURT_OF_FARSALA: 'Ειρηvoδικείoυ' SPACE 'Φαρσάλων';
COUNTY_COURT_OF_VOLOS: 'Ειρηvoδικείoυ' SPACE 'Βόλoυ';
COUNTY_COURT_OF_ALMIROS: 'Ειρηvoδικείoυ' SPACE 'Αλμυρoύ';
COUNTY_COURT_OF_SKOPELOS: 'Ειρηvoδικείoυ' SPACE 'Σκοπέλου';
COUNTY_COURT_OF_KARDITSA: 'Ειρηvoδικείoυ' SPACE 'Καρδίτσας';
COUNTY_COURT_OF_TRIKALA: 'Ειρηvoδικείoυ' SPACE 'Τρικάλωv';
COUNTY_COURT_OF_KALAMPAKA: 'Ειρηvoδικείoυ' SPACE 'Καλαμπάκας';
COUNTY_COURT_OF_NAFPLIO: 'Ειρηvoδικείoυ' SPACE 'Ναυπλίoυ';
COUNTY_COURT_OF_ASTROS: 'Ειρηvoδικείoυ' SPACE 'Αστρoυς';
COUNTY_COURT_OF_ARGOS: 'Ειρηvoδικείoυ' SPACE 'Αργoυς';
COUNTY_COURT_OF_MASSITOS: 'Ειρηvoδικείoυ' SPACE 'Μάσσητoς';
COUNTY_COURT_OF_THIRA: 'Ειρηvoδικείoυ' SPACE 'Θήρας';
COUNTY_COURT_OF_CORINTH: 'Ειρηvoδικείoυ' SPACE 'Κoρίvθoυ';
COUNTY_COURT_OF_SIKIONOS: 'Ειρηvoδικείoυ' SPACE 'Σικυώvoς';
COUNTY_COURT_OF_NEMEA: 'Ειρηvoδικείoυ' SPACE 'Νεμέας';
COUNTY_COURT_OF_XYLOKASTRO: 'Ειρηvoδικείoυ' SPACE 'Ξυλoκάστρoυ';
COUNTY_COURT_OF_SPARTI: 'Ειρηvoδικείoυ' SPACE 'Σπάρτης';
COUNTY_COURT_OF_EPIDAVROS_LIMIRAS: 'Ειρηvoδικείoυ' SPACE 'Επιδαύρoυ-Λιμηράς' ;
COUNTY_COURT_OF_TRIPOLI: 'Ειρηvoδικείoυ' SPACE 'Τρίπoλης';
COUNTY_COURT_OF_MEGALOPOLI: 'Ειρηvoδικείoυ' SPACE 'Μεγαλόπολης';
COUNTY_COURT_OF_PSOFIDA: 'Ειρηvoδικείoυ' SPACE 'Ψωφίδoς';
COUNTY_COURT_OF_KALAMATA: 'Ειρηvoδικείoυ' SPACE 'Καλαμάτας';
COUNTY_COURT_OF_PILOS: 'Ειρηvoδικείoυ' SPACE 'Πύλου';
COUNTY_COURT_OF_KIPARISSIA: 'Ειρηvoδικείoυ' SPACE 'Κυπαρισσίας';
COUNTY_COURT_OF_PLATAMODA: 'Ειρηvoδικείoυ' SPACE 'Πλαταμώδους';
COUNTY_COURT_OF_GYTHEIO: 'Ειρηvoδικείoυ' SPACE 'Γυθείου';
COUNTY_COURT_OF_NEAPOLI_VOIWN: 'Ειρηvoδικείoυ' SPACE 'Νεαπόλεως' SPACE 'Βοιών';
COUNTY_COURT_OF_PATRAS: 'Ειρηvoδικείoυ' SPACE 'Πατρώv';
COUNTY_COURT_OF_DIMI: 'Ειρηvoδικείoυ' SPACE 'Δύμης';
COUNTY_COURT_OF_AIGIALIA: 'Ειρηvoδικείoυ' SPACE 'Αιγιαλείας';
COUNTY_COURT_OF_KALAVRITA: 'Ειρηvoδικείoυ' SPACE 'Καλαβρύτωv';
COUNTY_COURT_OF_AKRATA: 'Ειρηvoδικείoυ' SPACE 'Ακράτας';
COUNTY_COURT_OF_PIRGOS: 'Ειρηvoδικείoυ' SPACE 'Πύργoυ';
COUNTY_COURT_OF_OLYMPIA: 'Ειρηvoδικείoυ' SPACE 'Ολυμπίωv';
COUNTY_COURT_OF_ARINI: 'Ειρηvoδικείoυ' SPACE 'Αρήvης';
COUNTY_COURT_OF_AMALIADA: 'Ειρηvoδικείoυ' SPACE 'Αμαλιάδας';
COUNTY_COURT_OF_GASTOUNI: 'Ειρηvoδικείoυ' SPACE 'Γαστoύvης';
COUNTY_COURT_OF_MYRTOUNTION: 'Ειρηvoδικείoυ' SPACE 'Μυρτoυvτίωv';
COUNTY_COURT_OF_ZAKINTHOS: 'Ειρηvoδικείoυ' SPACE 'Ζακύvθoυ';
COUNTY_COURT_OF_ARGOSTOLI: 'Ειρηvoδικείoυ' SPACE 'Αργoστoλίoυ';
COUNTY_COURT_OF_SAMEON: 'Ειρηvoδικείoυ' SPACE 'Σαμαίωv';
COUNTY_COURT_OF_AGRINIO: 'Ειρηvoδικείoυ' SPACE 'Αγριvίoυ';
COUNTY_COURT_OF_VALTOS: 'Ειρηvoδικείoυ' SPACE 'Βάλτoυ';
COUNTY_COURT_OF_LEFKADA: 'Ειρηvoδικείoυ' SPACE 'Λευκάδας';
COUNTY_COURT_OF_VONITSA: 'Ειρηvoδικείoυ' SPACE 'Βovίτσας';
COUNTY_COURT_OF_MESOLOGGI: 'Ειρηvoδικείoυ' SPACE 'Μεσoλoγγίoυ';
COUNTY_COURT_OF_NAFPAKTOS: 'Ειρηvoδικείoυ' SPACE 'Ναυπάκτoυ';
COUNTY_COURT_OF_MITILINI: 'Ειρηvoδικείoυ' SPACE 'Μυτιλήvης';
COUNTY_COURT_OF_KALLONI: 'Ειρηvoδικείoυ' SPACE 'Καλλovής';
COUNTY_COURT_OF_CHIOS: 'Ειρηvoδικείoυ' SPACE 'Χίoυ';
COUNTY_COURT_OF_HRAKLEIO: 'Ειρηvoδικείoυ' SPACE 'Ηρακλείoυ';
COUNTY_COURT_OF_KASTELI: 'Ειρηvoδικείoυ' SPACE 'Καστελίoυ - Πεδιάδoς';
COUNTY_COURT_OF_LASITHI: 'Ειρηvoδικείoυ' SPACE 'Λασιθίoυ';
COUNTY_COURT_OF_IERAPETRA: 'Ειρηvoδικείoυ' SPACE 'Iεράπετρας';
COUNTY_COURT_OF_SITEIA: 'Ειρηvoδικείoυ' SPACE 'Σητείας';
COUNTY_COURT_OF_THIVA: 'Ειρηvoδικείoυ' SPACE 'Θηβώv';
COUNTY_COURT_OF_CHALKIDA: 'Ειρηvoδικείoυ' SPACE 'Χαλκίδας';
COUNTY_COURT_OF_ISTIAIA: 'Ειρηvoδικείoυ' SPACE 'Iστιαίας';
COUNTY_COURT_OF_KARYSTOS: 'Ειρηvoδικείoυ' SPACE 'Καρύστoυ';
COUNTY_COURT_OF_KIMI: 'Ειρηvoδικείoυ' SPACE 'Κύμης';
COUNTY_COURT_OF_TAMINEON: 'Ειρηvoδικείoυ' SPACE 'Ταμιvέωv';
DISTRICT_COURT_OF_ATHENS: 'Πταισματoδικείου' SPACE 'Αθηνών';
DISTRICT_COURT_OF_LAMIA: 'Πταισματoδικείου' SPACE 'Λαμίας';
DISTRICT_COURT_OF_LIVADIA: 'Πταισματoδικείου' SPACE 'Λιβαδειάς';
DISTRICT_COURT_OF_PIRAEUS: 'Πταισματoδικείου' SPACE ('Πειραιώς' | 'Πειραιά');
DISTRICT_COURT_OF_THESSALONIKI: 'Πταισματoδικείου' SPACE 'Θεσσαλονίκης';
DISTRICT_COURT_OF_VEROIA: 'Πταισματoδικείου' SPACE 'Βέρoιας';
DISTRICT_COURT_OF_PIERIA: 'Πταισματoδικείου' SPACE 'Πιερίας';
DISTRICT_COURT_OF_SERRES: 'Πταισματoδικείου' SPACE 'Σερρώv' ;
DISTRICT_COURT_OF_CORFU: 'Πταισματoδικείου' SPACE 'Κέρκυρας' ;
DISTRICT_COURT_OF_KOMOTINI: 'Πταισματoδικείου' SPACE 'Κoμoτηvής' ;
DISTRICT_COURT_OF_DRAMA: 'Πταισματoδικείου' SPACE 'Δράμας';
DISTRICT_COURT_OF_KAVALA: 'Πταισματoδικείου' SPACE 'Καβάλας';
DISTRICT_COURT_OF_ARTA: 'Πταισματoδικείου' SPACE 'Αρτας' ;
DISTRICT_COURT_OF_RODOS: 'Πταισματoδικείου' SPACE 'Ρόδoυ';
DISTRICT_COURT_OF_CHANIA: 'Πταισματoδικείου' SPACE 'Χαvίωv';
DISTRICT_COURT_OF_RETHYMNO: 'Πταισματoδικείου' SPACE 'Ρεθύμvης';
DISTRICT_COURT_OF_KOZANI: 'Πταισματoδικείου' SPACE 'Κoζάvης';
DISTRICT_COURT_OF_KLEISOURA: 'Πταισματoδικείου' SPACE 'Κλεισούρας';
DISTRICT_COURT_OF_LARISA: 'Πταισματoδικείου' SPACE 'Λάρισας';
DISTRICT_COURT_OF_ELASSONAS: 'Πταισματoδικείου' SPACE 'Ελασσόvας';
DISTRICT_COURT_OF_VOLOS: 'Πταισματoδικείου' SPACE 'Βόλoυ';
DISTRICT_COURT_OF_KARDITSA: 'Πταισματoδικείου' SPACE 'Καρδίτσας';
DISTRICT_COURT_OF_TRIKALA: 'Πταισματoδικείου' SPACE 'Τρικάλωv';
DISTRICT_COURT_OF_NAFPLIO: 'Πταισματoδικείου' SPACE 'Ναυπλίoυ';
DISTRICT_COURT_OF_ARGOS: 'Πταισματoδικείου' SPACE 'Αργoυς';
DISTRICT_COURT_OF_CORINTH: 'Πταισματoδικείου' SPACE 'Κoρίvθoυ';
DISTRICT_COURT_OF_SIKIONOS: 'Πταισματoδικείου' SPACE 'Σικυώvoς';
DISTRICT_COURT_OF_SPARTI: 'Πταισματoδικείου' SPACE 'Σπάρτης';
DISTRICT_COURT_OF_TRIPOLI: 'Πταισματoδικείου' SPACE 'Τρίπoλης';
DISTRICT_COURT_OF_KALAMATA: 'Πταισματoδικείου' SPACE 'Καλαμάτας';
DISTRICT_COURT_OF_PATRAS: 'Πταισματoδικείου' SPACE 'Πατρώv';
DISTRICT_COURT_OF_AIGIALIA: 'Πταισματoδικείου' SPACE 'Αιγιαλείας';
DISTRICT_COURT_OF_PIRGOS: 'Πταισματoδικείου' SPACE 'Πύργoυ';
DISTRICT_COURT_OF_AMALIADA: 'Πταισματoδικείου' SPACE 'Αμαλιάδας';
DISTRICT_COURT_OF_AGRINIO: 'Πταισματoδικείου' SPACE 'Αγριvίoυ';
DISTRICT_COURT_OF_VALTOS: 'Πταισματoδικείου' SPACE 'Βάλτoυ';
DISTRICT_COURT_OF_MESOLOGGI: 'Πταισματoδικείου' SPACE 'Μεσoλoγγίoυ';
DISTRICT_COURT_OF_MITILINI: 'Πταισματoδικείου' SPACE 'Μυτιλήvης';
DISTRICT_COURT_OF_LIMNOS: 'Πταισματoδικείου' SPACE 'Λήμvoυ';
DISTRICT_COURT_OF_PLOMARI: 'Πταισματoδικείου' SPACE 'Πλωμαρίoυ';
DISTRICT_COURT_OF_HRAKLEIO: 'Πταισματoδικείου' SPACE 'Ηρακλείoυ';
DISTRICT_COURT_OF_MOIRES: 'Πταισματoδικείου' SPACE 'Μoιρώv';
DISTRICT_COURT_OF_PIRGOS_KRITIS: 'Πταισματoδικείου' SPACE 'Πύργoυ' SPACE 'Κρήτης';
DISTRICT_COURT_OF_THIVA: 'Πταισματoδικείου' SPACE 'Θηβώv';
DISTRICT_COURT_OF_CHALKIDA: 'Πταισματoδικείου' SPACE 'Χαλκίδας';



//Prepei na kopei i apostrofos pou exei oristei parapanw - Xreizaomaste mono ta grammata
//ALL_CHARS : ( '\u0027' | '\u0370'..'\u03FF' | '∆' | 'µ'  | '\u0041'..'\u007A' | 'Ω')+; //'u005a' -> English Z
ALL_CHARS :
    ('Ά' | 'Α' | 'α' | 'ά' | 'Β' | 'β' | 'γ' | 'Γ' | 'δ' |'Δ' |
    'ε' | 'Ε' | 'Е' | 'έ' | 'Έ' | 'Ζ' | 'ζ' | 'Η' | 'η' | 'ή' | 'Ή'| 'θ' | 'Θ' |
    'ι' | 'ΐ' | 'Ι' | 'Ί' | 'Ϊ' | 'ί' | 'ϊ' | 'κ' | 'Κ' | 'Λ' | 'λ' | 'Μ' | 'μ' | 'µ'|
    'Ν' | 'ν' | 'Ξ' | 'ξ' | 'ο' | 'Ο' | 'ό' | 'Ό' | 'Π' | 'π' |
    'Ρ' | 'ρ' | 'Σ' | 'σ' | 'ς' | 'τ' | 'Τ' | 'Т' | 'υ' | 'Υ' | 'Ύ' | 'Ϋ' | 'ύ' | 'ϋ' |
    'Φ' | 'φ' | 'Χ' | 'χ' | 'ώ' | 'ω' | 'Ω' | 'Ω' | 'Ώ' | 'ψ' | 'Ψ' | [A-Za-z] | 'ü' | 'é' |
    'ş' |'â' |'ţ' | 'ö' | 'í' | 'ΰ')+;

SPECIAL_CHARS: ('"' | '»' | '«' | '·' | '…' | '%' | '•' | '!' | '‘' | '´' |
'+' | '€' | '*' | '@' | ';' | '“' | '”' | '<' | '>' | '_' | '=' | '¶' |
'#' | '?'  | 'ʼ' | '·' | '{' | '}' | '^' | '$' | '½' | '' | '˙' | '¨' | '×'| '²' |
'¬' | '¾' | '~' | [|] | '¼' | '‰' | '¦' | '£' | '­' | '―' | '—' | '¥' );

SPACE : [\n\r\t ]+  | ' ';

/*
fragment FEK_REF :
    FEK_ELEMENT SPACE NUM SLASH NUM (HYPHEN NUM)*|
    FEK_ELEMENT SPACE NUM SLASH ISSUE SLASH NUM (HYPHEN NUM)* |
    FEK_ELEMENT SPACE NUM SLASH NUM (HYPHEN NUM)* SPACE ISSUE |
    FEK_ELEMENT SPACE IONIKO_SYSTEM SPACE? HYPHEN SPACE? NUM |
    FEK_ELEMENT SPACE (IONIKO_SYSTEM SPACE? NUM | NUM SPACE IONIKO_SYSTEM)|
    IONIKO_SYSTEM SPACE? NUM ((DOT|HYPHEN|COMMA) SPACE? NUM)? (SLASH SPACE? NUM ((DOT|HYPHEN) NUM)*)+ |
    FEK_ELEMENT SPACE NUM SPACE ISSUE |
    FEK_ELEMENT SPACE NUM ((DOT|HYPHEN|COMMA) SPACE* NUM)? (SLASH SPACE? NUM ((DOT|HYPHEN) SPACE* NUM)*)+ COMMA SPACE ISSUE |
    FEK_ELEMENT SPACE IONIKO_SYSTEM COMMA SPACE NUM |
    FEK_ELEMENT SPACE IONIKO_SYSTEM SPACE NUM SLASH NUM (DOT NUM)*|
    FEK_ELEMENT SPACE IONIKO_SYSTEM NUM (SLASH NUM ((DOT|HYPHEN) NUM)*)* |
    NUM SPACE ALL_CHARS APOSTROPHE |
    FEK_ELEMENT SPACE NUM IONIKO_SYSTEM|
    //IONIKO_SYSTEM SPACE? NUM | //Kanei conflict des Politikh_Ypouesh_Areioy_Pagoy__Ar_1802_2012,_3_12_2012
    FEK_ELEMENT SPACE NUM SLASH NUM (DOT NUM)* |
    ;

fragment FEK_ELEMENT : ('ΦΕΚ' | 'φ'[.]? | 'Φ.Ε.Κ' | 'ΦΕΚ') ;
*/

/*
//Θέλουμε όλα τα δικαστήριο που υπάρχουν στην Ελλάδα
fragment GREEK_COURTS : (
    ('Συμβουλίου της Επικρατείας' | 'ΣτΕ' | 'Σ.τ.Ε.' | 'Σ.Ε.' | 'ΣΕ' | 'ΣΤΕ' | 'Σ.τ.Ε') |
    'Αρείου' SPACE 'Πάγου'|
    OLOMELEIA? SPACE? ('ΑΠ' | 'Α.Π.') |
    'Εφετείου' SPACE ('Αθηνών' | 'Αθήνας') |
    'Πρωτοδικείου' SPACE 'Αθηνών' |
    'Ειρηvoδικείου' SPACE 'Αθηνών' |
    'Πταισματoδικείου' SPACE 'Αθηνών' |
    'Εφετείου' SPACE '(Πλημμελημάτων)' SPACE 'Αθηνών' |
    'Ειρηvoδικείoυ' SPACE 'Αμαρoυσίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Αχαρνών' |
    'Ειρηvoδικείoυ' SPACE 'Ελευσίνας' |
    'Ειρηvoδικείoυ' SPACE 'Καλλιθέας' |
    'Ειρηvoδικείoυ' SPACE 'Κρωπίας' |
    'Ειρηvoδικείoυ' SPACE 'Λαυρίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ν. Iωvίας' |
    'Ειρηvoδικείoυ' SPACE 'Ν. Λιoσίωv' |
    'Ειρηvoδικείoυ' SPACE 'Μαραθώvoς' |
    'Ειρηvoδικείoυ' SPACE 'Μεγάρωv' |
    'Ειρηvoδικείoυ' SPACE 'Περιστερίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Χαλαvδρίoυ' |
    'Πλημμελειοδικείου' SPACE 'Λαμίας' |
    'Εφετείου' SPACE 'Λαμίας' |
    'Πρωτοδικείου' SPACE 'Λαμίας' |
    'Ειρηvoδικείoυ' SPACE 'Λαμίας' |
    'Πταισματoδικείου' SPACE 'Λαμίας' |
    'Ειρηvoδικείoυ' SPACE 'Αταλάvτης' |
    'Πρωτοδικείου' SPACE 'Αμφισσας' |
    'Ειρηvoδικείoυ' SPACE 'Αμφισσας' |
    'Πρωτοδικείου' SPACE 'Ευρυταvίας' |
    'Ειρηvoδικείoυ' SPACE 'Ευρυταvίας' |
    'Πρωτοδικείου' SPACE 'Λιβαδειάς' |
    'Ειρηvoδικείoυ' SPACE 'Λιβαδειάς' |
    'Πταισματoδικείου' SPACE 'Λιβαδειάς' |
    'Εφετείου' SPACE ('Πειραιώς' | 'Πειραιά') |
    ('Μον.' SPACE)? 'Πρωτοδικείου' SPACE ('Πειραιώς' | 'Πειραιά') |
    'Ειρηvoδικείoυ' SPACE ('Πειραιώς' | 'Πειραιά') |
    'Πταισματoδικείου' SPACE ('Πειραιώς' | 'Πειραιά') |
    'Πλημμελειοδικείου' SPACE ('Πειραιώς' | 'Πειραιά') |
    'Ειρηvoδικείoυ' SPACE 'Αιγίvης' |
    'Ειρηvoδικείoυ' SPACE 'Καλαυρίας' |
    'Ειρηvoδικείoυ' SPACE 'Κυθήρωv' |
    'Ειρηvoδικείoυ' SPACE 'Νίκαιας' |
    'Ειρηvoδικείoυ' SPACE 'Σαλαμίvας' |
    'Ειρηvoδικείoυ' SPACE 'Σπετσώv' |
    'Μον. '? 'Εφετείου' SPACE 'Θεσσαλονίκης'|
    'Πρωτοδικείου' SPACE 'Θεσσαλονίκης' |
    'Ειρηvoδικείoυ' SPACE 'Θεσσαλονίκης' |
    'Πλημμελειοδικείου' SPACE 'Θεσσαλονίκης'|
    'Πταισματoδικείου' SPACE 'Θεσσαλονίκης' |
    'Ειρηvoδικείoυ' SPACE 'Βασιλικώv' |
    'Ειρηvoδικείoυ' SPACE 'Κoυφαλίωv' |
    'Ειρηvoδικείoυ' SPACE 'Λαγκαδά' |
    'Πρωτοδικείου' SPACE 'Βέρoιας' |
    'Ειρηvoδικείoυ' SPACE 'Βέρoιας' |
    'Πταισματoδικείου' SPACE 'Βέρoιας' |
    'Ειρηvoδικείoυ' SPACE 'Αλεξάvδρειας' |
    'Ειρηvoδικείoυ' SPACE 'Νάoυσας' |
    'Πρωτοδικείου' SPACE 'Εδεσσας' |
    'Ειρηvoδικείoυ' SPACE 'Έδεσσας' |
    'Ειρηvoδικείoυ' SPACE 'Αλμωπίας' |
    'Ειρηvoδικείoυ' SPACE 'Σκύδρας' |
    'Πρωτοδικείου' SPACE 'Κατερίvης' |
    'Ειρηvoδικείoυ' SPACE 'Πιερίας' |
    'Πταισματoδικείου' SPACE 'Πιερίας' |
    'Ειρηvoδικείoυ' SPACE 'Κολινδρού' |
    'Πρωτοδικείου' SPACE 'Κιλκίς' |
    'Ειρηvoδικείoυ' SPACE 'Κιλκίς' |
    'Ειρηvoδικείoυ' SPACE 'Πoλυκάστρoυ' |
    'Πρωτοδικείου' SPACE 'Σερρώv' |
    'Ειρηvoδικείoυ' SPACE 'Σερρώv' |
    'Πταισματoδικείου' SPACE 'Σερρώv' |
    'Ειρηvoδικείoυ' SPACE 'Νιγρίτας' |
    'Ειρηvoδικείoυ' SPACE 'Ρoδoλίβoυς' |
    'Ειρηvoδικείoυ' SPACE 'Συvτικής' |
    'Πρωτοδικείου' SPACE 'Χαλκιδικής' |
    'Ειρηvoδικείoυ' SPACE 'Πoλυγύρoυ' |
    'Ειρηvoδικείoυ' SPACE 'Αρvαίας' |
    'Ειρηvoδικείoυ' SPACE 'Κασσάvδρας' |
    'Ειρηvoδικείoυ' SPACE 'Ν. Μουδανιών' |
    'Πρωτοδικείου' SPACE 'Γιαvvιτσώv' |
    'Ειρηvoδικείoυ' SPACE 'Γιαvvιτσώv' |
    'Εφετείου' SPACE 'Κέρκυρας' |
    'Πρωτοδικείου' SPACE 'Κέρκυρας' |
    'Ειρηvoδικείoυ' SPACE 'Κέρκυρας' |
    'Πταισματoδικείου' SPACE 'Κέρκυρας' |
    'Πρωτοδικείου' SPACE 'Θεσπρωτίας' |
    'Ειρηvoδικείoυ' SPACE 'Ηγoυμεvίτσας' |
    'Εφετείου' SPACE 'Θράκης' |
    'Πρωτοδικείου' SPACE 'Ρoδόπης' |
    'Ειρηvoδικείoυ' SPACE 'Κoμoτηvής' |
    'Πταισματoδικείου' SPACE 'Κoμoτηvής' |
    'Πρωτοδικείου' SPACE 'Δράμας' |
    'Ειρηvoδικείoυ' SPACE 'Δράμας' |
    'Πταισματoδικείου' SPACE 'Δράμας' |
    'Πρωτοδικείου' SPACE 'Εβρου' |
    'Ειρηvoδικείoυ' SPACE 'Αλεξαvδρoύπoλης' |
    'Πρωτοδικείου' SPACE 'Καβάλας' |
    'Ειρηvoδικείoυ' SPACE 'Καβάλας' |
    'Πταισματoδικείου' SPACE 'Καβάλας' |
    'Ειρηvoδικείoυ' SPACE 'Θάσoυ' |
    'Ειρηvoδικείoυ' SPACE 'Παγγαίoυ' |
    'Πρωτοδικείου' SPACE 'Ξάvθης' |
    'Ειρηvoδικείoυ' SPACE 'Ξάvθης' |
    'Πρωτοδικείου' SPACE 'Ορεστιάδας' |
    'Ειρηvoδικείoυ' SPACE 'Ορεστιάδας' |
    'Ειρηvoδικείoυ' SPACE 'Διδυμoτείχoυ' |
    'Εφετείου' SPACE 'Iωαvvίvωv' |
    'Πρωτοδικείου' SPACE 'Iωαvvίvωv' |
    'Ειρηvoδικείoυ' SPACE 'Iωαvvίvωv' |
    'Ειρηvoδικείoυ' SPACE 'Κovίτσης' |
    'Πρωτοδικείου' SPACE 'Αρτας'|
    'Ειρηνοδικείου' SPACE 'Αρτας'|
    'Πταισματoδικείου' SPACE 'Αρτας' |
    'Πρωτοδικείου' SPACE 'Πρέβεζας'|
    'Ειρηνοδικείου' SPACE 'Πρέβεζας'|
    'Εφετείου' SPACE ('Δωδεκαvήσoυ' | 'Δωδεκανήσου') |
    'Πρωτοδικείου' SPACE 'Ρόδoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ρόδoυ' |
    'Πταισματoδικείου' SPACE 'Ρόδoυ' |
    'Ειρηvoδικείoυ' SPACE 'Καρπάθoυ' |
    'Πρωτοδικείου' SPACE 'Κω' |
    'Ειρηvoδικείoυ' SPACE 'Κω' |
    'Ειρηvoδικείoυ' SPACE 'Καλύμvoυ' |
    'Ειρηvoδικείoυ' SPACE 'Λέρoυ' |
    'Εφετείου' SPACE 'Αιγαίoυ' |
    'Πρωτοδικείου' SPACE 'Σύρoυ' |
    'Ειρηvoδικείoυ' SPACE 'Αvδρoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ερμoύπoλης' |
    'Ειρηvoδικείoυ' SPACE 'Μήλoυ' |
    'Ειρηvoδικείoυ' SPACE 'Μυκόvoυ' |
    'Ειρηvoδικείoυ' SPACE 'Πάρoυ' |
    'Ειρηvoδικείoυ' SPACE 'Τήvoυ' |
    'Πρωτοδικείου' SPACE 'Σάμoυ' |
    'Ειρηvoδικείoυ' SPACE 'Σάμoυ' |
    'Ειρηvoδικείoυ' SPACE 'Iκαρίας' |
    'Ειρηvoδικείoυ' SPACE 'Καρλoβασίoυ' |
    'Πρωτοδικείου' SPACE 'Νάξου' |
    'Ειρηvoδικείoυ' SPACE 'Νάξoυ' |
    'Ειρηvoδικείoυ' SPACE 'Θήρας' |
    'Εφετείου' SPACE 'Κρήτης' |
    'Πρωτοδικείου' SPACE 'Χαvίωv' |
    'Ειρηvoδικείoυ' SPACE 'Χαvίωv' |
    'Πταισματoδικείου' SPACE 'Χαvίωv' |
    'Ειρηvoδικείoυ' SPACE 'Βάμoυ' |
    'Πρωτοδικείου' SPACE 'Ρεθύμvης' |
    'Ειρηvoδικείoυ' SPACE 'Ρεθύμvης' |
    'Πταισματoδικείου' SPACE 'Ρεθύμvης' |
    'Εφετείου' SPACE 'Δυτ. Μακεδονίας' |
    'Πρωτοδικείου' SPACE 'Κoζάvης' |
    'Ειρηvoδικείoυ' SPACE 'Κoζάvης' |
    'Πταισματoδικείου' SPACE 'Κoζάvης' |
    'Ειρηvoδικείoυ' SPACE 'Εoρδαίας' |
    'Πρωτοδικείου' SPACE 'Γρεβεvώv' |
    'Ειρηvoδικείoυ' SPACE 'Γρεβεvώv' |
    'Πρωτοδικείου' SPACE 'Καστοριάς' |
    'Ειρηvoδικείoυ' SPACE 'Καστoριάς' |
    'Πταισματoδικείου' SPACE 'Κλεισούρας' |
    'Πρωτοδικείου' SPACE 'Φλώριvας' |
    'Ειρηvoδικείoυ' SPACE 'Φλώριvας' |
    'Ειρηvoδικείoυ' SPACE 'Αμυvταίoυ' |
    'Εφετείου' SPACE 'Λάρισας' |
    'Πρωτοδικείου' SPACE 'Λάρισας' |
    'Ειρηvoδικείoυ' SPACE 'Λάρισας' |
    'Πταισματoδικείου' SPACE 'Λάρισας' |
    'Ειρηvoδικείoυ' SPACE 'Ελασσόvας' |
    'Πταισματoδικείου' SPACE 'Ελασσόvας' |
    'Ειρηvoδικείoυ' SPACE 'Φαρσάλων' |
    'Πρωτοδικείου' SPACE 'Βόλoυ' |
    'Ειρηvoδικείoυ' SPACE 'Βόλoυ' |
    'Πταισματoδικείου' SPACE 'Βόλoυ' |
    'Ειρηvoδικείoυ' SPACE 'Αλμυρoύ' |
    'Ειρηvoδικείoυ' SPACE 'Σκοπέλου' |
    'Πρωτοδικείου' SPACE 'Καρδίτσας' |
    'Ειρηvoδικείoυ' SPACE 'Καρδίτσας' |
    'Πταισματoδικείου' SPACE 'Καρδίτσας' |
    'Πρωτοδικείου' SPACE 'Τρικάλωv' |
    'Ειρηvoδικείoυ' SPACE 'Τρικάλωv' |
    'Πταισματoδικείου' SPACE 'Τρικάλωv' |
    'Ειρηvoδικείoυ' SPACE 'Καλαμπάκας' |
    'Εφετείου' SPACE 'Ναυπλίoυ' |
    'Πρωτοδικείου' SPACE 'Ναυπλίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ναυπλίoυ' |
    'Πταισματoδικείου' SPACE 'Ναυπλίoυ' |
    'Πταισματoδικείου' SPACE 'Αργoυς' |
    'Ειρηvoδικείoυ' SPACE 'Αργoυς ' |
    'Ειρηvoδικείoυ' SPACE 'Αστρoυς' |
    'Ειρηvoδικείoυ' SPACE 'Μάσσητoς' |
    'Πρωτοδικείου' SPACE 'Κoρίvθoυ' |
    'Ειρηvoδικείoυ' SPACE 'Κoρίvθoυ' |
    'Πταισματoδικείου' SPACE 'Κoρίvθoυ' |
    'Ειρηvoδικείoυ' SPACE 'Σικυώvoς' |
    'Πταισματoδικείου' SPACE 'Σικυώvoς' |
    'Ειρηvoδικείoυ' SPACE 'Νεμέας' |
    'Ειρηvoδικείoυ' SPACE 'Ξυλoκάστρoυ' |
    'Πρωτοδικείου' SPACE 'Σπάρτης' |
    'Ειρηvoδικείoυ' SPACE 'Σπάρτης' |
    'Πταισματoδικείου' SPACE 'Σπάρτης' |
    'Ειρηvoδικείoυ' SPACE 'Επιδαύρoυ-Λιμηράς' |
    'Πρωτοδικείου' SPACE 'Τρίπoλης' |
    'Ειρηvoδικείoυ' SPACE 'Τρίπoλης' |
    'Πταισματoδικείου' SPACE 'Τρίπoλης' |
    'Ειρηvoδικείoυ' SPACE 'Μεγαλόπολης' |
    'Ειρηvoδικείoυ' SPACE 'Ψωφίδoς' |
    'Εφετείου' SPACE 'Καλαμάτας' |
    'Πρωτοδικείου' SPACE 'Καλαμάτας' |
    'Ειρηvoδικείoυ' SPACE 'Καλαμάτας' |
    'Πταισματoδικείου' SPACE 'Καλαμάτας' |
    'Ειρηvoδικείoυ' SPACE 'Πύλου' |
    'Πρωτοδικείου' SPACE 'Κυπαρισσίας' |
    'Ειρηvoδικείoυ' SPACE 'Κυπαρισσίας' |
    'Ειρηvoδικείoυ' SPACE 'Πλαταμώδους' |
    'Πρωτοδικείου' SPACE 'Γυθείου' |
    'Ειρηvoδικείoυ' SPACE 'Γυθείου' |
    'Ειρηvoδικείoυ' SPACE 'Νεαπόλεως' SPACE 'Βοιών' |
    'Εφετείου' SPACE 'Πατρώv' |
    'Εφετείου' SPACE 'Πατρών'|  //κάποιος χαρακτήρας διαφορετικός unicode
    'Πρωτοδικείου' SPACE 'Πατρώv' |
    'Ειρηvoδικείoυ' SPACE 'Πατρώv' |
    'Πταισματoδικείου' SPACE 'Πατρώv' |
    'Ειρηvoδικείoυ' SPACE 'Δύμης' |
    'Πρωτοδικείου' SPACE 'Αιγίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Αιγιαλείας' |
    'Πταισματoδικείου' SPACE 'Αιγιαλείας' |
    'Πρωτοδικείου' SPACE 'Καλαβρύτωv' |
    'Ειρηvoδικείoυ' SPACE 'Καλαβρύτωv' |
    'Ειρηvoδικείoυ' SPACE 'Ακράτας' |
    'Πρωτοδικείου' SPACE 'Ηλείας' |
    'Ειρηvoδικείoυ' SPACE 'Πύργoυ' |
    'Πταισματoδικείου' SPACE 'Πύργoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ολυμπίωv' |
    'Ειρηvoδικείoυ' SPACE 'Αρήvης' |
    'Πρωτοδικείου' SPACE 'Αμαλιάδας' |
    'Ειρηvoδικείoυ' SPACE 'Αμαλιάδας' |
    'Πταισματoδικείου' SPACE 'Αμαλιάδας' |
    'Ειρηvoδικείoυ' SPACE 'Γαστoύvης' |
    'Ειρηvoδικείoυ' SPACE 'Μυρτoυvτίωv' |
    'Πρωτοδικείου' SPACE 'Ζακύvθoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ζακύvθoυ' |
    'Πρωτοδικείου' SPACE 'Κεφαλληvίας' |
    'Ειρηvoδικείoυ' SPACE 'Αργoστoλίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Σαμαίωv' |
    'Εφετείου' SPACE 'Δυτ. Στερεάς' |
    'Πρωτοδικείου' SPACE 'Αγριvίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Αγριvίoυ' |
    'Πταισματoδικείου' SPACE 'Αγριvίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Βάλτoυ' |
    'Πταισματoδικείου' SPACE 'Βάλτoυ' |
    'Πρωτοδικείου' SPACE 'Λευκάδας' |
    'Ειρηvoδικείoυ' SPACE 'Λευκάδας' |
    'Ειρηvoδικείoυ' SPACE 'Βovίτσας' |
    'Πρωτοδικείου' SPACE 'Μεσoλoγγίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Μεσoλoγγίoυ' |
    'Πταισματoδικείου' SPACE 'Μεσoλoγγίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ναυπάκτoυ' |
    'Εφετείου' SPACE 'Βορείου Αιγαίου' |
    'Πρωτοδικείου' SPACE 'Μυτιλήvης' |
    'Ειρηvoδικείoυ' SPACE 'Μυτιλήvης' |
    'Πταισματoδικείου' SPACE 'Μυτιλήvης' |
    'Ειρηvoδικείoυ' SPACE 'Καλλovής' |
    'Πταισματoδικείου' SPACE 'Λήμvoυ' |
    'Πταισματoδικείου' SPACE 'Πλωμαρίoυ' |
    'Πρωτοδικείου' SPACE 'Χίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Χίoυ' |
    'Εφετείου' SPACE 'Αν. Κρήτης' |
    'Πρωτοδικείου' SPACE 'Ηρακλείoυ' |
    'Ειρηvoδικείoυ' SPACE 'Ηρακλείoυ' |
    'Πταισματoδικείου' SPACE 'Ηρακλείoυ' |
    'Ειρηvoδικείoυ' SPACE 'Καστελίoυ - Πεδιάδoς' |
    'Πταισματoδικείου' SPACE 'Μoιρώv' |
    'Πταισματoδικείου' SPACE 'Πύργoυ Κρήτης' |
    'Πρωτοδικείου' SPACE 'Λασιθίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Λασιθίoυ' |
    'Ειρηvoδικείoυ' SPACE 'Iεράπετρας' |
    'Ειρηvoδικείoυ' SPACE 'Σητείας' |
    'Εφετείου' SPACE 'Ευβοίας' |
    'Πρωτοδικείου' SPACE 'Θηβώv' |
    'Ειρηvoδικείoυ' SPACE 'Θηβώv' |
    'Πταισματoδικείου' SPACE 'Θηβώv' |
    'Πρωτοδικείου' SPACE 'Χαλκίδας' |
    'Ειρηvoδικείoυ' SPACE 'Χαλκίδας' |
    'Πταισματoδικείου' SPACE 'Χαλκίδας' |
    'Ειρηvoδικείoυ' SPACE 'Iστιαίας' |
    'Ειρηvoδικείoυ' SPACE 'Καρύστoυ' |
    'Ειρηvoδικείoυ' SPACE 'Κύμης' |
    'Ειρηvoδικείoυ' SPACE 'Ταμιvέωv' |
    'Α.Ε.Δ.'
    );
    */

//Θέλουμε όλα τα Υπουργεία (παλαιά και νέα καθώς references γίνονται και σε Υπουργεία με την παλιά τους ονομασία)
/*fragment GREEK_MINISTRY :
    'Υπουργείου' SPACE 'Εσωτερικών' | 'Υπ. Εσωτερικών' |
    'Υπουργείου' SPACE 'Οικονοµίας' SPACE 'Ανταγωνιστικότητας' SPACE 'και' SPACE 'Ναυτιλίας' |
    'Υπουργείου' SPACE 'Δημόσιας' SPACE 'Τάξης' SPACE 'και' SPACE 'Προστασίας' SPACE 'του' 'Πολίτη' |
    'Εθνικής' SPACE 'Άμυνας' |
    'Δημόσιας' SPACE 'Τάξης' |
    'ΓΕΑ' |
    'ΥΦΕΘΑ' |
    'ΥΕΘΑ' |
    'ΑΝΥΕΘΑ' |
    'ΓΕΕΘΑ'
    ;
*/
//Χρειαζόμαστε το σύνολο των φορέων που δημιουργούν εγκυκλίους
/*fragment FOREIS :
    'Ε.Τ.Α.Α.' SPACE* HYPHEN SPACE 'Τ.Α.Ν.' |
    'ΕΤΑΑ' HYPHEN 'ΤΑΝ' | 'ΕΤΑΑ' SPACE* HYPHEN SPACE* 'ΤΑΝ'|
    'Ελληνικής' SPACE 'Αστυνομίας' |
    'ΕΛΑΣ' |
    'του' SPACE 'Δ.Ο.Α.Τ.Α.Π.' |
    'Διεπιστημoνικού' SPACE 'Οργανισμού' SPACE 'Αναγνώρισης' SPACE 'Τίτλων' SPACE 'Ακαδημαϊκών' SPACE 'και' SPACE 'Πληροφόρησης'|
    'Αρχής' SPACE 'Προστασίας' SPACE 'Προσωπικών' SPACE 'Δεδομένων'
    ;
*/