# -*- coding: utf-8 -*-
import logging
import re
import datetime
from lxml import etree
from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.RuleContext import RuleContext
from functions import *
from variables import *
from grammars.gen.Legal_refLexer import Legal_refLexer
from grammars.gen.Legal_refParser import Legal_refParser
from grammars.gen.Legal_refListener import Legal_refListener
from grammars.gen.Legal_refVisitor import Legal_refVisitor


Akn_LOGGER = logging.getLogger('Akn_LOGGER')

global href_base
global href_base_eu
#global judgment_href
href_base = "/akn/gr/"
href_base_eu = "/akn/eu/"
judgment = "judgment/"
legalOpinion = "advisoryOpinion/LegalCouncilOfState"

class AknLegalReferences(Legal_refListener, Legal_refVisitor):

    def __init__(self):
         self.text = ''
         self.LoggerCounter = 0
         Akn_LOGGER.info('Parsing legal references...')

    # Visit a parse tree produced by Legal_refParser#legal_text.
    #def visitAll_text(self, ctx):
    #   Akn_LOGGER.info("Start parsing legal references...\n")
    #   return self.visit(ctx.legal_text())

    # Visit a parse tree produced by Legal_refParser#legal_text.
    def visitLegal_reference(self, ctx):
        self.LoggerCounter += 1
        #if self.LoggerCounter > 1:
            #Akn_LOGGER.info("")
            #Akn_LOGGER.info("")
        Akn_LOGGER.info("LEGAL REFERENCE FOUND...")
        Akn_LOGGER.debug("legal reference text: %s", ctx.getText())
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by Legal_refParser#other.
    def visitOther_text(self, ctx):
        self.text += ctx.getText()
        return self.text

    # Visit a parse tree produced by Legal_refParser#courtDecision.
    def visitCourtDecision(self, ctx):
        Akn_LOGGER.debug('CourtDecision node START')
        return self.visitChildren(ctx)

    """ --------------- Two general types of court decsicion based on grammar ------------------  """
    # Visit a parse tree produced by Legal_refParser#singleCourtDec.
    def visitSingleCourtDec(self, ctx):
        Akn_LOGGER.debug("SingleCourtDec node START")
        global judgment_href
        judgment_href = href_base + judgment
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Legal_refParser#multipleCourtsDec.
    def visitMultipleCourtsDec(self, ctx):
        Akn_LOGGER.debug('MultipleCourtsDec node START')
        Akn_LOGGER.debug('MultipleCourts reference: %s', ctx.getText())
        for child in ctx.getChildren():
            if isinstance(child, Legal_refParser.IncompleteCourtDecAltContext) or isinstance(child, Legal_refParser.CompleteCourtDecAltContext):
                self.visit(child)
            else:
                self.text += child.getText()
        Akn_LOGGER.debug('MultipleCourtsDec node END')
        return self.text
    """ -----------------------------------------------------------------------------------------------------------"""

    # Visit a parse tree produced by Legal_refParser#completeCourtSingleDecision.
    def visitCompleteCourtSingleDecision(self, ctx):
        Akn_LOGGER.debug('completeCourtSingleDecision node START')
        Akn_LOGGER.debug('CompleteCourtSingleDecision text: %s', ctx.getText())
        court = self.visit(ctx.explicitCourt())
        global judgment_href
        #print court
        decision_id = self.visit(ctx.ids())
        #print decision_id
        judgment_href +=  court + "/" + decision_id + "/!main"
        #print judgment_href
        Akn_LOGGER.debug('href: %s', judgment_href)
        CompleteCourtSingleDecisionRef = '<ref href =' + '"' + judgment_href + '"' + '>' + ctx.getText() + '</ref>'
        #print CompleteCourtSingleDecisionRef
        self.text += CompleteCourtSingleDecisionRef
        Akn_LOGGER.debug('CompleteCourtSingleDecision reference: %s', CompleteCourtSingleDecisionRef)
        Akn_LOGGER.debug('completeCourtSingleDecision END')
        return self.text
    
    # Visit a parse tree produced by Legal_refParser#completeCourtMultipleDecisions.
    def visitCompleteCourtMultipleDecisions(self, ctx):
        Akn_LOGGER.debug('completeCourtMultipleDecisions node START')
        Akn_LOGGER.debug('completeCourtMultipleDecisions text: %s', ctx.getText())
        global judgment_href
        indx = 0 #index to visit all Multiple_idsContext of ctx

        #get court to create href
        court = self.visit(ctx.explicitCourt())
        judgment_href +=  court + "/"
        Akn_LOGGER.debug('href: %s', judgment_href)
        ComplCourtMultDecText = ''

        #traverse all chlidren of ctx
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, Legal_refParser.ExplicitCourtContext):
                #ExplicitCourt = self.visit(ctx.explicitCourt())
                #court = ExplicitCourt[0]
                #court_string = ExplicitCourt[1].encode('utf-8')
                #print court
                #print court_string
                #judgment_href = href_base + "judgment/" + court + '/'
                #self.text += court_string.decode('utf-8')
                ComplCourtMultDecText += child.getText()
                ##Akn_LOGGER.debug('judgment_href: %s', judgment_href) 

            # if it is instance of TerminalNodeImpl class
            # that means SPACE character is present, write it to self.text
            elif isinstance(child, tree.Tree.TerminalNodeImpl):
                ComplCourtMultDecText += child.getText()

            # if it is instance of Multiple_idsContext class
            # visit all nodes and construct href attribute for each case
            elif isinstance(child, Legal_refParser.Multiple_idsContext):
                refs = self.visit(ctx.multiple_ids(indx))
                ##Akn_LOGGER.debug('refs: %s', refs)
                indx += 1
                #print 'refs: ' + refs
                ComplCourtMultDecText += refs

            elif isinstance(child, Legal_refParser.DecisionContext):
                ComplCourtMultDecText += child.getText()

        self.text += ComplCourtMultDecText
        #print text
        Akn_LOGGER.debug('completeCourtMultipleDecisions reference: %s', ComplCourtMultDecText)
        Akn_LOGGER.info('completeCourtMultipleDecisions END')
        return self.text
    
    # Visit a parse tree produced by Legal_refParser#completeCourtDecAlt.
    def visitCompleteCourtDecAlt(self, ctx):
        Akn_LOGGER.debug('CompleteCourtDecAlt node START')
        Akn_LOGGER.debug('CompleteCourtDecAlt text: %s', ctx.getText())
        global judgment_href
        judgment_href = href_base + judgment
        court = self.visit(ctx.explicitCourt())
        #print judgment_href 
        #print court
        decision_id = self.visit(ctx.ids()[0])
        #print decision_id
        judgment_href +=  court + "/" + decision_id + "/!main"
        #print judgment_href
        Akn_LOGGER.debug('href: %s', judgment_href)
        CompleteCourtDecAltRef = '<ref href = ' + '"' + judgment_href + '"' + '>' + ctx.getText() + '</ref>'
        self.text += CompleteCourtDecAltRef
        Akn_LOGGER.debug('CompleteCourtDecAlt reference: %s', CompleteCourtDecAltRef)
        Akn_LOGGER.debug('CompleteCourtDecAlt END')
        return self.text

    # Visit a parse tree produced by Legal_refParser#incompleteCourtDec.
    def visitIncompleteCourtDec(self, ctx):
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by Legal_refParser#incompleteCourtDecAlt.
    def visitIncompleteCourtDecAlt(self, ctx):
        Akn_LOGGER.debug('IncompleteCourtDecAlt node START')
        Akn_LOGGER.debug('IncompleteCourtDecAlt text: %s', ctx.getText())
        global judgment_href
        judgment_href = href_base + judgment
        #print judgment_href 
        court = self.visit(ctx.implicitCourt()) 
        decision_id = self.visit(ctx.ids()[0])
        judgment_href +=  court + "/" + decision_id + "/!main"
        Akn_LOGGER.debug('href: %s', judgment_href)
        IncompleteCourtDecAlt = '<ref href = ' + '"' + judgment_href + '"' + '>' + ctx.getText() + '</ref>'
        self.text += IncompleteCourtDecAlt
        Akn_LOGGER.debug('IncompleteCourtDecAlt reference: %s', IncompleteCourtDecAlt)
        Akn_LOGGER.debug('IncompleteCourtDecAlt END')
        return self.text
    
    # Visit a parse tree produced by Legal_refParser#multiple_ids.
    def visitMultiple_ids(self, ctx):
        '''This is in case multiple decisions of a single court is present. There are several cases,
        e.g. a single reference -> 709/1981 and multiple ids -> 1317, 1318/1979'''
        Akn_LOGGER.debug('Entering multiple_ids node...')
        Akn_LOGGER.debug('Node text: %s', ctx.getText())

        # There cases when multiple ids of the same year are referred
        # We need to check how the ids are split in the text either by comma or by a hyphen
        if len(ctx.COMMA()) == 1:
            commaOrHyphen = ctx.COMMA()[0].getText()
            Akn_LOGGER.debug('separator %s', commaOrHyphen)
        elif len(ctx.HYPHEN()) :
            commaOrHyphen = ctx.HYPHEN()[0].getText()
            Akn_LOGGER.debug('separator %s', commaOrHyphen)
        else :
            commaOrHyphen = ','
            Akn_LOGGER.debug('no separator found, use: %s', commaOrHyphen)

        # get the year
        year = ctx.getText().encode('utf-8').split(ctx.SLASH().getText())[1]
        # check if multiple ids exist
        decision_id = ctx.getText().split('/')[0].split(str(commaOrHyphen))    
        size = len(decision_id)
        #print year
        #print decision_id

        if len(year) == 2:
            if int(year) in range(0, 19):
                year = '20'+year
            else:
                year = '19'+year
                
        text = ''
        Akn_LOGGER.debug('year: %s,  decision_id: %s,   size: %s', year, decision_id, size)
        #case single id is present in list
        if size == 1:
            Akn_LOGGER.debug('single id found')
            href = judgment_href + year + "/" + decision_id[0].strip() + "/!main"
            #print href
            text += '<ref href = ' + '"' + href + '"' + '>' + ctx.getText() + '</ref>'
        #case multiple ids are present
        else:
            Akn_LOGGER.debug('multiple ids found')
            for ref in decision_id: #for each id
                #if it is last reference in list
                if ref.strip() == decision_id[-1].strip():
                    href = judgment_href + year + "/" + ref.strip() + "/!main"
                    text += '<ref href = ' + '"' + href + '"' + '>' + ref.strip() + '/' + year + '</ref>'
                else :
                    href = judgment_href + year + "/" + ref.strip() + "/!main"
                    text += '<ref href = ' + '"' + href + '"' + '>' + ref.strip() + commaOrHyphen + '</ref>'
        return text

    # Visit a parse tree produced by Legal_refParser#explicitCourt.
    def visitExplicitCourt(self, ctx):
        Akn_LOGGER.debug('Entering ExplicitCourt node...')
        Akn_LOGGER.debug('court text: %s',  ctx.getText())
        court = self.visit(ctx.dikastirio())
        return court
        #return [self.visitChildren(ctx), ctx.getText()]

    # Visit a parse tree produced by Legal_refParser#implicitCourt.
    def visitImplicitCourt(self, ctx):
        return 'implicit_dikastirio_name'
    
    # Visit a parse tree produced by Legal_refParser#dikastirio.
    def visitDikastirio(self, ctx):
        # we just need to visit the only child of ctx and use courts dictionary to get the
        # corresponding court otherwise return "no_court_name"
        object_methods = [method_name for method_name in dir(ctx)
                          if callable(getattr(ctx, method_name))]

        #print dir(ctx)
        item_list = [e for e in dir(ctx) if e not in ('OLOMELEIA', 'SPACE')]
        courtStr = getTokenName(ctx, item_list, courts, 'no_court_name')
        #print courtStr
        Akn_LOGGER.debug('courts dictionary search result: %s',  courtStr)
        #print courts.get(type(ctx.getChild(0)).__name__, 'no_court_name')
        return courtStr

    # Visit a parse tree produced by Legal_refParser#ste.
    #def visitSte(self, ctx):
    #    Akn_LOGGER.debug('court variable: %s',  'COS')
    #    return 'COS'

    # Visit a parse tree produced by Legal_refParser#ste.
    def visitNsk(self, ctx):
        Akn_LOGGER.debug('court variable: %s',  'NSK')
        return 'NSK'
    
    # Visit a parse tree produced by Legal_refParser#ids.
    def visitIds(self, ctx):
        Akn_LOGGER.debug('Entering ids node...')
        if len(ctx.SLASH()) == 1:
            splitter = ctx.SLASH()[0].getText()
            Akn_LOGGER.debug('splitter %s', splitter)
        else :
            splitter = '/'
            Akn_LOGGER.debug('splitter %s', splitter)
            
        legal_id = ctx.getText().split(splitter)
        year = legal_id[1]
        #print 'year: ' + year
        arithmos = legal_id[0]
        #print 'arithmos: ' + arithmos
        
        if (len(legal_id)) == 3:
            arithmos = legal_id[0] + '/' + legal_id[1]
            #check M1107_2006 - STE
            if len(legal_id[2]) != 4 :
                date = re.split('\.|-', legal_id[2])
                #print date
                #date_str = datetime.date(int(date[2]), int(date[1]), int(date[0])).isoformat()
                #year = date_str
                year = date[2]
            #print year
        else:
            # here special cases of how they write ids
            # case where year is a double digit and the reference year first and number second
            if len(legal_id[1]) == 3 and (len(legal_id[0]) == 2 or len(legal_id[0]) == 4) :
                #print 'mpike'
                year = legal_id[0]
                arithmos = legal_id[1]
            # reference to ν. 4325/20015
            elif len(legal_id[1]) == 5:
                year = legal_id[1]
                arithmos = legal_id[0]
            # case where year is a date string
            elif len(legal_id[1]) != 4 and len(legal_id[1]) != 2 :
                date = re.split('\.|-', year)
                #print date
                #date_str = datetime.date(int(date[2]), int(date[1]), int(date[0])).isoformat()
                #year = date_str
                try:
                    year = date[2]
                except:
                    year = '0'
            elif len(legal_id[0]) == 2 and len(legal_id[1]) == 2 :
                year = legal_id[0]
                arithmos = legal_id[1]

        #print year
        # If year is a two digit string we need to convert it to 4digit string
        if len(year) == 2:
            if int(year) in range(0, 19):
                year = '20'+year
            else:
                year = '19'+year
        #print year
        decision_id = year  + '/' + arithmos
        Akn_LOGGER.debug('year: %s,  arithmos: %s,   decision_id: %s', year, arithmos, decision_id)
        return decision_id
    
    # Visit a parse tree produced by Legal_refParser#completeEULegislation.
    def visitCompleteEULegislation(self, ctx):
        Akn_LOGGER.debug('Entering CompleteEULegislation node...')
        global legislation_href
        global elemDict
        
        legislation_href = href_base_eu
        elemDict = {}
        #object_methods = [method_name for method_name in dir(ctx) if callable(getattr(ctx, method_name))]
        #print object_methods
        #print ctx.eu_directive
        #print ctx.eu_regulation()

        if ctx.eu_regulation():
            legislation_href +=  'act/regulation/'
        elif ctx.eu_directive():
            legislation_href +=  'act/directive/'

        #decision_id = self.visit(ctx.ids())
        decision_id = ctx.ids().getText()
        #print ctx.ids().getText()
        decision_id_split = re.compile(r"/|\|").split(decision_id)
        if len(decision_id_split[0]) == 2 :
            if int(decision_id_split[0]) in range(0, 19):
                elemDict['legalYear'] = '20' + decision_id_split[0]
            else:
                elemDict['legalYear'] = '19' + decision_id_split[0]
        else:
            elemDict['legalYear'] = decision_id_split[0]

        elemDict['legalNumber'] = decision_id_split[1]
        
        #print elemDict
        #if decision_id:
        #    elemDict['ExplicitLegalTypeContext'] = decision_id

        if len(ctx.explicitLegalElement()) > 0 :
            for n in range(0, len(ctx.explicitLegalElement())):
                #print type(ctx.explicitLegalElement()[n])
                childType = ctx.explicitLegalElement()[n].getChild(0)
                for child in childType.getChildren():
                    #print type(child)
                    if isinstance(child, Legal_refParser.SingleLegalElementIdContext):
                        elemID = child.getText()
                        #print elemID
                        #print type(elemID)
                        elemID = textToNumbering(elemID, numberingSystem)
                        #print elemID
                        elemDict[type(childType).__name__] = elemID
                        
        text = ''
        if splitMultHref == 1:
            Akn_LOGGER.debug('This EUreference contains multiple ids in some elements!')
            self.text += ctx.getText()
        else:
            Akn_LOGGER.debug('This EUreference contains single ids in all elements!')
            href = legislation_href + createHrefFromDictionary(elemDict, 0)
            Akn_LOGGER.debug('href: %s', href)
            text =  '<ref href = ' + '"' + href + '"' + '>' + ctx.getText() + '</ref>'
            Akn_LOGGER.debug('reference_text: %s', href)

        Akn_LOGGER.debug('CompleteEULegislation text: %s', text)
        Akn_LOGGER.debug('CompleteEULegislation node END')
        self.text += text
        #print text
        return self.text
    
    # Visit a parse tree produced by Legal_refParser#completeLegalOpinion.
    def visitCompleteLegalOpinion(self, ctx):
        Akn_LOGGER.debug('Entering CompleteLegalOpinion node...')
        Akn_LOGGER.debug('CompleteLegalOpinion text: %s', ctx.getText())
        global LegalOp_href
        LegalOp_href = href_base + legalOpinion
        text = ''
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, tree.Tree.TerminalNodeImpl) or isinstance(child, Legal_refParser.NskContext):
                text += child.getText()
            elif isinstance(child, Legal_refParser.IdsContext):
                Akn_LOGGER.debug('id text: %s', child.getText())
                decision_id = self.visit(child)
                Akn_LOGGER.debug('decision_id: %s', ctx.getText())
                href =  LegalOp_href + "/" + decision_id + "/!main"
                Akn_LOGGER.debug('decision_id: %s', ctx.getText())
                text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
        #print text
        Akn_LOGGER.debug('legal Opinion ref: %s', text)
        self.text += text
        return self.text
    
    # Visit a parse tree produced by Legal_refParser#singleLegislation.
    def visitSingleLegislation(self, ctx):
        Akn_LOGGER.debug('Entering SingleLegislation node...')
        Akn_LOGGER.debug('SingleLegislation text: %s', ctx.getText())
        # A global variable is used to catch cases where there exist multiple element ids
        # and we need to split text in multiple references
        global splitMultHref
        splitMultHref = 0
        #return self.visitChildren(ctx)
        self.text += self.visit(ctx.getChild(0))
        return self.text

    # Visit a parse tree produced by Legal_refParser#singleEULegislation.
    def visitSingleEULegislation(self, ctx):
        Akn_LOGGER.debug('Entering SingleEULegislation node...')
        Akn_LOGGER.debug('SingleEULegislation text: %s', ctx.getText())
        # A global variable is used to catch cases where there exist multiple element ids
        # and we need to split text in multiple references
        global splitMultHref
        splitMultHref = 0
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Legal_refParser#singleLegislation.
    def visitMultipleLegislation(self, ctx):
        Akn_LOGGER.debug('Entering MultipleLegislation node...')
        Akn_LOGGER.debug('MultipleLegislation text: %s', ctx.getText())
        # By default in this node only multiple references exist
        global elemDict
        global splitMultHref

        multLegislText = ''
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, tree.Tree.TerminalNodeImpl):
                #self.text += child.getText()
                multLegislText += child.getText()
            elif isinstance(child, Legal_refParser.MultipleCompleteLegislation_1Context):
                #self.visit(child)
                splitMultHref = 1
                multLegislText += self.visit(child)
            elif isinstance(child, Legal_refParser.ArthraContext):
                #self.visit(child)
                multLegislText += child.getText()
            elif isinstance(child, Legal_refParser.SingleLegislationContext):
                multLegislText += self.visit(child.getChild(0))
            else:
                global legislation_href
                splitMultHref = 1
                legislation_href = href_base
                elemDict = {}
                Akn_LOGGER.debug('Reading explicitLegalType for populating elemDict...')
                legalTypeID = self.visit(ctx.explicitLegalType())
                Akn_LOGGER.debug('splitMultHref: %s', splitMultHref)
                Akn_LOGGER.debug('DictionaryOfElements: %s', elemDict)
                if isinstance(child, Legal_refParser.Par_multContext):
                    explicitElem = self.visit(child)
                    #print explicitElem
                    Akn_LOGGER.debug('explicitElem reference: %s', explicitElem)
                    multLegislText += explicitElem
                elif isinstance(child, Legal_refParser.Arthro_idContext):
                    elemID = self.visit(child)
                    elemDict['ExplicitArthroContext'] = textToNumbering(elemID, numberingSystem)
                    Akn_LOGGER.debug('Arthro_id: %s', elemID)
                    href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, element = 'ExplicitParContext')
                    #print href
                    Akn_LOGGER.debug('Arthro_id reference: %s', href)
                    multLegislText += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                elif isinstance(child, Legal_refParser.ExplicitLegalTypeContext):
                    element = type(child).__name__
                    href = legislation_href + createHrefFromDictionary(elemDict, 1, element)
                    #print href
                    #we have already traversed this node to create elemDict
                    multLegislText += '<ref href = ' + '"' + href + '"' + '>' + legalTypeID + '</ref>'
                elif isinstance(child, Legal_refParser.ExplicitLegalElementContext):
                    multLegislText += child.getText()
        self.text += multLegislText
        Akn_LOGGER.debug('MultipleLegislation reference: %s', multLegislText)
        Akn_LOGGER.debug('MultipleLegislation node END')
        
    # Visit a parse tree produced by Legal_refParser#arthra.
    def visitArthra(self, ctx):
        self.text += ctx.getText()
        #return self.text

    # Visit a parse tree produced by Legal_refParser#Par_mult.
    def visitPar_mult(self, ctx):
        Akn_LOGGER.debug('Entering Par_mult node...')
        Akn_LOGGER.debug('Par_mult text: %s', ctx.getText())
        #print ctx.getText()
        text = ''
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, Legal_refParser.Arthro_idContext):
                elemID = self.visit(child)
                elemDict['ExplicitArthroContext'] = elemID
                Akn_LOGGER.debug('Par_mult Arthro_id: %s', elemID)
                #href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, element = 'ExplicitParContext')
                #print href
                Akn_LOGGER.debug('Par_mult Arthro_id reference: %s', href)
                #text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
            #elif isinstance(child, tree.Tree.TerminalNodeImpl):
                #text += child.getText()
            elif isinstance(child, Legal_refParser.SingleLegalElementIdContext):
                elemID = child.getText()
                elemDict['ExplicitParContext'] = textToNumbering(elemID, numberingSystem)
                Akn_LOGGER.debug('Par_mult par_id: %s', elemID)
                #href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, element = 'ExplicitPeriptwsiContext')
                #print href
                Akn_LOGGER.debug('Par_mult par reference: %s', href)
                #text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'

        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, element = 'ExplicitPeriptwsiContext')
        text += '<ref href = ' + '"' + href + '"' + '>' + ctx.getText() + '</ref>'        
        return text

    # Visit a parse tree produced by Legal_refParser#arthra.
    #def visitTerminal(self, ctx):
        #print ctx.getText()
        #self.text += ctx.getText()
        #return self.text
    
    # Visit a parse tree produced by Legal_refParser#multipleCompleteLegislation_1.
    def visitMultipleCompleteLegislation_1(self, ctx):
        Akn_LOGGER.debug('Entering MultipleLegislation_1 node...')
        global legislation_href
        global elemDict #A dictionary holding element values (e.g. article:5)
        legislation_href = href_base
        elemDict = {}
        Akn_LOGGER.debug('Reading explicitLegalType for populating elemDict...')
        legalTypeID = self.visit(ctx.explicitLegalType())
        #print elemDict
        #print splitMultHref
        Akn_LOGGER.debug('splitMultHref: %s', splitMultHref)
        Akn_LOGGER.debug('DictionaryOfElements: %s', elemDict)

        text = ''
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, tree.Tree.TerminalNodeImpl):
                text += child.getText()
                #self.text += child.getText()
            elif isinstance(child, Legal_refParser.ArthraContext):
                text += child.getText()
            elif isinstance(child, Legal_refParser.Arthro_idContext):
                elemID = self.visit(child)
                elemDict['ExplicitArthroContext'] = elemID
                href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, element = 'ExplicitParContext')
                #print href
                text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #self.text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #print type(child).__name__
                #print href
            elif isinstance(child, Legal_refParser.ExplicitLegalTypeContext):
                #explicitElem = self.visit(child.getChild(0))
                element = type(child).__name__
                href = legislation_href + createHrefFromDictionary(elemDict, 1, element)
                #print href
                #we have already traversed this node to create elemDict
                text += '<ref href = ' + '"' + href + '"' + '>' + legalTypeID + '</ref>'
                #self.text += '<ref href = ' + '"' + href + '"' + '>' + legalTypeID + '</ref>'
                #print text
            elif isinstance(child, Legal_refParser.M1Context):
                Akn_LOGGER.debug('M1Context node found...')
                explicitElem = self.visit(child)
                text += explicitElem
                #self.text += explicitElem
                #print explicitElem
            elif isinstance(child, Legal_refParser.M2Context):
                Akn_LOGGER.debug('M2Context node found...')
                explicitElem = self.visitM1(child)
                text += explicitElem
                #self.text += explicitElem
                #print explicitElem
            '''elif isinstance(child, Legal_refParser.M3Context):
                Akn_LOGGER.debug('M3Context node found...')
                explicitElem = self.visitM1(child)
                text += explicitElem
                #self.text += explicitElem
                #print explicitElem
            elif isinstance(child, Legal_refParser.M4Context):
                Akn_LOGGER.debug('M4Context node found...')
                explicitElem = self.visitM1(child)
                text += explicitElem
                #self.text += explicitElem
                #print explicitElem
            '''
        Akn_LOGGER.debug('MultipleLegislation_1 text: %s', text)
        Akn_LOGGER.debug('MultipleLegislation_1 node END')
        #print text
        #self.text += text
        #Akn_LOGGER.info('MultipleLegislation_1 text: %s', self.text)
        #return self.text
        return text
    
    # Visit a parse tree produced by Legal_refParser#m1.
    def visitM1(self, ctx):
        #Akn_LOGGER.debug('Entering M1 node...')
        text = ''
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, Legal_refParser.Arthro_idContext):
                elemID = child.getText()
                #print elemID
                elemDict['ExplicitArthroContext'] = elemID
                #Akn_LOGGER.debug('Arthro_id: %s', elemID)
                #print elemDict
                #print splitMultHref
                href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, 'ExplicitParContext')
                text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #print href
            elif isinstance(child, Legal_refParser.ExplicitLegalElementContext):
                explicitElem = self.visit(child.getChild(0))
                #print explicitElem
                text += explicitElem
                #self.text += explicitElem
                #print text
            else:
                text += child.getText()
                #print text
        #print text
        Akn_LOGGER.debug('M1: %s', text)
        #print text
        #self.text += text
        return text
                
    # Visit a parse tree produced by Legal_refParser#arthro_id.
    def visitArthro_id(self, ctx):
        Akn_LOGGER.debug('Entering Arthro_id node...')
        return ctx.getText()

    # Visit a parse tree produced by Legal_refParser#completeLegislation.
    def visitCompleteLegislation(self, ctx):
        Akn_LOGGER.debug('Entering CompleteLegislation node...')
        #print ctx.getText()
        global legislation_href
        global elemDict #A dictionary holding element values (e.g. article:5)
        global splitMultHref
        splitMultHref = 0
        global hasRangeIds

        hasRangeIds = 0
        legislation_href = href_base
        elemDict = {}

        # A completeLegislation node contains exactly 1 explicitLegalType
        # we build href attribute until '!main' section of AkomaNtoso naming convention
        #Akn_LOGGER.debug('Reading explicitLegalType for populating elemDict...')
        legalTypeID = self.visit(ctx.explicitLegalType())
        #multLawsIDs = 0
        #for ch in ctx.explicitLegalType().getChildren():
         #   if isinstance(ch, Legal_refParser.Law_idContext):
         #       multLawsIDs +=1
        #print multLawsIDs
        # we also need to update elemDict with all possible elements and values
        # a completeLegislation might contain so we visit the first child of
        # every explicitLegalElement node. If multiple ids are found update global splitMultHref
        #print len(ctx.explicitLegalElement())
        if len(ctx.explicitLegalElement()) > 0 :
            for n in range(0, len(ctx.explicitLegalElement())):
                #self.visit(ctx.explicitLegalElement()[n])
                #print type(ctx.explicitLegalElement()[n])
                #a= ctx.explicitLegalElement()[n]
                #object_methods = [method_name for method_name in dir(a)
                #      if callable(getattr(a, method_name))]
                #print object_methods
                childType = ctx.explicitLegalElement()[n].getChild(0)
                #print type(childType)
                # This is if we want to get the href until paragraphs!
                if isinstance(childType, Legal_refParser.ExplicitArthroContext) or isinstance(childType, Legal_refParser.ExplicitParContext):
                    for child in childType.getChildren():
                        if isinstance(child, Legal_refParser.MultipleLegalElementIdsContext):
                            splitMultHref = 1
                            elementIds = []
                            for child_lv2 in child.getChildren():
                                if isinstance(child_lv2, Legal_refParser.SingleLegalElementIdContext):
                                    #print type(child_lv2)
                                    elemID = child_lv2.getText()
                                    #print type(child_lv2.getText())
                                    elemID = textToNumbering(elemID, numberingSystem)
                                    #print elemID
                                    elementIds.append(elemID)
                            elemDict[type(childType).__name__] = elementIds
                            
                        if isinstance(child, Legal_refParser.SingleLegalElementIdContext):
                            elemID = child.getText()
                            #print elemID
                            #print type(elemID)
                            elemID = textToNumbering(elemID, numberingSystem)
                            #print elemID
                            elemDict[type(childType).__name__] = elemID

                        if isinstance(child, Legal_refParser.Range_idContext):
                            hasRangeIds = 1
                            elemID = ''
                            #print elemDict
                            for child_lv2 in child.getChildren():
                                #print type(child_lv2)
                                if isinstance(child_lv2, Legal_refParser.SingleLegalElementIdContext):
                                    elemID += 'par_' + child_lv2.getText() + '->'
                            
                            elemID = re.sub(r'->$', '', elemID)
                            #print elemID
                            elemIDparts = elemID.split('->')
                            elemID = elemIDparts[0] + '->art_' + elemDict.get('ExplicitArthroContext', '0') + '__' +elemIDparts[1]
                            elemID = re.sub(r'^par_', '', elemID)
                            #print elemID
                            #elemID = textToNumbering(elemID, numberingSystem)
                            #print elemID
                            elemDict[type(childType).__name__] = elemID

        # This is in case no explicitLegal element exists and arthro_id is present
        elif ctx.arthro_id():
            elemID = ctx.getChild(2).getText()
            #print elemID
            elemID = textToNumbering(elemID, numberingSystem)
            elemDict['ExplicitArthroContext'] = elemID

        # This is in case no explicitLegal element exists and there is a range_id in articles
        elif len(ctx.explicitLegalElement()) == 0  and ctx.range_id():
            hasRangeIds = 1
            elemID=''
            for child_lv2 in ctx.range_id().getChildren():
                #print type(child_lv2)
                if isinstance(child_lv2, Legal_refParser.SingleLegalElementIdContext):
                    elemID += 'art_' + textToNumbering(child_lv2.getText(), numberingSystem) + '->'
            elemID = re.sub(r'->$', '', elemID)
            elemID = re.sub(r'^art_', '', elemID)
            #print re.sub(r'->$', '', elemID)
            elemDict['ExplicitArthroContext'] = elemID
            #print elemDict['ExplicitArthroContext']

        #print elemDict
        #print splitMultHref
        Akn_LOGGER.debug('splitMultHref: %s', splitMultHref)
        Akn_LOGGER.debug('DictionaryOfElements: %s', elemDict)
        text = ''
        # If multiple ids has been found write each element into a <ref> node
        if splitMultHref == 1:
            Akn_LOGGER.debug('This reference contains multiple ids in some elements!')
            for child in ctx.getChildren():
                if isinstance(child, Legal_refParser.ExplicitLegalElementContext):
                    explicitElem = self.visit(child.getChild(0))
                    #print explicitElem
                    #text += '<ref href = ' + '"' + href + '"' + '>' + explicitElem + '</ref>'
                    text += explicitElem
                    #self.text += explicitElem
                if isinstance(child, Legal_refParser.ExplicitLegalTypeContext):
                    explicitElem = self.visit(child)
                    #print explicitElem
                    #print type(child).__name__
                    element = type(child).__name__
                    #print explicitElem[1]
                    href = legislation_href + createHrefFromDictionary(elemDict, 1, element)
                    #print href
                    text += '<ref href = ' + '"' + href + '"' + '>' + explicitElem + '</ref>'
                    #self.text += '<ref href = ' + '"' + href + '"' + '>' + explicitElem + '</ref>'
                if isinstance(child, tree.Tree.TerminalNodeImpl):
                    text += child.getText()
        # otherwise write all completeLegislation text into a <ref> node
        else:
            Akn_LOGGER.debug('This reference contains single ids in all elements!')
            href = legislation_href + createHrefFromDictionary(elemDict, 0)
            if hasRangeIds == 1:
                href = re.sub(r'#', '~', href)
            Akn_LOGGER.debug('href: %s', href)
            text =  '<ref href = ' + '"' + href + '"' + '>' + ctx.getText() + '</ref>'
            #self.text =  '<ref href = ' + '"' + href + '"' + '>' + ctx.getText() + '</ref>'
            Akn_LOGGER.debug('reference_text: %s', href)
            #print etree.fromstring(text)
        Akn_LOGGER.debug('CompleteLegislation text: %s', text)
        Akn_LOGGER.debug('CompleteLegislation node END')
        #print text
        #self.text += text
        #return self.text
        return text

    # Visit a parse tree produced by Legal_refParser#explicitLegalElement.
    def visitExplicitLegalElement(self, ctx):
        Akn_LOGGER.debug('Entering ExplicitLegalElement node...')
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by Legal_refParser#explicitArthro.
    def visitExplicitArthro(self, ctx):
        Akn_LOGGER.debug('Entering ExplicitArthro node...')
        Akn_LOGGER.debug('ExplicitArthro text: %s', ctx.getText())
        #global elemDict
        #arthro_id = self.visit(ctx.singleLegalElementId()[0])
        #print type(arthro_id)
        #elemDict['ExplicitArthroContext'] = str(arthro_id)
        #global splitMultHref
        text = ''
        indx = 0
        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
        #print href
        for child in ctx.getChildren():
            if isinstance(child, Legal_refParser.SingleLegalElementIdContext):
                Akn_LOGGER.debug('SingleLegalElementId found...')
                arthro_id = child.getText()
                elemDict['ExplicitArthroContext'] = textToNumbering(arthro_id, numberingSystem)
                href += '#art_' + elemDict[type(ctx).__name__]
                text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #self.text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #Akn_LOGGER.debug('href: %s', href)
            elif isinstance(child, Legal_refParser.MultipleLegalElementIdsContext):
                Akn_LOGGER.debug('MultipleLegalElementIds found...')
                elementIds = []
                #splitMultHref = 1
                #for n in range(0, len(ctx.explicitLegalElement())):
                for child_lv2 in child.getChildren():
                    #print type(child_lv2)
                    if isinstance(child_lv2, Legal_refParser.SingleLegalElementIdContext):
                        #print indx
                        elemID = child_lv2.getText()   
                        elemID = textToNumbering(elemID, numberingSystem)
                        #print elemID
                        elementIds.append(elemID)
                        elemDict[type(ctx).__name__] = elementIds
                        #print elemDict
                        #print indx
                        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
                        href += '#art_' + elemDict[type(ctx).__name__][indx]
                        text += '<ref href = ' + '"' + href + '"' + '>' + child_lv2.getText() + '</ref>'
                        #self.text += '<ref href = ' + '"' + href + '"' + '>' + child_lv2.getText() + '</ref>'
                        indx += 1
                        Akn_LOGGER.debug('href: %s', href)
                        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
                    else:
                        text += child_lv2.getText()
                        #self.text += child_lv2.getText()
            elif isinstance(child, tree.Tree.TerminalNodeImpl):
                text += child.getText()
                #self.text += child.getText()
                
        Akn_LOGGER.debug('ExplicitArthroText: %s', text)        
        #print text
        return  text
    
    # Visit a parse tree produced by Legal_refParser#explicitArthro.
    def visitExplicitPar(self, ctx):
        Akn_LOGGER.debug('Entering ExplicitPar node...')
        Akn_LOGGER.debug('ExplicitPar text: %s', ctx.getText())
        #global splitMultHref
        #href = legislation_href + createHrefFromDictionary(elemDict, 1, element)
        text = ''
        indx = 0
        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
        #print href
        for child in ctx.getChildren():
            if isinstance(child, Legal_refParser.SingleLegalElementIdContext):
                Akn_LOGGER.debug('SingleLegalElementId found...')
                par_id = self.visit(ctx.singleLegalElementId())
                #href = par_href + '__par_' + par_id
                elemDict['ExplicitParContext'] = par_id
                href += '__par_' + elemDict[type(ctx).__name__]
                text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #self.text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                Akn_LOGGER.debug('href: %s', href)
            elif isinstance(child, Legal_refParser.MultipleLegalElementIdsContext):
                Akn_LOGGER.debug('MultipleLegalElementIds found...')
                #splitMultHref = 1
                #for n in range(0, len(ctx.explicitLegalElement())):
                elementIds = []
                for child_lv2 in child.getChildren():
                    #print type(child_lv2)
                    if isinstance(child_lv2, Legal_refParser.SingleLegalElementIdContext):
                        #print indx
                        elemID = child_lv2.getText()   
                        elemID = textToNumbering(elemID, numberingSystem)
                        #print elemID
                        #elementIds.append(elemID)
                        #elemDict[type(ctx).__name__] = elementIds
                        elemDict[type(ctx).__name__] = elemID
                        #print elemDict
                        #print indx
                        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
                        #href += '__par_' + elemDict[type(ctx).__name__][indx]
                        href += '__par_' + elemDict[type(ctx).__name__]
                        text += '<ref href = ' + '"' + href + '"' + '>' + child_lv2.getText() + '</ref>'
                        #self.text += '<ref href = ' + '"' + href + '"' + '>' + child_lv2.getText() + '</ref>'
                        indx += 1
                        Akn_LOGGER.debug('href: %s', href)
                        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
                    else:
                        text += child_lv2.getText()
                        #self.text += child_lv2.getText()
            elif isinstance(child, tree.Tree.TerminalNodeImpl):
                text += child.getText()
                #self.text += child.getText()

        Akn_LOGGER.debug('ExplicitParText: %s', text)   
        #print text
        return  text

    '''
    # Visit a parse tree produced by Legal_refParser#explicitArthro.
    def visitExplicitPeriptwsi(self, ctx):
        Akn_LOGGER.debug('Entering ExplicitPeriptwsi node...')
        Akn_LOGGER.debug('ExplicitPeriptwsi text: %s', ctx.getText())
        #global elemDict
        #arthro_id = self.visit(ctx.singleLegalElementId()[0])
        #print type(arthro_id)
        #elemDict['ExplicitArthroContext'] = str(arthro_id)
        text=''
        indx = 0
        Akn_LOGGER.debug('elemDict: %s', elemDict)
        Akn_LOGGER.debug('ctx type: %s', type(ctx).__name__)
        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
        for child in ctx.getChildren():
            if isinstance(child, Legal_refParser.SingleLegalElementIdContext):
                Akn_LOGGER.debug('SingleLegalElementId found...')
                case_id = self.visit(ctx.singleLegalElementId())
                elemDict['ExplicitPeriptwsiContext'] = case_id
                href += '__case_' + elemDict[type(ctx).__name__]
                text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                #self.text += '<ref href = ' + '"' + href + '"' + '>' + child.getText() + '</ref>'
                Akn_LOGGER.debug('href: %s', href)
            elif isinstance(child, Legal_refParser.MultipleLegalElementIdsContext):
                Akn_LOGGER.debug('MultipleLegalElementIds found...')
                elementIds = []
                for child_lv2 in child.getChildren():
                    if isinstance(child_lv2, Legal_refParser.SingleLegalElementIdContext):
                        #print indx
                        elemID = child_lv2.getText()   
                        elemID = textToNumbering(elemID, numberingSystem)
                        #print elemID
                        #elementIds.append(elemID)
                        #elemDict[type(ctx).__name__] = elementIds
                        elemDict[type(ctx).__name__] = elemID
                        #print elemDict
                        #print indx
                        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
                        #href += '__case_' + elemDict[type(ctx).__name__][indx]
                        href += '__case_' + elemDict[type(ctx).__name__]
                        #print href
                        text += '<ref href = ' + '"' + href + '"' + '>' + child_lv2.getText() + '</ref>'
                        #self.text += '<ref href = ' + '"' + href + '"' + '>' + child_lv2.getText() + '</ref>'
                        indx += 1
                        Akn_LOGGER.debug('href: %s', href)
                        href = legislation_href + createHrefFromDictionary(elemDict, splitMultHref, type(ctx).__name__)
                    else:
                        text += child_lv2.getText()
                        #self.text += child_lv2.getText()
            elif isinstance(child, tree.Tree.TerminalNodeImpl):
                text += child.getText()
                #self.text += child.getText()
        Akn_LOGGER.debug('ExplicitPeriptwsiText: %s', text) 
        #print text
        return text
    '''
    
    # Visit a parse tree produced by Legal_refParser#explicitLegalType.
    def visitExplicitLegalType(self, ctx):
        '''With this method we traverse through a parse tree and update
        elemDict with possible values found in child nodes

        possible types (based on grammar):
            Legislative_type: This type contains all laws and presidential decrees
            Law_id: The id of the legislative type (usually in the form 'number/year')
            ExplicitKwdikas : A special type of laws (code laws) that the legislator usually
                    make a reference using its title and not law_id (above)
            Syntagma : Constitution (same as ExplicitKwdikas)
        '''
        Akn_LOGGER.debug('Entering ExplicitLegalType node...')
        Akn_LOGGER.debug('ExplicitLegalType text: %s', ctx.getText())
        #legalTypeID = self.visitChildren(ctx)
        #return [legalTypeID, ctx.getText()]
        #return self.visitChildren(ctx)
        global elemDict
        #traverse all childs of ExplicitLegalType
        for child in ctx.getChildren():
            if isinstance(child, Legal_refParser.Legislative_typeContext):
                #print type(child.getChild(0))
                if isinstance(child.getChild(0), Legal_refParser.ActsContext):
                    elemDict['type'] = "act/law"
                elif isinstance(child.getChild(0), Legal_refParser.Presidential_decreeContext):
                    elemDict['type'] = "act/presidentialDecree"
                elif isinstance(child.getChild(0), Legal_refParser.Compulsory_lawContext):
                    elemDict['type'] = "act/compulsoryLaw"
                elif isinstance(child.getChild(0), Legal_refParser.Decree_lawContext):
                    elemDict['type'] = "act/decreeLaw"
                elif isinstance(child.getChild(0), Legal_refParser.Royal_decreeContext):
                    elemDict['type'] = "act/royalDecree"
                elif isinstance(child.getChild(0), Legal_refParser.DecreeContext):
                    elemDict['type'] = "act/decree"
            elif isinstance(child, Legal_refParser.Law_idContext):
                law_id = self.visit(child)
                #print law_id.split(r'/|(|)')
                law_id_split = re.compile(r"/|\||\\").split(law_id)
                #print law_id_split[1]
                #sys.exit()
                # legalYear might be in dd.mm.yyyy format
                # akomaNtoso format in this case must be YYYY or YYYY-MM-DD
                if len(law_id_split[1]) == 5:
                    elemDict['legalYear'] = law_id_split[1]
                elif len(law_id_split[1]) == 2:
                    if int(law_id_split[1]) in range(0, 19):
                        elemDict['legalYear'] = '20' + law_id_split[1]
                    else:
                        elemDict['legalYear'] = '19' + law_id_split[1]
                elif len(law_id_split[1]) != 4 and len(law_id_split[1]) != 2 :
                    date = re.split('\.|-', law_id_split[1])
                    #print date
                    #date_str = datetime.date(int(date[2]), int(date[1]), int(date[0])).isoformat()
                    #elemDict['legalYear'] = date_str
                    try:
                        elemDict['legalYear'] = date[2]
                    except IndexError:
                         elemDict['legalYear'] = '0'
                else:
                    try:
                        elemDict['legalYear'] = law_id_split[1]
                    except IndexError:
                        elemDict['legalYear'] = '0'
                elemDict['legalNumber'] = law_id_split[0]
            elif isinstance(child, Legal_refParser.ExplicitKwdikasContext):
                kwdikas = self.visit(child)
            elif isinstance(child, Legal_refParser.SyntagmaContext):
                syntagma = self.visit(child)
        return ctx.getText()

    # Visit a parse tree produced by Legal_refParser#explicitKwdikas.
    def visitExplicitKwdikas(self, ctx):
        Akn_LOGGER.debug('Entering ExplicitKwdikas node...')
        Akn_LOGGER.debug('ExplicitKwdikas text: %s', ctx.getText())
        #global legislation_href
        #return self.visitChildren(ctx)
        #print type(ctx.getChild(0)).__name__
        global elemDict
        text = ''
        item_list = [e for e in dir(ctx) if e not in ('OLOMELEIA', 'SPACE')]
        legalTypeID = getTokenName(ctx, dir(ctx), codeLaws, 'none_0_0')
        Akn_LOGGER.debug('Kwdikas dictionary search result: %s',  legalTypeID)
        elemDict['type'] = legalTypeID.split('_')[0]
        elemDict['legalNumber'] = legalTypeID.split('_')[1]
        elemDict['legalYear'] = legalTypeID.split('_')[2]
        #print legalTypeID
        text += ctx.getText()
        '''
        for child in ctx.getChildren():
            #print type(child)
            if isinstance(child, tree.Tree.TerminalNodeImpl):
                text+= child.getText()
            else:
                #print type(ctx.getChild(0)).__name__
                #print child.getRuleIndex()
                #print child.getAltNumber()
                print dir(ctx)
                sys.exit()
                legalTypeID = codeLaws.get(type(ctx.getChild(0)).__name__, 'none_0_0')
                elemDict['type'] = legalTypeID.split('_')[0]
                elemDict['legalNumber'] = legalTypeID.split('_')[1]
                elemDict['legalYear'] = legalTypeID.split('_')[2]
                text+= child.getText()
                #self.text+= child.getText()
        #print text
        #print elemDict
        '''
        return text


    # Visit a parse tree produced by Legal_refParser#syntagma.
    def visitSyntagma(self, ctx):
        Akn_LOGGER.debug('Entering Syntagma node...')
        #global legislation_href
        #legislation_href += "syntagma/"
        #return self.visitChildren(ctx)
        global elemDict
        elemDict['type'] = 'act/constitution'
        elemDict['legalYear'] = '2001'
        return ctx.getText()
    
    # Visit a parse tree produced by Legal_refParser#law_id.
    def visitLaw_id(self, ctx):
        #if self.visitChildren(ctx) is not None:
         #   law_id =  self.visitChildren(ctx)
        #else:
        law_id =  ctx.getText()
        return law_id

    # Visit a parse tree produced by Legal_refParser#singleLegalElementId.
    def visitSingleLegalElementId(self, ctx):
        #Akn_LOGGER.debug('Entering SingleLegalElementId node...')
        return ctx.getText()

    # Visit a parse tree produced by Legal_refParser#multipleLegalElementIds.
    def visitMultipleLegalElementIds(self, ctx):
        #Akn_LOGGER.debug('Entering MultipleLegalElementIds node...')
        #text = ''
        #for child in ctx.getChildren():
         #   if isinstance(child, Legal_refParser.SingleLegalElementIdContext):
         #       text += '<ref href = ' + '"' + str(legislation_href.encode('utf-8')) + '"' + '>' + child.getText() + '</ref>'
          #  elif isinstance(child, tree.Tree.TerminalNodeImpl):
          #      text += child.getText()
        return ctx.getText()

