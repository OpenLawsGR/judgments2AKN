grammar LegalOpinion;

akomaNtoso : judgment EOF;

//------------------------------- JUDGMENT --------------------------------------------------//
judgment : header judgmentBody conclusions?;

header : personalLegalOpinion? caseNmuber? docProponent? headerPar+;
judgmentBody : introduction? (background motivation decision | background_alt motivation decision);

//------------------------------- HEADER --------------------------------------------------//
personalLegalOpinion: (PERSONAL SPACE LEGAL_OPINION | LEGAL_OPINION SPACE BRACKET PERSONAL BRACKET) (NEXT_LINE | SPACE);
caseNmuber:
    (NUMBER_TEXT SPACE docType SPACE? ANO_KATO? SPACE? |
    docType (SPACE NUMBER_TEXT)? SPACE |
    NUMBER_TEXT SPACE)
        docNumber NEXT_LINE
    ;

docType: LEGAL_OPINION;
docNumber: NUM SPACE? SLASH SPACE? NUM;
docProponent: (OF SPACE)? NSK (SPACE BRACKET TMHMA_TEXT SPACE TMIMA_ID BRACKET)? NEXT_LINE;
headerPar :
    (PAR | BRACKET | ALL_CHARS | SPECIAL_CHARS |
    SPACE | COMMA | NUMBER_TEXT | NUM | HYPHEN |
    SLASH  | ANO_KATO | EMBEDDED_TEXT | OF | CONCLUSTION_START|
    TMIMA_ID | TMHMA_TEXT | APOSTROPHE | NSK | PAR_2 | PERSONAL)+ NEXT_LINE*
    ;

questionInfo: QUESTION_NUM (BRACKET | ALL_CHARS | SPECIAL_CHARS |
                           SPACE | COMMA | NUMBER_TEXT | NUM | HYPHEN |
                           SLASH  | ANO_KATO | EMBEDDED_TEXT | OF |
                           TMIMA_ID | TMHMA_TEXT | NSK|
                           PAR| APOSTROPHE | LEGAL_OPINION | NEXT_LINE)+
                           NEXT_LINE?;

headerLastPar: BASE_ON_QUESTIONS (ALL_CHARS | SPACE | COMMA | NUMBER_TEXT |
                                  ANO_KATO | TMIMA_ID | OF| NEXT_LINE | NSK | BRACKET |
                                  APOSTROPHE | NUM | SPECIAL_CHARS | SLASH | LEGAL_OPINION|
                                  HYPHEN | EMBEDDED_TEXT)+;
//------------------------------- END HEADER --------------------------------------------------//

// ------------------------------- judgmentBody --------------------------------------------//
//------------------------------ background ---------------------------------//
introduction: questionInfo+ headerLastPar*;
background: backgroundDivision;
backgroundDivision: backgroundDivisionHeading alinea? backgroundDivisionParagraph*;
//backgroundDivision: heading backgroundDivisionParagraph+;
backgroundDivisionHeading: SECTIONS_DIVISION ;
backgroundDivisionParagraph: backgroundDivisionParagraphNum SPACE? content;
backgroundDivisionParagraphNum: PAR | PAR_2;
//backgroundDivisionAlinea: backgroundDivisionAlineaContent;
//backgroundDivisionAlineaContent: contentPar;
alinea:content;

//alineaContent: content;
content: contentPar;
contentPar:
    (ALL_CHARS | SPECIAL_CHARS | SPACE | COMMA | SLASH | NUM |
    NEXT_LINE | HYPHEN | NUMBER_TEXT| EMBEDDED_TEXT |
    ANO_KATO | BRACKET | LEGAL_OPINION |
    OF | APOSTROPHE | TMIMA_ID | NSK | BASE_ON_QUESTIONS |PERSONAL)+;

//This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
background_alt: backgroundDivision_alt;
backgroundDivision_alt: backgroundDivisionHeading_alt alinea? backgroundDivisionParagraph_alt*;
backgroundDivisionHeading_alt: PAR_2;
backgroundDivisionParagraph_alt: PAR SPACE? content;
//------------------------------ END background ---------------------------------//

//------------------------------ motivation ---------------------------------//
motivation : motivationDivision+ | motivationDivision_alt+;
motivationDivision : motivationHeading alinea? motivationDivisionParagraph*;
motivationHeading : SECTIONS_DIVISION ;
motivationDivisionParagraph: motivParNum SPACE? content;
motivParNum: PAR | PAR_2;
//alinea: alineaContent;

