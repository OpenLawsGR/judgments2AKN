# -*- coding: utf-8 -*-
import datetime
import logging
from functions import *
from lxml import etree
from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.RuleContext import RuleContext

from grammars.gen.CouncilOfStateLexer import CouncilOfStateLexer
from grammars.gen.CouncilOfStateParser import CouncilOfStateParser
from grammars.gen.CouncilOfStateListener import CouncilOfStateListener

from grammars.gen.SupremeCourtLexer import SupremeCourtLexer
from grammars.gen.SupremeCourtParser import SupremeCourtParser
from grammars.gen.SupremeCourtListener import SupremeCourtListener

from grammars.gen.LegalOpinionLexer import LegalOpinionLexer
from grammars.gen.LegalOpinionParser import LegalOpinionParser
from grammars.gen.LegalOpinionListener import LegalOpinionListener


# get Logger
Akn_LOGGER = logging.getLogger('Akn_LOGGER')

global href_base
href_base = "/akn/gr/"

global judgment_href
judgment_href = "/akn/gr/judgment/"
        
class AknJudgementXML(LegalOpinionListener, CouncilOfStateListener, SupremeCourtListener):
    """This is an AkomaNtoso class that inherits from Listeners according
    to legal document type. It is based on grammars to construct the structure
    of judgments in XML format. It also includes methods to construct metadata
    and other elements based on AkomaNtoso principles.
    """
    def __init__(self, textType = None, author = None,
                 foreas = None, issueYear=None, decisionNumber = None,
                 ECLI = None, publicationDate = None, ada = None,
                 status = None, summary = None, keywords = None,
                 chairman = None, rapporteur = None):
        
        """Constructor of an instance

        Args:
            textType: legal text type (judgment etc.) that is used to construct
                meta -> identification node
            author: issuing authority of legal text (Council of State etc.)
            foreas: name reference of issuing authority
            issueYear: issuing year of legal text
            decisionNumber: The id of the legal text based on numbering made by the authority
                It is used to construct the FRBR uri
            ECLI: The European Case Law Identifier of the legal text
            publicationDate: date of judgment publication
            ada: Id that is used in diavgeia site (for legal texts that are published in diavgeia)
            status: If the legal text has been accepted, declined etc. (used in advisory opinions)
            summary: summary of the legal decision (advisory opinions)
            keywords: keywords that may be found in legal decision (advisory opinions)
            chairman: chairman on conference date (advisory opinions)
            rapporteur: the rapporteur of the advisory opinion
        """
        
        Akn_LOGGER.info("initialiazing AknJudgmentXmlListener Object...")
        global division_eId
        global division_para_eId
        self.text = ""
        self.itemCounter = 0
        self.motivationCounter = 0
        self.divisionCounter = 0
        self.divisionParagraph = 0
        self.attrQName = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        self.schemaLocation = "http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd"
        self.nsmap = {
            None : "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            'xsi' : "http://www.w3.org/2001/XMLSchema-instance"
            }
        #self.xmlns = 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'
        self.textType = textType
        self.author = author
        self.foreas = foreas
        self.issueYear = issueYear
        self.decisionNumber = decisionNumber
        self.ECLI = ECLI
        self.publicationDate = publicationDate
        self.ada = ada
        self.status = status
        self.summary = summary
        self.keywords = keywords
        self.chairman = chairman
        self.rapporteur = rapporteur
        self.creator = "#openLawsGR"
        Akn_LOGGER.debug("textType: %s", self.textType)
        Akn_LOGGER.debug("author: %s", self.author)
        Akn_LOGGER.debug("foreas: %s", self.foreas)
        Akn_LOGGER.debug("issueYear: %s", self.issueYear)
        Akn_LOGGER.debug("decisionNumber: %s", self.decisionNumber)
        Akn_LOGGER.debug("ECLI: %s", self.ECLI)
        Akn_LOGGER.debug("publicationDate: %s", self.publicationDate)
        Akn_LOGGER.debug("ada: %s", self.ada)
        Akn_LOGGER.debug("status: %s", self.status)
        Akn_LOGGER.debug("summary: %s", self.summary)
        if self.keywords:
            for keyword in self.keywords:
                Akn_LOGGER.debug("keyword: %s", keyword)
        Akn_LOGGER.debug("chairman: %s", self.chairman)
        Akn_LOGGER.debug("rapporteur: %s", self.rapporteur)

        
    def createAkomaNtosoRoot(self):
        """This method creates the <<AkomaNtoso>> root element 

        Args:
            self: The object itself

        Returns:
            lxml element 
        """
        #print("Creating AkomaNtoso Element...")
        Akn_LOGGER.info("Creating AkomaNtoso Element...")
        akomaNtoso = etree.Element("akomaNtoso", nsmap=self.nsmap)
        akomaNtoso.set(self.attrQName, self.schemaLocation)
        return akomaNtoso
        
    def createMeta(self):
        """This method creates the <<meta>> element of AkomaNtoso's judgment
        node. It is based on extra methods to construct an XML node 

        Args:
            self: The object itself

        Returns:
            lxml <<meta>> element 
        """
        #print("Creating meta Element...")
        Akn_LOGGER.info("Creating meta Element...")
        meta = etree.Element("meta")
        identification = self.createIdentification()
        meta.append(identification)
        
        if self.textType == 'judgment/advisoryOpinion' :
            publication = self.createPublication()
            meta.append(publication)

            classification = self.createClassification()
            meta.append(classification)
            
        lifecycle = self.createLifecycle()
        meta.append(lifecycle)

        if self.textType == 'judgment' :
            workflow = self.createWorkflow()
            meta.append(workflow)

        references =  self.createReferences()
        meta.append(references)
        
        if self.textType == 'judgment/advisoryOpinion' :
            proprietary = self.createProprietary()
            meta.append(proprietary)

        #print(etree.tostring(meta,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
        return meta

    def createIdentification(self):
        """This method creates the <<identification>> element of AkomaNtoso's meta node.
        It is based on methods createFRBRWork, createFRBRExpression, createFRBRManifestation
        to construct an XML node 

        Args:
            self: The object itself

        Returns:
            lxml <<identification>> element
        """
        #print("Creating identification Element...")
        Akn_LOGGER.info("Creating identification Element...")
        identification = etree.Element("identification", attrib={"source" : self.creator})
        FRBRWork = self.createFRBRWork()
        FRBRExpression = self.createFRBRExpression()
        FRBRManifestation = self.createFRBRManifestation()
        identification.append(FRBRWork)
        identification.append(FRBRExpression)
        identification.append(FRBRManifestation)

        #print(etree.tostring(identification,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return identification
    
    def createFRBRWork(self):
        """This method creates the <<FRBRWork>> element of AkomaNtoso's
        identification node

        Args:
            self: The object itself

        Returns:
            lxml <<FRBRWork>> element 
        """
        #print("Creating FRBRWork Element...")
        Akn_LOGGER.info("Creating FRBRWork Element...")
        FRBRWork = etree.Element("FRBRWork")

        FRBRthis = etree.SubElement(FRBRWork, "FRBRthis",
                                    attrib={"value" : "/akn/gr/"+
                                            self.textType + "/" + self.foreas + "/" +
                                            self.issueYear + "/" +
                                            self.decisionNumber + "/!main"}
                                    )

        FRBRuri = etree.SubElement(FRBRWork, "FRBRuri",
                                   attrib={"value" : "/akn/gr/"+
                                           self.textType + "/" + self.foreas + "/" +
                                           self.issueYear + "/" +
                                           self.decisionNumber + "/"}
                                   )
        
        if self.ECLI:
            FRBRalias = etree.SubElement(FRBRWork, "FRBRalias")
            FRBRalias.set("value", self.ECLI)
            FRBRalias.set("name", "ECLI")

        FRBRdate = etree.SubElement(FRBRWork, "FRBRdate",
                                    attrib = {"name":""})

        if self.publicationDate:
            FRBRdate.set("date", self.publicationDate)
            FRBRdate.set("name", "")

        FRBRauthor = etree.SubElement(FRBRWork, "FRBRauthor",
                                      attrib={"href" : self.author}
                                      )

        FRBRcountry = etree.SubElement(FRBRWork, "FRBRcountry",
                                       attrib={"value" : "gr"}
                                       )

        #print(etree.tostring(FRBRWork, pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
        return FRBRWork


    def createFRBRExpression(self):
        """This method creates the <<FRBRExpression>> element of AkomaNtoso's
        identification node

        Args:
            self: The object itself

        Returns:
            lxml <<FRBRExpression>> element 
        """
        #print("Creating FRBRExpression Element...")
        Akn_LOGGER.info("Creating FRBRExpression Element...")
        FRBRExpression = etree.Element("FRBRExpression")

        FRBRthis = etree.SubElement(FRBRExpression, "FRBRthis",
                                    attrib={"value" : "/akn/gr/" +
                                            self.textType + "/" + self.foreas + "/" +
                                            self.issueYear + "/" +
                                            self.decisionNumber +
                                            "/ell@/!main"}
                                    )
        
        FRBRuri = etree.SubElement(FRBRExpression, "FRBRuri",
                                   attrib={"value" : "/akn/gr/" +
                                           self.textType + "/" + self.foreas + "/" +
                                           self.issueYear + "/" +
                                           self.decisionNumber + "/ell@"}
                                   )
            
        FRBRdate = etree.SubElement(FRBRExpression, "FRBRdate", attrib = {"name":""})

        if self.publicationDate:
            FRBRdate.set("date", self.publicationDate)

        FRBRauthor = etree.SubElement(FRBRExpression, "FRBRauthor", attrib={"href" : self.author})

        FRBRlanguage = etree.SubElement(FRBRExpression, "FRBRlanguage",
                                        attrib={"language" : "ell"}
                                       )

        #print(etree.tostring(FRBRExpression,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
        return FRBRExpression


    def createFRBRManifestation(self):
        """This method creates the <<FRBRManifestation>> element of
        AkomaNtoso's identification node

        Args:
            self: The object itself

        Returns:
            lxml <<FRBRManifestation>> element 
        """
        #print("Creating FRBRManifestation Element...")
        Akn_LOGGER.info("Creating FRBRManifestation Element...")
        FRBRManifestation = etree.Element("FRBRManifestation")

        FRBRthis = etree.SubElement(FRBRManifestation, "FRBRthis",
                                    attrib={"value" : "/akn/gr/" +
                                            self.textType + "/" + self.foreas + "/" +
                                            self.issueYear + "/" +
                                            self.decisionNumber +
                                            "/ell@/!main.xml"}
                                    )
        
        FRBRuri = etree.SubElement(FRBRManifestation, "FRBRuri",
                                   attrib={"value" : "/akn/gr/" +
                                            self.textType + "/" + self.foreas + "/" +
                                            self.issueYear + "/" +
                                            self.decisionNumber +
                                           "/ell@.xml"}
                                   )

        FRBRdate = etree.SubElement(FRBRManifestation, "FRBRdate",
                                    attrib = {
                                        "name":"XMLConversion",
                                        "date": str(datetime.date.today())
                                        }
                                    )

        FRBRauthor = etree.SubElement(FRBRManifestation, "FRBRauthor",
                                        attrib={"href" : self.creator})

        #print(etree.tostring(FRBRManifestation,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))

        return FRBRManifestation


    def createLifecycle(self):
        """This method creates the <<lifecycle>> element of
        AkomaNtoso's meta node

        Args:
            self: The object its self

        Returns:
            lxml <<lifecycle>> element 
        """
        #print("Creating Lifecycle Element...")
        Akn_LOGGER.info("Creating Lifecycle Element...")
        lifecycle = etree.Element("lifecycle", attrib ={"source" : self.creator})
        eventRef = etree.SubElement(lifecycle, "eventRef",
                                    attrib={"source" : "#original",
                                            "type" : "generation",
                                            "date": str(datetime.date.today())
                                            }
                                    )
        
        #print(etree.tostring(lifecycle,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return lifecycle

    def createWorkflow(self):
        """This method creates the <<workflow>> element of
        AkomaNtoso's judgment node.

        Args:
            self: The object itself

        Returns:
            lxml <<workflow>> element 
        """
        #print("Creating workflow Element...")
        Akn_LOGGER.info("Creating workflow Element...")
        workflow = etree.Element("workflow", attrib={"source" : self.creator})
        
        #print(etree.tostring(workflow,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return workflow

    def createReferences(self):
        """This method creates the <<references>> element of
        AkomaNtoso's judgment node.

        Args:
            self: The object itself

        Returns:
            lxml <<references>> element 
        """
        #print("Creating references Element...")
        Akn_LOGGER.info("Creating references Element...")
        references = etree.Element("references", attrib={"source" : self.creator})
        original = etree.SubElement(references, "original", attrib={"eId":"original",
                                                                    "href":"/akn/gr/" + self.textType + "/" +
                                                                    self.foreas + "/" +
                                                                    self.issueYear + "/" +
                                                                    self.decisionNumber +
                                                                    "/ell@", "showAs":"Original"})
        
        #print(etree.tostring(references,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return references

    def checkReferencesElementExists(self, node = None):
        """This method checks if <<references>> element exists as subelement
        in node parameter

        Args:
            self: The object itself
            node: The node to check for references element
            
        Returns:
            true or false 
        """
        elemExists = False
        if node is not None:
            referenceElem = node.findall('references')
            if referenceElem:
                elemExists = True

        return elemExists

    def createProprietary(self):
        """This method creates the <<proprietary>> element of
        AkomaNtoso's judgment node.

        Args:
            self: The object itself

        Returns:
            lxml <<proprietary>> element 
        """
        #print("Creating proprietary Element...")
        Akn_LOGGER.info("Creating proprietary Element...")
        
        proprietary = etree.Element("proprietary", attrib={'source' : self.creator})
        adaElem = etree.SubElement(proprietary, '{' + self.nsmap['openlawsgr']+'}ada')
        adaElem.text = self.ada

        if self.chairman is not None:
            chairmanElem = etree.SubElement(proprietary, '{' + self.nsmap['openlawsgr']+'}chairman')
            chairmanElem.text = self.chairman

        if self.rapporteur is not None:
            rapporteurElem = etree.SubElement(proprietary, '{' + self.nsmap['openlawsgr']+'}rapporteur')
            rapporteurElem.text = self.rapporteur
        
        statusElem = etree.SubElement(proprietary, '{' + self.nsmap['openlawsgr']+'}status')
        statusElem.text = self.status

        summaryElem = etree.SubElement(proprietary, '{' + self.nsmap['openlawsgr']+'}summary')
        summaryElem.text = self.summary
        
        #print(etree.tostring(proprietary,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return proprietary


    def createPublication(self):
        """This method creates the <<publication>> element of
        AkomaNtoso's judgment node.

        Args:
            self: The object itself

        Returns:
            lxml <<publication>> element 
        """
        #print("Creating publication Element...")
        Akn_LOGGER.info("Creating publication Element...")
        publication = etree.Element("publication",
                                    attrib={
                                        'name' : 'Diavgeia',
                                        'showAs' : 'Diavgeia',
                                        'number' : self.ada
                                        }
            )

        if self.publicationDate:
            publication.set("date", self.publicationDate)
        
        #print(etree.tostring(publication,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return publication

    def createClassification(self):
        """This method creates the <<classification>> element of
        AkomaNtoso's judgment meta node.

        Args:
            self: The object itself

        Returns:
            lxml <<classification>> element 
        """
        #print("Creating classification Element...")
        Akn_LOGGER.info("Creating classification Element...")
        classification = etree.Element("classification",
                                       attrib={'source' : self.creator})
    
        if self.keywords:
            cnt = 0
            for keyword in self.keywords:
                cnt += 1
                keywordElem = etree.SubElement(classification, "keyword",
                                               attrib={'eId' : "keyword_" + str(cnt),
                                                       'value' : keyword,
                                                       'showAs' : keyword,
                                                       'dictionary' : "none"})
        
        #print(etree.tostring(classification,
        #                     pretty_print=True,
        #                     encoding="UTF-8",
        #                     xml_declaration =True).decode('utf8'))
    
        return classification
    
    def enterAkomaNtoso(self, ctx):
        """Enter a parse tree produced by aknParser#akomaNtoso"""
        #Akn_LOGGER.info("Entering AkomaNtoso node...")
        self.text += '<akomaNtoso>'
   
    def exitAkomaNtoso(self, ctx):
        """Exit a parse tree produced by aknParser#akomaNtoso"""
        #Akn_LOGGER.info("Exit AkomaNtoso node...")
        self.text += '</akomaNtoso>'
        return self.text
        
    def enterJudgment(self, ctx):
        """Enter a parse tree produced by aknParser#judgment"""
        if self.foreas == 'legalCouncilOfState':
            judgmentType = 'advisoryOpinion'
        else :
            judgmentType = 'decision'
        #Akn_LOGGER.info("Entering Judgment node...")
        self.text +='<judgment name=' + '"'+judgmentType + '"'+ '>'
    
    def exitJudgment(self, ctx):
        """Exit a parse tree produced by aknParser#judgment"""
        #Akn_LOGGER.info("Exit Judgment node...")
        self.text +='</judgment>'

    def enterHeader(self, ctx):
        """Enter a parse tree produced by aknParser#header"""
        #Akn_LOGGER.info("Entering Header node...")
        self.text +='<header>'
        
    def exitHeader(self, ctx):
        """Exit a parse tree produced by aknParser#header"""
        #Akn_LOGGER.info("Exit Header node...")
        self.text += '</header>'

    def enterCaseNmuber(self, ctx):
        """Enter a parse tree produced by aknParser#caseNmuber"""
        #Akn_LOGGER.info("Entering CaseNmuber node...")
        #Akn_LOGGER.debug("CaseNmuber text: %s", ctx.getText().rstrip())
        self.text += '<p>'
        for child in ctx.getChildren():
            if isinstance(child, tree.Tree.TerminalNodeImpl):
                self.text += child.getText().rstrip().encode('utf-8')
            else:
                pass
        
    def exitCaseNmuber(self, ctx):
        """Exit a parse tree produced by aknParser#caseNmuber"""
        #Akn_LOGGER.info("Exit CaseNmuber node...")
        self.text += '</p>'

    def enterDocProponent(self, ctx):
        """Enter a parse tree produced by aknParser#docProponent"""
        #Akn_LOGGER.info("Entering DocProponent node...")
        #Akn_LOGGER.debug("DocProponent text: %s", ctx.getText().strip())
        self.text += '<p><docProponent>' + ctx.getText().strip().encode('utf-8')
    
    def exitDocProponent(self, ctx):
        """Exit a parse tree produced by aknParser#docProponent"""
        #Akn_LOGGER.info("Exit DocProponent node...")
        self.text += '</docProponent></p>'

    def enterDocType(self, ctx):
        """Enter a parse tree produced by aknParser#docType"""
        #Akn_LOGGER.info("Entering DocType node...")
        #Akn_LOGGER.debug("DocType text: %s", ctx.getText().strip())
        self.text += '<docType>' + ctx.getText().strip().encode('utf-8')
    
    def exitDocType(self, ctx):
        """Exit a parse tree produced by aknParser#docType"""
        #Akn_LOGGER.info("Exit DocType node...")
        self.text += '</docType>'
        
    def enterHeaderPar(self, ctx):
        """Enter a parse tree produced by aknParser#headerPar"""
        #Akn_LOGGER.info("Entering HeaderPar node...")
        #Akn_LOGGER.debug("HeaderPar text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')
        
    def exitHeaderPar(self, ctx):
        """Exit a parse tree produced by aknParser#headerPar"""
        #Akn_LOGGER.info("Exit HeaderPar node...")
        self.text += '</p>' 

    def enterHeaderLastPar(self, ctx):
        """Enter a parse tree produced by aknParser#headerLastPar"""
        #Akn_LOGGER.info("Entering headerLastPar node...")
        #Akn_LOGGER.debug("headerLastPar text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')
        
    def exitHeaderLastPar(self, ctx):
        """Exit a parse tree produced by aknParser#headerLastPar"""
        #Akn_LOGGER.info("Exit headerLastPar node...")
        self.text += '</p>' 

    def enterHeaderLastPar_alt(self, ctx):
        """Enter a parse tree produced by aknParser#headerLastPar_alt"""
        #Akn_LOGGER.info("Entering HeaderLastPar_alt node...")
        #Akn_LOGGER.debug("HeaderLastPar_alt text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')
        
    def exitHeaderLastPar_alt(self, ctx):
        """Exit a parse tree produced by aknParser#headerLastPar_alt"""
        #Akn_LOGGER.info("Exit HeaderLastPar_alt node...")
        self.text += '</p>'
        
    def enterDocNumber(self, ctx):
        """Enter a parse tree produced by aknParser#docNumber"""
        #Akn_LOGGER.info("Entering DocNumber node...")
        #Akn_LOGGER.debug("DocNumber text: %s", ctx.getText().rstrip())
        self.text += '<docNumber>' + ctx.getText().rstrip().encode('utf-8')
        
    def exitDocNumber(self, ctx):
        """Exit a parse tree produced by aknParser#docNumber"""
        #Akn_LOGGER.info("Exit DocNumber node...")
        self.text += '</docNumber>'

    def enterJudgmentBody(self, ctx):
        """Enter a parse tree produced by aknParser#judgmentBody"""
        #Akn_LOGGER.info("Entering judgmentBody node...")
        self.text += '<judgmentBody>'

    def exitJudgmentBody(self, ctx):
        """Exit a parse tree produced by aknParser#judgmentBody"""
        #Akn_LOGGER.info("Exit judgmentBody node...")
        self.text += '</judgmentBody>'

    def enterIntroduction(self, ctx):
        """Enter a parse tree produced by aknParser#introduction"""
        #Akn_LOGGER.info("Entering Introduction node...")
        self.text += '<introduction>'

    def exitIntroduction(self, ctx):
        """Exit a parse tree produced by aknParser#introduction"""
        #Akn_LOGGER.info("Exit Introduction node...")
        self.text += '</introduction>'

    def enterIntroductionIntro(self, ctx):
        """Enter a parse tree produced by aknParser#introductionIntro"""
        #Akn_LOGGER.info("Entering IntroductionIntro node...")
        #Akn_LOGGER.debug("IntroductionIntro text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitIntroductionIntro(self, ctx):
        """Exit a parse tree produced by aknParser#introductionIntro"""
        #Akn_LOGGER.info("Exit IntroductionIntro node...")
        self.text += '</p>'

    def enterIntro_Par(self, ctx):
        """Enter a parse tree produced by aknParser#introPar"""
        #Akn_LOGGER.info("Entering Intro_Par node...")
        #Akn_LOGGER.debug("Intro_Par text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitIntro_Par(self, ctx):
        """Exit a parse tree produced by aknParser#introPar"""
        #Akn_LOGGER.info("Exit Intro_Par node...")
        self.text += '</p>'
        
    def enterMotivation(self, ctx):
        """Enter a parse tree produced by aknParser#motivation"""
        # This is for judgments
        self.motivationCounter += 1
        # This is only for Legal Opinions
        self.divisionCounter = 0
        #Akn_LOGGER.info("Entering motivation node...")
        self.text += '<motivation>'

    def exitMotivation(self, ctx):
        """Exit a parse tree produced by aknParser#motivation"""
        #Akn_LOGGER.info("Exit motivation node...")
        self.text += '</motivation>'

    def enterMotivPar(self, ctx):
        """Enter a parse tree produced by aknParser#motivPar"""
        #Akn_LOGGER.info("Entering MotivPar node...")
        #Akn_LOGGER.debug("MotivPar text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitMotivPar(self, ctx):
        """Exit a parse tree produced by aknParser#motivPar"""
        #Akn_LOGGER.info("Exit MotivPar node...")
        self.text += '</p>'

    def enterBlockList(self, ctx):
        """Enter a parse tree produced by aknParser#blockList"""
        #Akn_LOGGER.info("Entering BlockList node...")
        eId = "motivation_list_" + str(self.motivationCounter) 
        self.text += '<blockList eId = ' + '"' + eId + '"' + '>'

    def exitBlockList(self, ctx):
        """Exit a parse tree produced by aknParser#blockList"""
        #Akn_LOGGER.info("Exit BlockList node...")
        self.text += '</blockList>'

    def enterSte_item(self, ctx):
        """Enter a parse tree produced by aknParser#ste_item"""
        #Akn_LOGGER.info("Entering Ste_item node...")
        #Akn_LOGGER.debug("Ste_item text: %s", ctx.getText().rstrip())
        self.itemCounter +=1
        eId = "motivation_list_" + str(self.motivationCounter) + "__item_" + str(self.itemCounter)
        self.text += '<item eId = ' + '"' + eId + '"' + '>'

    def exitSte_item(self, ctx):
        """Exit a parse tree produced by aknParser#ste_item"""
        #Akn_LOGGER.info("Exit Ste_item node...")
        self.text += '</item>'

    def enterNum(self, ctx):
        """Enter a parse tree produced by aknParser#num"""
        #Akn_LOGGER.info("Entering Num node...")
        self.text += '<num>' + ctx.getText().rstrip().encode('utf-8')

    def exitNum(self, ctx):
        """Exit a parse tree produced by aknParser#num"""
        #Akn_LOGGER.info("Exit Num node...")
        self.text += '</num>'

    def enterItemPar(self, ctx):
        """Enter a parse tree produced by aknParser#itemPar"""
        #Akn_LOGGER.info("Entering ItemPar node...")
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitItemPar(self, ctx):
        """Exit a parse tree produced by aknParser#itemPar"""
        #Akn_LOGGER.info("Exit ItemPar node...")
        self.text += '</p>'

    def enterArPagos_item(self, ctx):
        """Enter a parse tree produced by aknParser#arPagos_item"""
        #Akn_LOGGER.info("Entering ArPagos_item node...")
        #Akn_LOGGER.debug("ArPagos_item text: %s", ctx.getText().rstrip())
        self.itemCounter +=1
        eId = "motivation_list_" + str(self.motivationCounter) + "__item_" + str(self.itemCounter)
        self.text += '<item eId = ' + '"' + eId + '"' + '>'

    def exitArPagos_item(self, ctx):
        """Exit a parse tree produced by aknParser#arPagos_item"""
        #Akn_LOGGER.info("Exit ArPagos_item node...")
        self.text += '</item>'
    
    def enterDecision(self, ctx):
        """Enter a parse tree produced by aknParser#decision"""
        #Akn_LOGGER.info("Entering Decision node...")
        # This is only for Legal Opinions
        self.divisionCounter = 0
        self.text += '<decision>'
    
    def exitDecision(self, ctx):
        """Exit a parse tree produced by aknParser#decision"""
        #Akn_LOGGER.info("Exit Decision node...")
        self.text += '</decision>'

    def enterDecisionIntro(self, ctx):
        """Enter a parse tree produced by aknParser#decisionIntro"""
        #Akn_LOGGER.info("Entering DecisionIntro node...")
        #Akn_LOGGER.debug("DecisionIntro text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitDecisionIntro(self, ctx):
        """Exit a parse tree produced by aknParser#decisionIntro"""
        #Akn_LOGGER.info("Exit DecisionIntro node...")
        self.text += '</p>'

    def enterDecisionPar(self, ctx):
        """Enter a parse tree produced by aknParser#decisionPar"""
        #Akn_LOGGER.info("Entering DecisionPar node...")
        if ctx.getText().rstrip() != '':
            self.text += '<p>'

    def exitDecisionPar(self, ctx):
        """Exit a parse tree produced by aknParser#decisionPar"""
        #Akn_LOGGER.debug("DecisionPar text: %s", ctx.getText().rstrip())
        #Akn_LOGGER.info("Exit DecisionPar node...")
        if ctx.getText().rstrip() != '':
            for child in ctx.getChildren():
                #print type(child)
                if isinstance(child, tree.Tree.TerminalNodeImpl):
                    self.text += child.getText().encode('utf-8')
                else:
                    pass
            self.text = self.text.rstrip()
            self.text += '</p>'

    def enterOutcomePar(self, ctx):
        """Enter a parse tree produced by aknParser#OutcomePar"""    
        #Akn_LOGGER.info("Entering OutcomePar node...")
        self.text += '<p>'
    
    def exitOutcomePar(self, ctx):
        """Enter a parse tree produced by aknParser#OutcomePar"""
        # outcomePar may contain an outcome node so text has already be written
        # in self.text, we just need to write any text that is instance of terminalNodeImpl
        text = ''
        for child in ctx.getChildren():
            if isinstance(child, tree.Tree.TerminalNodeImpl):
                text += child.getText().encode('utf-8')
        #remove line break from the end of the text
        text = text.rstrip()
        self.text += text
        #Akn_LOGGER.debug("OutcomePar text: %s", text)
        #Akn_LOGGER.info("Exit OutcomePar node...")
        self.text += '</p>'
    
    def enterOutcome(self, ctx):
        """Enter a parse tree produced by aknParser#outcome"""
        #Akn_LOGGER.info("Entering Outcome node...")
        #Akn_LOGGER.debug("Outcome text: %s", ctx.getText().rstrip())
        self.text += '<outcome>' + ctx.getText().rstrip().encode('utf-8')

    def exitOutcome(self, ctx):
        """Exit a parse tree produced by aknParser#outcome"""
        #Akn_LOGGER.info("Exit Outcome node...")
        self.text += '</outcome>'

    def enterConclusions(self, ctx):
        """Enter a parse tree produced by aknParser#conclusion"""
        #Akn_LOGGER.info("Entering Conclusions node...")
        self.text += '<conclusions>'

    def exitConclusions(self, ctx):
        """Exit a parse tree produced by aknParser#conclusion"""
        #Akn_LOGGER.info("Exit Conclusions node...")
        self.text += '</conclusions>'

    def enterConclusionIntro(self, ctx):
        """Enter a parse tree produced by aknParser#conclusionIntro"""
        #Akn_LOGGER.info("Entering ConclusionIntro node...")
        #Akn_LOGGER.debug("ConclusionIntro text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitConclusionIntro(self, ctx):
        """Exit a parse tree produced by aknParser#conclusionIntro"""
        #Akn_LOGGER.info("Exit conclusionIntro node...")
        self.text += '</p>'

    def enterConcPar(self, ctx):
        """Enter a parse tree produced by aknParser#concPar"""
        #Akn_LOGGER.info("Entering concPar node...")
        #Akn_LOGGER.debug("concPar text: %s", ctx.getText().rstrip())
        if ctx.getText().rstrip() != '':
            self.text += '<p>' + ctx.getText().rstrip().encode('utf-8')

    def exitConcPar(self, ctx):
        """Exit a parse tree produced by aknParser#concPar"""
        #Akn_LOGGER.info("Exit concPar node...")
        if ctx.getText().rstrip() != '':
            self.text += '</p>'

    """--------------------------------- LEGAL OPINIONS ----------------------------------------- """
    def enterPersonalLegalOpinion(self, ctx):
        """Enter a parse tree produced by aknParser#personalLegalOpinion"""
        #Akn_LOGGER.info("Entering personalLegalOpinion node...")
        #Akn_LOGGER.info("personalLegalOpinion text: %s", ctx.getText().strip())
        self.text +='<p>' + ctx.getText().strip().encode('utf-8')

    def exitPersonalLegalOpinion(self, ctx):
        """Exit a parse tree produced by aknParser#personalLegalOpinion"""
        #Akn_LOGGER.info("Exit personalLegalOpinion node...")
        self.text +='</p>'
    
    def enterQuestionInfo(self, ctx):
        """Enter a parse tree produced by aknParser#questionInfo"""
        #Akn_LOGGER.info("Entering questionInfo node...")
        #Akn_LOGGER.debug("questionInfo text: %s", ctx.getText().strip())
        self.text += '<p>' + ctx.getText().strip().encode('utf-8')
    
    def exitQuestionInfo(self, ctx):
        """Exit a parse tree produced by aknParser#questionInfo"""
        #Akn_LOGGER.info("Exit questionInfo node...")
        self.text += '</p>'

    def enterBackground(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#background"""
        #Akn_LOGGER.info("Entering background node...")
        self.divisionCounter = 0
        self.text += '<background>'

    def exitBackground(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#background"""
        #Akn_LOGGER.info("Exit background node...")
        self.text += '</background>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterBackground_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#background_alt"""
        #Akn_LOGGER.info("Entering background_alt node...")
        self.divisionCounter = 0
        self.text += '<background>'

    def exitBackground_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#background_alt"""
        #Akn_LOGGER.info("Exit background_alt node...")
        self.text += '</background>'
    # -------------------------------------------------------------------------------------------------------------#

    def enterBackgroundDivision(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivision"""
        #Akn_LOGGER.info("Entering backgroundDivision node...")
        global division_eId
        self.divisionParagraph = 0
        self.divisionCounter += 1
        eId = "background__division_" + str(self.divisionCounter)
        division_eId = eId
        self.text += "<division eId = " + '"' + eId + '"' + ">"

    def exitBackgroundDivision(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivision"""
        #Akn_LOGGER.info("Exit backgroundDivision node...")
        self.text += '</division>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterBackgroundDivision_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivision_alt"""
        #Akn_LOGGER.info("Entering backgroundDivision_alt node...")
        global division_eId
        self.divisionParagraph = 0
        self.divisionCounter += 1
        eId = "background__division_" + str(self.divisionCounter)
        division_eId = eId
        self.text += "<division eId = " + '"' + eId + '"' + ">"

    def exitBackgroundDivision_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivision_alt"""
        #Akn_LOGGER.info("Exit backgroundDivision_alt node...")
        self.text += '</division>'
    # -------------------------------------------------------------------------------------------------------------#

    def enterBackgroundDivisionHeading(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivisionHeading"""
        #Akn_LOGGER.info("Entering backgroundDivisionHeading node...")
        #Akn_LOGGER.debug("backgroundDivisionHeading text: %s", ctx.getText().rstrip())
        self.text += '<heading>' + ctx.getText().strip().encode('utf-8')

    def exitBackgroundDivisionHeading(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivisionHeading"""
        #Akn_LOGGER.info("Exit backgroundDivisionHeading node...")
        self.text += '</heading>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterBackgroundDivisionHeading_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivisionHeading_alt"""
        #Akn_LOGGER.info("Entering backgroundDivisionHeading_alt node...")
        #Akn_LOGGER.debug("backgroundDivisionHeading_alt text: %s", ctx.getText().rstrip())
        self.text += '<heading>' + ctx.getText().strip().encode('utf-8')

    def exitBackgroundDivisionHeading_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivisionHeading_alt"""
        #Akn_LOGGER.info("Exit backgroundDivisionHeading_alt node...")
        self.text += '</heading>'
    # -------------------------------------------------------------------------------------------------------------#
    
    def enterBackgroundDivisionParagraph(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivisionParagraph"""
        #Akn_LOGGER.info("Entering backgroundDivisionParagraph node...")
        global division_para_eId
        self.divisionParagraph += 1
        eId = division_eId + "__para_" + str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitBackgroundDivisionParagraph(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivisionParagraph"""
        #Akn_LOGGER.info("Exit backgroundDivisionParagraph node...")
        self.text += '</paragraph>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterBackgroundDivisionParagraph_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivisionParagraph_alt"""
        #Akn_LOGGER.info("Entering backgroundDivisionParagraph_alt node...")
        global division_para_eId
        self.divisionParagraph += 1
        eId = division_eId + "__para_" + str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitBackgroundDivisionParagraph_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivisionParagraph_alt"""
        #Akn_LOGGER.info("Exit backgroundDivisionParagraph_alt node...")
        self.text += '</paragraph>'
    # -------------------------------------------------------------------------------------------------------------#
    
    def enterBackgroundDivisionParagraphNum(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#backgroundDivisionParagraphNum"""
        #Akn_LOGGER.info("Entering backgroundDivisionParagraphNum node...")
        #Akn_LOGGER.debug("backgroundDivisionParagraphNum text: %s", ctx.getText().rstrip())
        self.text += '<num>' + ctx.getText().strip().encode('utf-8')

    def exitBackgroundDivisionParagraphNum(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#backgroundDivisionParagraphNum"""
        #Akn_LOGGER.info("Exit backgroundDivisionParagraphNum node...")
        self.text += '</num>'

    def enterContent(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#content"""
        #Akn_LOGGER.info("Entering content node...")
        eId = division_para_eId + "__content"
        self.text += "<content eId = " + '"' + eId + '"' + ">"

    def exitContent(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#content"""
        #Akn_LOGGER.info("Exit content node...")
        self.text += '</content>'
    
    def enterAlinea(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#alinea"""
        #Akn_LOGGER.info("Entering alinea node...")
        global division_para_eId
        self.divisionParagraph += 1
        eId = division_eId + "__" + "para_" +str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitAlinea(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#alinea."""
        #Akn_LOGGER.info("Exit alinea node...")
        self.text += '</paragraph>'
        
    def enterContentPar(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#contentPar"""
        #Akn_LOGGER.info("Entering contentPar node...")
        #Akn_LOGGER.debug("contentPar text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().strip().encode('utf-8')

    def exitContentPar(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#contentPar"""
        #Akn_LOGGER.info("Exit contentPar node...")
        self.text += '</p>'

    def enterMotivationDivision(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivationDivision"""
        #Akn_LOGGER.info("Entering motivationDivision node...")
        global division_eId
        self.divisionCounter += 1
        self.divisionParagraph = 0
        eId = "motivation__division_" + str(self.divisionCounter)
        division_eId = eId
        self.text += "<division eId = " + '"' + eId + '"' + ">"

    def exitMotivationDivision(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivationDivision"""
        #Akn_LOGGER.info("Exit motivationDivision node...")
        self.text += '</division>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterMotivationDivision_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivationDivision_alt"""
        #Akn_LOGGER.info("Entering motivationDivision_alt node...")
        global division_eId
        self.divisionCounter += 1
        self.divisionParagraph = 0
        eId = "motivation__division_" + str(self.divisionCounter)
        division_eId = eId
        self.text += "<division eId = " + '"' + eId + '"' + ">"

    def exitMotivationDivision_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivationDivision_alt"""
        #Akn_LOGGER.info("Exit motivationDivision_alt node...")
        self.text += '</division>'
    # -------------------------------------------------------------------------------------------------------------#
    
    def enterMotivationHeading(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivationHeading"""
        #Akn_LOGGER.info("Entering motivationHeading node...")
        #Akn_LOGGER.debug("motivationHeading text: %s", ctx.getText().rstrip())
        self.text += '<heading>' + ctx.getText().strip().encode('utf-8')

    def exitMotivationHeading(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivationHeading"""
        #Akn_LOGGER.info("Exit motivationHeading node...")
        self.text += '</heading>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterMotivationHeading_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivationHeading_alt"""
        #Akn_LOGGER.info("Entering motivationHeading_alt node...")
        #Akn_LOGGER.debug("motivationHeading_alt text: %s", ctx.getText().rstrip())
        self.text += '<heading>' + ctx.getText().strip().encode('utf-8')

    def exitMotivationHeading_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivationHeading_alt"""
        #Akn_LOGGER.info("Exit motivationHeading_alt node...")
        self.text += '</heading>'
    # -------------------------------------------------------------------------------------------------------------#

    def enterMotivationDivisionParagraph(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivationDivisionParagraph"""
        #Akn_LOGGER.info("Entering motivationDivisionParagraph node...")
        global division_para_eId
        self.divisionParagraph += 1
        eId = division_eId + "__para_" + str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitMotivationDivisionParagraph(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivationDivisionParagraph"""
        #Akn_LOGGER.info("Exit motivationDivisionParagraph node...")
        self.text += '</paragraph>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterMotivationDivisionParagraph_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivationDivisionParagraph_alt"""
        #Akn_LOGGER.info("Entering motivationDivisionParagraph_alt node...")
        global division_para_eId
        self.divisionParagraph += 1
        eId = division_eId + "__para_" + str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitMotivationDivisionParagraph_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivationDivisionParagraph_alt"""
        #Akn_LOGGER.info("Exit motivationDivisionParagraph_alt node...")
        self.text += '</paragraph>'
    # -------------------------------------------------------------------------------------------------------------#

    def enterMotivParNum(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivParNum"""
        #Akn_LOGGER.info("Entering motivParNum node...")
        #Akn_LOGGER.debug("motivParNum text: %s", ctx.getText().rstrip())
        self.text += '<num>' + ctx.getText().strip().encode('utf-8')

    def exitMotivParNum(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivParNum"""
        #Akn_LOGGER.info("Exit motivParNum node...")
        self.text += '</num>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterMotivParNum_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#motivParNum_alt"""
        #Akn_LOGGER.info("Entering motivParNum_alt node...")
        #Akn_LOGGER.debug("motivParNum_alt text: %s", ctx.getText().rstrip())
        self.text += '<num>' + ctx.getText().strip().encode('utf-8')

    def exitMotivParNum_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#motivParNum_alt"""
        #Akn_LOGGER.info("Exit motivParNum_alt node...")
        self.text += '</num>'
    # -------------------------------------------------------------------------------------------------------------#
    
    def enterDecisionDivision(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#decisionDivision"""
        #Akn_LOGGER.info("Entering decisionDivision node...")
        global division_eId
        self.divisionCounter += 1
        self.divisionParagraph = 0
        eId = "decision__division_" + str(self.divisionCounter)
        division_eId = eId
        self.text += "<division eId = " + '"' + eId + '"' + ">"

    def exitDecisionDivision(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#decisionDivision"""
        #Akn_LOGGER.info("Exit decisionDivision node...")
        self.text += '</division>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterDecisionDivision_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#decisionDivision_alt"""
        #Akn_LOGGER.info("Entering decisionDivision_alt node...")
        global division_eId
        self.divisionCounter += 1
        self.divisionParagraph = 0
        eId = "decision__division_" + str(self.divisionCounter)
        division_eId = eId
        self.text += "<division eId = " + '"' + eId + '"' + ">"

    def exitDecisionDivision_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#decisionDivision_alt"""
        #Akn_LOGGER.info("Exit decisionDivision_alt node...")
        self.text += '</division>'
    # -------------------------------------------------------------------------------------------------------------#
    
    def enterDecisionHeading(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#decisionHeading"""
        #Akn_LOGGER.info("Entering decisionHeading node...")
        self.text += '<heading>' + ctx.getText().strip().encode('utf-8')

    def exitDecisionHeading(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#decisionHeading"""
        #Akn_LOGGER.info("Exit decisionHeading node...")
        self.text += '</heading>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterDecisionHeading_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#decisionHeading_alt"""
        #Akn_LOGGER.info("Entering decisionHeading_alt node...")
        #Akn_LOGGER.debug("decisionHeading_alt text: %s", ctx.getText().rstrip())
        self.text += '<heading>' + ctx.getText().strip().encode('utf-8')

    def exitDecisionHeading_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#decisionHeading"""
        #Akn_LOGGER.info("Exit decisionHeading_alt node...")
        self.text += '</heading>'
    # -------------------------------------------------------------------------------------------------------------#

    def enterDecisionDivisionParagraph(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#decisionDivisionParagraph"""
        #Akn_LOGGER.info("Entering decisionDivisionParagraph node...")
        global division_para_eId
        self.divisionParagraph += 1
        eId = division_eId + "__para_" + str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitDecisionDivisionParagraph(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#decisionDivisionParagraph"""
        #Akn_LOGGER.info("Exit decisionDivisionParagraph node...")
        self.text += '</paragraph>'

    # This is when sections are split not by Latin numbering but uppercase letters (A. B. etc)
    def enterDecisionDivisionParagraph_alt(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#decisionDivisionParagraph_alt"""
        #Akn_LOGGER.info("Entering decisionDivisionParagraph_alt node...")
        global elementID
        self.divisionParagraph += 1
        eId = division_eId + "__para_" + str(self.divisionParagraph)
        division_para_eId = eId
        self.text += "<paragraph eId = " + '"' + eId + '"' + ">"

    def exitDecisionDivisionParagraph_alt(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#decisionDivisionParagraph_alt"""
        #Akn_LOGGER.info("Exit decisionDivisionParagraph_alt node...")
        self.text += '</paragraph>'
    # -------------------------------------------------------------------------------------------------------------#

    def enterDecisionContent(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#DecisionContent"""
        #Akn_LOGGER.info("Entering DecisionContent node...")
        eId = division_para_eId + "__content"
        self.text += "<content eId = " + '"' + eId + '"' + ">"

    def exitDecisionContent(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#DecisionContent"""
        #Akn_LOGGER.info("Exit DecisionContent node...")
        self.text += '</content>'

    def enterDecisionContentPar(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#DecisionContentPar"""
        #Akn_LOGGER.info("Entering DecisionContentPar node...")
        #Akn_LOGGER.debug("DecisionContentPar text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().encode('UTF-8')

    def exitDecisionContentPar(self, ctx):
        """Exit a parse tree produced by LegalOpinionParser#DecisionContentPar"""
        #Akn_LOGGER.info("Exit DecisionContentPar node...")
        self.text += '</p>'

    def enterConclusionStart(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#conclusionStart"""
        #Akn_LOGGER.info("Entering conclusionStart node...")
        #Akn_LOGGER.debug("conclusionStart text: %s", ctx.getText().rstrip())
        self.text += '<p>' + ctx.getText().strip().encode('UTF-8')

    # Exit a parse tree produced by LegalOpinionParser#onclusionStart.
    def exitConclusionStart(self, ctx):
        """Enter a parse tree produced by LegalOpinionParser#conclusionStart"""
        #Akn_LOGGER.info("Exit conclusionStart node...")
        self.text += '</p>'

    # We don' t need these parser will visit HeaderPar node!
    # Enter a parse tree produced by LegalOpinionParser#conclusionPar.
    #def enterConclusionPar(self, ctx):
    #    self.text += '<p>'

    # Exit a parse tree produced by LegalOpinionParser#conclusionPar.
    #def exitConclusionPar(self, ctx):
     #   self.text += '</p>'
    
    ###################### OTHER METHODS ##########################
    def modifyReferencesFromGateXml(self, gateXmlFileObj, node):
        """This method populates the references node of an Akoma Ntoso document
        with the appropriate nodes based on Named Entity Recognition

        Args:
            self: The object itself

            gateXmlFileObj: A gate XML file containing Named Entities

            node: The XML node tha will be modified (references node)

        Returns:
            node: A new modified node element (references node) 
        """

        ontology_href = '/akn/ontology/'
        grString = 'gr/'
        hrefTag = ''

        elementTree = etree.parse(gateXmlFileObj)
        gateXmlRoot = elementTree.getroot()
        annotationNodes = gateXmlRoot.findall("AnnotationSet/Annotation")
        for annotation in annotationNodes:
            # we need to read only those annotation which contain an entity
            if annotation.get('Type') == 'ENTITY':
                #print 'StartNode: ' + annotation.get("StartNode") + ' - EndNode: ' +  annotation.get("EndNode")
                #print '1st Level Node: ' + annotation[0].tag
                #print annotation[0].find('Value').text
                #print '2nd Level Node: ' + annotation[1].tag
                #print annotation[1].find('Value').text

                EntityString = annotation[0].find('Value').text
                # Problem with some characters from gate XML (need to replace &#xd; with '' -> (none) in GATE XML
                EntityString = re.sub(r"\n", " ", EntityString.encode('utf-8'))
                EntityType = annotation[1].find('Value').text

                # Check if Entity has already been inserted as a node
                lemmas = ''
                latinLemmas = ''
                # Get Annotations which contain entity tokens
                TokenAnnotationsNodes = gateXmlRoot.findall('.//Annotation[@Type="Token"]')
                for tokenAnnotation in TokenAnnotationsNodes:
                    # For entities with multiple tokens
                    if int(tokenAnnotation.get("StartNode")) in range(int(annotation.get("StartNode")), int(annotation.get("EndNode"))):
                        # Find node which contains "Lemma" text
                        selectedFeatureNodeList = tokenAnnotation.xpath('.//Feature/Name[contains(text(),"Lemma")]')
                        if selectedFeatureNodeList is not None:
                            # Get parent node (Feature node)
                            selectedFeatureNode = selectedFeatureNodeList[0].getparent()
                            #print etree.tostring(selectedFeatureNode, pretty_print=True, encoding="UTF-8", xml_declaration =True)
                            # Get lemma
                            lemmas = selectedFeatureNode.find('Value').text
                            if lemmas:
                                for char in lemmas:
                                    for key, value in grToLat_v2.items():
                                        if char == key.decode('utf-8'):
                                            latinLemmas += value
                                latinLemmas = latinLemmas + "_"
                        
                lemmas = re.sub(r'_$', '', latinLemmas)
                # IF lemmas is not an empty string AND it has not been already inserted in references
                # Create an element and append it to references 
                if lemmas:
                    #elemEidExists = node.findall('.//*[@eId="'+latinValue+'"]')
                    elemEidExists = node.findall('.//*[@eId="'+lemmas+'"]')
                    if not elemEidExists:
                        if EntityType == 'FACILITY' or EntityType == 'ORGANIZATION' :
                            hrefTag = 'organization/'
                            entityTag = 'TLCOrganization'
                        elif EntityType == 'PERSON':
                            hrefTag = 'person/'
                            entityTag = 'TLCPerson'
                        elif EntityType == 'LOCATION':
                            hrefTag = 'location/'
                            entityTag = 'TLCLocation'

                        hrefAttr = ontology_href + hrefTag + grString
                        EntityElement = etree.SubElement(node, entityTag, attrib={'eId' : lemmas,
                                                                                  'href' : hrefAttr + lemmas,
                                                                                  'showAs' : EntityString.decode('utf-8')})

        #print etree.tostring(node, pretty_print=True, encoding="UTF-8", xml_declaration =True)
        return node

    def createNamedEntitiesInText(self, gateXmlFileObj, elementString):
        """This method finds Named Entities in a string representation of an element
        based on a gateXml file

        Args:
            self: The object itself

            gateXmlFileObj: A gate XML file containing Named Entities

            elementString: A string representation of a XML node (judgment node)

        Returns:
            string: A new modified XML string
        """
        LemmaSet = set()
        elementTree = etree.parse(gateXmlFileObj)
        gateXmlRoot = elementTree.getroot()
        annotationNodes = gateXmlRoot.findall("AnnotationSet/Annotation")
        for annotation in annotationNodes:
            Entitylemma = ''
            latinLemmas = ''
            tag = ''
            # we need to read only those annotation which contain an entity
            if annotation.get('Type') == 'ENTITY':
                #print '\n\n'
                #print 'StartNode ' + annotation.get("StartNode") + ' - EndNode' +  annotation.get("EndNode")
                #print '1st Level Node: ' + annotation[0].tag
                #print annotation[0].find('Value').text
                #print '2nd Level Node: ' + annotation[1].tag
                #print annotation[1].find('Value').text

                EntityString = annotation[0].find('Value').text
                # Problem with some characters from gate XML (need to replace &#xd; with '' -> (none) in GATE XML
                #EntityString = re.sub(r"&#xd;", "\r\n", EntityString)
                #print type(EntityString.encode('utf-8'))
                #print EntityString.encode('utf-8')
                #print type(EntityString.decode('UTF-8'))
                EntityType = annotation[1].find('Value').text

                # Find lemmas so as to create "refersTo" attribute
                TokensAnnotationNodes = gateXmlRoot.findall('.//Annotation[@Type="Token"]')
                for tokenAnnotation in TokensAnnotationNodes:
                    if int(tokenAnnotation.get("StartNode")) in range(int(annotation.get("StartNode")), int(annotation.get("EndNode"))):
                        # Find node which contains "Lemma" text
                        selectedFeatureNodeList = tokenAnnotation.xpath('.//Feature/Name[contains(text(),"Lemma")]')
                        if selectedFeatureNodeList is not None:
                            # Get parent node (Feature node)
                            selectedFeatureNode = selectedFeatureNodeList[0].getparent()
                            #print etree.tostring(selectedFeatureNode, pretty_print=True, encoding="UTF-8", xml_declaration =True)
                            # Get lemma
                            lemmas = selectedFeatureNode.find('Value').text
                            if lemmas:
                                for char in lemmas:
                                    for key, value in grToLat_v2.items():
                                        if char == key.decode('utf-8'):
                                            latinLemmas += value
                                latinLemmas = latinLemmas + "_"
                Entitylemma = re.sub(r'_$', '', latinLemmas)
                #print Entitylemma
                if Entitylemma and Entitylemma not in LemmaSet:
                    LemmaSet.add(Entitylemma)
                    refersToAttribute = '#' + Entitylemma   
                    if EntityType == 'FACILITY' or EntityType == 'ORGANIZATION' :
                        tag = '<organization refersTo = ' + '"' + refersToAttribute + '"' + '>' + EntityString + '</organization>'
                    elif EntityType == 'PERSON':
                        tag = '<person refersTo = ' + '"' + refersToAttribute + '"' + '>' + EntityString + '</person>'
                    elif EntityType == 'LOCATION':
                        tag = '<location refersTo = ' + '"' + refersToAttribute + '"' + '>' + EntityString + '</location>'
                    #pattern = re.compile(EntityString.encode('UTF-8'))
                    #elementString = re.sub(r"'"+EntityString.encode('UTF-8')+"'", r"'"+tag.encode('UTF-8')+"'", elementString)
                    elementString = elementString.replace(EntityString.encode('utf-8'),
                                                          tag.encode('utf-8'))
        return elementString
                        
    
    def XML(self):
        """
        This method returns a new element instance representing the XML
        written in as a string
        """
        return etree.fromstring(self.text.decode('utf8'))

    def replaceNewLine(self, text):
        """
        A method that removes the \n from the end of an element text so that
        an element is in pretty format.
        New lines control characters in Windows includes CR+LF, in Linux only LF 
        """
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        return text