//This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
//motivation_alt: motivationDivision_alt+;
motivationDivision_alt: motivationHeading_alt alinea? motivationDivisionParagraph_alt*;
motivationHeading_alt: PAR_2;
motivationDivisionParagraph_alt: motivParNum_alt SPACE? content;
motivParNum_alt: PAR;
//------------------------------ END motivation ---------------------------------//

//------------------------------ decision -----------------------------------//
decision : decisionDivision | decisionDivision_alt;
decisionDivision : decisionHeading alinea? decisionDivisionParagraph*;
decisionHeading: SECTIONS_DIVISION ;
//decisionDivisionParagraph: backgroundDivisionParagraphNum? decisionContent;
decisionDivisionParagraph: backgroundDivisionParagraphNum SPACE? decisionContent;
decisionContent: decisionContentPar;

decisionContentPar: (ALL_CHARS | SPECIAL_CHARS | SPACE | COMMA | SLASH | NUM |
                     NEXT_LINE | HYPHEN | NUMBER_TEXT| EMBEDDED_TEXT |
                     ANO_KATO | BRACKET | LEGAL_OPINION | SECTIONS_DIVISION|
                     OF | APOSTROPHE | TMIMA_ID | NSK | BASE_ON_QUESTIONS)+;

//This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
//decision_alt: decisionDivision_alt;
decisionDivision_alt: decisionHeading_alt alinea? decisionDivisionParagraph_alt*;
decisionHeading_alt: PAR_2;
decisionDivisionParagraph_alt: motivParNum_alt SPACE? content;
//------------------------------ END decision -----------------------------------//
//-------------------------------END judgmentBody ---------------------------------//

//------------------------------ conclusions ---------------------------------//
conclusions: conclusionStart conclusionPar+;
conclusionStart: NEXT_LINE CONCLUSTION_START NEXT_LINE;
conclusionPar: headerPar;

//------------------------------ END conclusions ---------------------------------//
//------------------------------- END JUDGMENT --------------------------------------------------//


//------------------------------------TOKENS---------------------------------------------------------------------//
CONCLUSTION_START:
    'ΘΕΩΡΗΘΗΚΕ' |
    'ΘΕΩΡΗΘΗΚΕ Ο ΕΙΣΗΓΗΤΗΣ' |
    'ΘΕΩΡΗΘΗΚΕ Ο Εισηγητής' |
    'Θεωρήθηκε' |
    'ΘΕΩΡΗΘΗΚΕ' |
    'Ο Γνωμοδοτών' | 'Ο ΓΝΩΜΟΔΟΤΩΝ' |
    'Αθήνα' SPACE (NUM HYPHEN?)+
    ;

PAR :
    NEXT_LINE NUM DOT HYPHEN? SPACE //|
    //NEXT_LINE LOWER DOT HYPHEN? SPACE
    ;

PAR_2: NEXT_LINE UPPER DOT HYPHEN? SPACE;

SECTIONS_DIVISION:
    NEXT_LINE LATIN DOT SPACE?
        (HISTORY_HEADER |
        DECISION_HEADER |
        MOTIVATION_HEADER)
            DOT? |
    NEXT_LINE LATIN DOT SPACE? |
    HISTORY_HEADER |
    DECISION_HEADER |
    MOTIVATION_HEADER
    ;

//SECTIONS_DIVISION_ALT: PAR;

//BACKGR_DIV_HEADING : SECTION_DIVISION SPACE? (HISTORY_HEADER | DECISION_HEADER) DOT? | SECTION_DIVISION | HISTORY_HEADER | DECISION_HEADER;
//MOTIV_DIV_HEADING :  SECTION_DIVISION SPACE? MOTIVATION_HEADER? | MOTIVATION_HEADER | SECTION_DIVISION;
//DECISION_DIV_HEADING: SECTION_DIVISION SPACE? ?;
//SECTION_DIVISION : NEXT_LINE LATIN DOT SPACE? NEXT_LINE?;

EMBEDDED_TEXT: '"'.*?'"' | '«'.*?~('@')'»' | '“'.*?'”';
PERSONAL: 'ΑΤΟΜΙΚΗ' | 'Ατομική';
NUMBER_TEXT:
    'Αριθμός' |
    'υπ΄αριθ' DOT |
    'Aριθμός' |
    'Αριθµός' |
    'ΑΡΙΘΜΟΣ' |
    'υπ’' SPACE 'αριθμ' DOT |
    'Αριθµ' DOT |
    'Αριθμ' DOT |
    'Αρ' DOT
    ;

LEGAL_OPINION:
    'ΓΝΩΜΟΔΟΤΗΣΗ' |
    'ΓΝΩΜΟΔΟΤΗΣHΣ' |
    'ΓΝΩΜΟΔΟΤΗΣΗΣ' |
    'Γνωμοδότησης' |
    'Γνωμοδότηση' |
    'Γνωμοδοτήσεως' |
    'Γνωµοδοτήσεως' |
    'γνωμοδότησης'
    ;

OF: 'ΤΟΥ' | 'του' | 'ΤΟ' | 'Το';
NSK:
    ('ΝΟΜΙΚΟ' SPACE 'ΣΥΜΒΟΥΛΙΟ' | 'ΝΟΜΙΚΟΥ' SPACE 'ΣΥΜΒΟΥΛΙΟΥ') SPACE OF SPACE 'ΚΡΑΤΟΥΣ' |
    'Νομικό' SPACE 'Συμβούλιο' SPACE OF SPACE 'Κράτους'
;


HISTORY_HEADER:
    'Ιστορικό' DOT? |
    'ΙΣΤΟΡΙΚΟ' DOT? |
    'ΙΣΤΟΡΙΚΟ ΤΗΣ ΥΠΟΘΕΣΗΣ' |
    'ΙΣΤΟΡΙΚΟ ΚΑΙ ΓΝΩΜΟΔΟΤΗΣΗ ΝΣΚ' SPACE NUM SLASH NUM |
    'Σύντομο' SPACE 'Ιστορικό' |
    'ΔΟΘΕΝ' SPACE 'ΙΣΤΟΡΙΚΟ'
    ;

MOTIVATION_HEADER:
    'Εφαρμοστέες διατάξεις' |
    'Σχετικές διατάξεις' |
    '- ΚΡΙΣΙΜΕΣ ΔΙΑΤΑΞΕΙΣ' DOT?|
    'ΚΡΙΣΙΜΕΣ ΔΙΑΤΑΞΕΙΣ' DOT?|
    'Κρίσιμες διατάξεις' |
    'Ερμηνεία της διάταξης - Υπαγωγή' |
    'Ερμηνεία των διατάξεων' DOT?|
    'ΕΡΜΗΝΕΙΑ ΤΩΝ ΔΙΑΤΑΞΕΩΝ' |
    'Ερμηνεία και εφαρμογή διατάξεων' |
    'Ερμηνεία και εφαρμογή των διατάξεων' |
    'Ερμηνεία διατάξεων' |
    'ΕΡΜΗΝΕΙΑ ΚΑΙ ΕΦΑΡΜΟΓΗ ΤΩΝ ΔΙΑΤΑΞΕΩΝ' |
    'Νομοθετικό πλαίσιο' DOT?|
    'Νομοθετικό Πλαίσιο' DOT?|
    'Nομοθετικό πλαίσιο' DOT?|
    'ΝΟΜΟΘΕΤΙΚΟ ΠΛΑΙΣΙΟ' DOT?|
    'ΝΟΜΙΚΟΠΛΑΙΣΙΟ' DOT |
    'Ανάλυση' |
    'ΤΟ ΚΟΙΝΟΤΙΚΟ, ΕΘΝΙΚΟ KAI ΕΙΔΙΚΟ ΝΟΜΙΚΟ ΠΛΑΙΣΙΟ ΤΗΣ' (NEXT_LINE | SPACE) 'ΥΠΟΘΕΣΗΣ' |
    'ΤΑ ΕΡΩΤΗΜΑΤΑ' |
    'ΤΕΘΕΝΤΑ ΕΡΩΤΗΜΑΤΑ' |
    'ΤΟ EΝΩΣΙΑΚΟ ΚΑΙ ΕΘΝΙΚΟ ΝΟΜΟΘΕΤΙΚΟ ΚΑΙ ΝΟΜΟΛΟΓΙΑΚΟ ΠΛΑΙΣΙΟ' |
    'ΕΡΜΗΝΕΙΑ – ΥΠΑΓΩΓΗ' |
    'ΝΟΜΙΚΟ ΠΛΑΙΣΙΟ ΤΗΣ ΥΠΟΘΕΣΗΣ' |
    'ΣΥΜΠΕΡΑΣΜΑTA' |
    'ΣΥΜΠΕΡΑΣΜΑΤΑ' |
    'ΣΥΜΠΕΡΑΣΜΑ' |
    'Συμπέρασμα' |
    'ΤΟ ΕΙΔΙΚΟ ΝΟΜΙΚΟ ΠΛΑΙΣΙΟ'
    ;

DECISION_HEADER:
    '- Απάντηση' |
    'Απάντηση' |
    'ΑΠΑΝΤΗΣΕΙΣ' |
    'ΑΠΑΝΤΗΣΗ'
    ;

BASE_ON_QUESTIONS:
    'Επί' SPACE 'των' SPACE 'ερωτημάτων' |
    'Επί' SPACE OF SPACE 'ανωτέρω' SPACE 'ερωτήματος' |
    'Επί' SPACE OF SPACE 'ως' SPACE 'άνω' SPACE 'ερωτήματος' |
    'Επί' SPACE OF SPACE 'ερωτήματος' |
    'Επί' SPACE 'των' SPACE 'ανωτέρω' SPACE 'ερωτημάτων' |
    'Επί' SPACE OF SPACE 'παραπάνω' SPACE 'ερωτήματος' |
    'Επί' SPACE 'των' SPACE 'ως' SPACE 'άνω' SPACE 'ερωτημάτων' |
    'Επί' SPACE 'των' SPACE 'ως' SPACE 'άνω' SPACE 'ερωτηµάτων'
    ;

QUESTION_NUM:
    NUMBER_TEXT SPACE ('Ερωτήματος' | 'Ερωτήµατος' | 'ερωτήματος' | 'ΕΡΩΤΗΜΑΤΟΣ') SPACE? ANO_KATO |
    NUMBER_TEXT SPACE ANO_KATO |
    'Ερώτημα' SPACE? ANO_KATO |
    ('Περίληψη' | 'ΠΕΡΙΛΗΨΗ') SPACE ('ερωτήματος' | 'Ερωτήματος' | 'Ερωτήµατος' | 'ερωτημάτων' | 'ΕΡΩΤΗΜΑΤΟΣ') SPACE? ANO_KATO |
    'Περίληψη' SPACE? ANO_KATO |
    'Έγγραφο' SPACE 'Ερωτήματος' SPACE? ANO_KATO |
    'Ερωτάται' ANO_KATO |
    'Αριθμός' SPACE 'Eρωτήματος' |
    'Περίληψη' SPACE 'Ερωτημάτων' |
    'Θέμα' SPACE '(περίληψη ερωτήματος)'
    ;

NUM : [0-9]+ ;
SLASH : '/';

COMMA : ',';
NEXT_LINE: '\n';
BRACKET: '(' | ')';
HYPHEN: ('-' | '–' | '−');
//LATIN : 'Ι' | 'ΙΙ' | 'II' | 'ΙΙΙ' | 'ΙV' | 'IV' | 'V';
ANO_KATO: ':';
TMHMA_TEXT: 'ΤΜΗΜΑ';
TMIMA_ID: ('Α' | 'Β' | 'Γ'  | 'Δ' | 'Ε' | 'ΣΤ') APOSTROPHE;
APOSTROPHE: [’΄'`´ʽ‘ʹ];
ALL_CHARS : ([Α-Ωα-ωάέήίόύϋώϊΐΆΈΉΊΌΎΏΪ] | [A-Za-z] | [üéâşţöí] | '∆' | 'Ω' | 'Т' | 'Е' | 'µ' |'×' )+;
SPECIAL_CHARS: (
    '¶' | '$' |
    '·' | '•' | '°' | '·'|
    '…' |
    '%' | '{' | '}' |
    '!' |
    '.'| '¾' | '²' | '½' |
    ']' | '[' | '¦' |
    '+' | '-' | '–' | '¬' | '−' |
    '?' | '‐'| '_'| '£' |
    '€' | '*' | '@' | '=' |
    '\\' | '/' | '‰' | '^' |
    '&' | '>' | '<' | '~' | '¼' |
    '§' | '“' | '”' | '»' | [|] |
    '"' | '¨' | '«' | ';' | '#' |
    ''
);

SPACE : ([\r\t ] | ' ')+ ;

//-------------------------------------FRAGMENTS-------------------------------------------------//
fragment UPPER: ('Α' | 'Β' | 'Γ' | 'Δ' | 'Ε' | 'E' | 'ΣΤ') ;
fragment LATIN: 'Ι' | 'I' | 'ΙΙ' | 'II' | 'ΙI' | 'ΙΙΙ' | 'IΙΙ' | 'III' | 'ΙV' | 'IV' | 'V' | 'VI' | 'VII'  ;
fragment LOWER: 'α' | 'β' | 'γ' | 'δ' | 'ε' | 'στ';
fragment DOT : '.';