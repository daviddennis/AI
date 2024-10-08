from nltk.stem.wordnet import WordNetLemmatizer
from django.db.models import Q
from wikipedia.lib.parser import Parser
from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.group_manager import GroupManager
from wikipedia.lib.word_mgr import WordManager
from wikipedia.lib.time_mgr import TimeManager
from wikipedia.models import *
from django.core.exceptions import MultipleObjectsReturned
import operator
import sys
from annoying.functions import get_object_or_None

class Interpreter():

    ref_words = ['THIS', 'THESE', 'THAT', 'THOSE', 'THEIR', 'THERE', 'OUR']

    def __init__(self):
        self.parser = Parser()        
        self.pr = PatternRecognizer()
        self.group_mgr = GroupManager()
        self.interpretations = []
        self.topic = None
        self.word_mgr = WordManager()
        self.thought_processor = None
        self.time_mgr = None
        self.restrict = set()
        self.learned = {}
        self.struct_mgr = None

        self.user = get_object_or_None(Concept, name="DAVID DENNIS")
        self.ai = get_object_or_None(Concept, name="AI")

        self.one_item = None

    def interpret(self, parsed_sentence, last_transform=None, thinker=None):
        if thinker:
            self.thinker = thinker

        if parsed_sentence not in self.interpretations:
            self.interpretations += [parsed_sentence]
            #self.add_interpretation(parsed_sentence)

        if self.pr.recognize(parsed_sentence, "SW:if ... ... ... SW:then ... ... ..."):
            self.ngram_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "STRING SW:is CONCEPT:past CONCEPT:verb SW:of CONCEPT"):
            self.ngram_past_verb(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT:everything SWS:that_is_a CONCEPT"):
            self.ngram_everything(parsed_sentence)

        self.interpret_unigrams(parsed_sentence)
        self.interpret_bigrams(parsed_sentence)
        self.interpret_trigrams(parsed_sentence)
        self.interpret_4grams(parsed_sentence)
        self.interpret_5grams(parsed_sentence)
        self.interpret_6grams(parsed_sentence)
        self.interpret_7grams(parsed_sentence)
        
        self.track_topic(parsed_sentence)

        return self.interpretations #self.return_interpretations()

    def interpret_unigrams(self, parsed_sentence):
        for i, unigram in enumerate(parsed_sentence):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+1:]
            if self.pr.recognize([unigram], 'PUNC:"'):
                self.unigram_double_quote(unigram, before, after)
            if self.pr.recognize([unigram], "NAME"):
                self.unigram_name(unigram, before, after)
            if self.pr.recognize([unigram], "SW"):
                self.unigram_quantifier(unigram, before, after)
                self.unigram_prep(unigram, before, after)
                self.unigram_anaphora(unigram, before, after)
            if self.pr.recognize([unigram], "SW:am"):
                self.unigram_am(unigram, before, after)
            if self.pr.recognize([unigram], "SW:an"):
                self.unigram_an(unigram, before, after)
            if self.pr.recognize([unigram], "SW:my"):
                self.unigram_my(unigram, before, after)
            if self.pr.recognize([unigram], "SW:you"):
                self.unigram_you(unigram, before, after)
            if self.pr.recognize([unigram], "SW:it"):
                self.unigram_it(unigram, before, after)
            if self.pr.recognize([unigram], "SW:so"):
                self.unigram_so(unigram, before, after)
            if self.pr.recognize([unigram], "SW:we"):
                self.unigram_we(unigram, before, after)
            if self.pr.recognize([unigram], "SW:i"):
                self.unigram_i(unigram, before, after)
            if self.pr.recognize([unigram], "SW:are"):
                self.unigram_are(unigram, before, after)
            if self.pr.recognize([unigram], "SW:can"):
                self.unigram_exclude_word(unigram, before, after)
            if self.pr.recognize([unigram], "SW:will"):
                self.unigram_exclude_word(unigram, before, after)
            if self.pr.recognize([unigram], "SWS:was_an"):
                self.unigram_was_an(unigram, before, after)
            if self.pr.recognize([unigram], "SWS:was_a"):
                self.unigram_was_a(unigram, before, after)
            if self.pr.recognize([unigram], "SWS:are_a"):
                self.unigram_are_a(unigram, before, after)
            if self.pr.recognize([unigram], "SWS:on_then"):
                self.unigram_on_then(unigram, before, after)
            if self.pr.recognize([unigram], "SWS"):
                self.unigram_sws(unigram, before, after)
            if self.pr.recognize([unigram], "CONCEPT"):
                self.unigram_concept(unigram, before, after)
            if self.pr.recognize([unigram], "CONCEPT:the_way"):
                self.unigram_exclude_word(unigram, before, after)
            if self.pr.recognize([unigram], "PUNC:,"):
                self.unigram_comma(unigram, before, after)
            if self.pr.recognize([unigram], "VERB"):
                self.unigram_verb(unigram, before, after)
            #    self.unigram_on_then(unigram, before, after)
            

    def interpret_bigrams(self, parsed_sentence):
        bigrams = [(x,y) for x,y in zip(parsed_sentence, parsed_sentence[1:])]
        for i, bigram in enumerate(bigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+2:]
            if self.pr.recognize(bigram, "Q CONCEPT"):
                self.bigram_q_concept(bigram, before, after)
            #if self.pr.recognize(bigram, "CONCEPT CONCEPT"):
            #    self.bigram_adj_c(bigram, before, after)
            if self.pr.recognize(bigram, "CONCEPT:type SW:of"):
                self.bigram_type_of(bigram, before, after)
            if self.pr.recognize(bigram, "SW:the CONCEPT"):
                self.bigram_the(bigram, before, after)
            if self.pr.recognize(bigram, "SW:a CONCEPT"):
                self.bigram_a(bigram, before, after)
            if self.pr.recognize(bigram, "SW:a VERB"):
                self.bigram_a_verb(bigram, before, after)
            if self.pr.recognize(bigram, "CONCEPT SWS:are_an"):
                self.bigram_are_an(bigram, before, after)
            if self.pr.recognize(bigram, "SW:that CONCEPT"):
                self.bigram_recall(bigram, before, after)
            if self.pr.recognize(bigram, "NUMBER CONCEPT"):
                self.bigram_amount_or_time(bigram, before, after)
            if self.pr.recognize(bigram, "SW:are SW:a"):
                self.bigram_are_a(bigram, before, after)
            if self.pr.recognize(bigram, "SW SW"):
                self.bigram_sw(bigram, before, after)
            if self.pr.recognize(bigram, "SW:the CONCEPT:way"):
                self.bigram_exclude(bigram, before, after)
            if self.pr.recognize(bigram, "VERB SW"):
                self.bigram_verb_prep(bigram, before, after)
            if self.pr.recognize(bigram, "SW:your CONCEPT"):
                self.bigram_your(bigram, before, after)
            if self.pr.recognize(bigram, "SW CONCEPT"):
                self.bigram_anaphoric_ref(bigram, before, after)
            if self.pr.recognize(bigram, "PREP:in NUMBER"):
                self.bigram_year(bigram, before, after)
            if self.pr.recognize(bigram, "CONCEPT NUMBER"):
                self.bigram_small_date(bigram, before, after)
            if self.pr.recognize(bigram, "TIME NUMBER"):
                self.bigram_date_year(bigram, before, after)


    def interpret_trigrams(self, parsed_sentence):
        trigrams = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        for i, trigram in enumerate(trigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if self.pr.recognize(trigram, "CONCEPT VERB CONCEPT"):
                self.trigram_verb_construct(trigram, before, after)
            if self.pr.recognize(trigram, "SWS:is_a NUMBER CONCEPT"):
                self.trigram_isa_number_c(trigram, before, after)

            # List formation
            if self.pr.recognize(trigram, "CONCEPT PUNC:, CONCEPT"):
                self.trigram_punc_list(trigram, before, after)
            if self.pr.recognize(trigram, "LIST PUNC:, CONCEPT"):
                self.trigram_concat_list(trigram, before, after)
            if self.pr.recognize(trigram, "LIST SW:and CONCEPT"):
                self.trigram_and_list(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SW:and CONCEPT"):
                self.trigram_and_to_list(trigram, before, after)

            if self.pr.recognize(trigram, "VERB SWS:to_the CONCEPT"):
                self.trigram_to_the(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SWS:is_an CONCEPT"):
                self.trigram_is_an(trigram, before, after)

            # Math
            if self.pr.recognize(trigram, "NUMBER PUNC:. NUMBER"):
                self.trigram_float(trigram, before, after)
            if self.pr.recognize(trigram, "NUMBER PUNC:^ NUMBER"):
                self.trigram_exp(trigram, before, after)
            if self.pr.recognize(trigram, "NUMBER CONCEPT:x NUMBER"):
                self.trigram_multiply(trigram, before, after)

            #if self.pr.recognize(trigram, "... PUNC:, ..."):
            #    self.trigram_comma(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SW:are LIST"):
                self.trigram_are_list(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SW:are CONCEPT"):
                self.trigram_are(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SWS:such_as CONCEPT"):
                self.trigram_such_as(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SWS:am_a CONCEPT"):
                self.trigram_am_a(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SWS:will_be CONCEPT"):
                self.trigram_will_be(trigram, before, after)                
            if self.pr.recognize(trigram, "SWS:was_a TIME CONCEPT"):
                self.trigram_time(trigram, before, after)                
            if self.pr.recognize(trigram, "VERB SW:and VERB"):
                self.trigram_v_and_v(trigram, before, after)
            if self.pr.recognize(trigram, "ADJECTIVE SW:or ADJECTIVE"):
                self.trigram_adj_and_adj(trigram, before, after)
            if self.pr.recognize(trigram, "NUMBER PUNC:- NUMBER"):
                self.trigram_year_range(trigram, before, after)
            if self.pr.recognize(trigram, "NUMBER CONCEPT NUMBER"):
                self.trigram_alt_date(trigram, before, after)


    def interpret_4grams(self, parsed_sentence):
        _4grams = [(w,x,y,z) for w,x,y,z in zip(parsed_sentence, 
                                                parsed_sentence[1:],
                                                parsed_sentence[2:],
                                                parsed_sentence[3:])]
        for i, _4gram in enumerate(_4grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+4:]
            if self.pr.recognize(_4gram, "CONCEPT SWS:is_the CONCEPT CONCEPT"):
                self._4gram_is_the(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT:file CONCEPT PUNC:. CONCEPT:CSV"):
                self._4gram_file(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT SWS:is_a ADJECTIVE CONCEPT"):
                self._4gram_adj(_4gram, before, after)
            if self.pr.recognize(_4gram, "NUMBER CONCEPT SW:of CONCEPT"):
                self._4gram_amount(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT SWS:is_the CONCEPT SW:of"):
                self._4gram_is_the_of(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT SWS:was_the NUMBER CONCEPT"):
                self._4gram_was_the_number(_4gram, before, after)
            if self.pr.recognize(_4gram, "SWS:is_a CONCEPT SW:and CONCEPT"):
                self._4gram_and(_4gram, before, after)
            if self.pr.recognize(_4gram, "VERB CONCEPT SW:and CONCEPT"):
                self._4gram_verb_and(_4gram, before, after)
            if self.pr.recognize(_4gram, "PREP:on CONCEPT NUMBER NUMBER"):
                self._4gram_date(_4gram, before, after)
            if self.pr.recognize(_4gram, "PUNC:' ... ... PUNC:'"):
                self._4gram_quoted_item(_4gram, before, after)
            if self.pr.recognize(_4gram, "... PUNC:' SW:s CONCEPT"):
                self._4gram_x_to_c(_4gram, before, after)

    def interpret_5grams(self, parsed_sentence):
        _5grams = [(v,w,x,y,z) for v,w,x,y,z in zip(parsed_sentence, 
                                                    parsed_sentence[1:],
                                                    parsed_sentence[2:],
                                                    parsed_sentence[3:],
                                                    parsed_sentence[4:])]
        for i, _5gram in enumerate(_5grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+5:]
            if self.pr.recognize(_5gram, "CONCEPT PUNC:, CONCEPT SW:and CONCEPT"):
                self._5gram_small_list_3(_5gram, before, after)
            if self.pr.recognize(_5gram, "CONCEPT VERB CONCEPT VERB CONCEPT"):
                self._5gram_cvcvc(_5gram, before, after)
            if self.pr.recognize(_5gram, "CONCEPT VERB CONCEPT SW:and CONCEPT"):
                self._5gram_and(_5gram, before, after)
            if self.pr.recognize(_5gram, "CONCEPT SW:are VERB SW:by CONCEPT"):
                self._5gram_by(_5gram, before, after)
            if self.pr.recognize(_5gram, "PREP:on CONCEPT NUMBER PUNC:, NUMBER"):
                self._5gram_date(_5gram, before, after)
            if self.pr.recognize(_5gram, "NUMBER PUNC:/ NUMBER PUNC:/ NUMBER"):
                self._5gram_long_slash_date(_5gram, before, after)
            #if self.pr.recognize(_5gram, "VERB PREP CONCEPT PREP CONCEPT"):  ### spoke on island of corsica - not working
            #    self._5gram_break_complex_verb(_5gram, before, after)


    def interpret_6grams(self, parsed_sentence):

        return

        _6grams = [(u,v,w,x,y,z) for u,v,w,x,y,z in zip(parsed_sentence, 
                                                        parsed_sentence[1:],
                                                        parsed_sentence[2:],
                                                        parsed_sentence[3:],
                                                        parsed_sentence[4:],
                                                        parsed_sentence[5:])]
        for i, _6gram in enumerate(_6grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+6:]
            if self.pr.recognize(_6gram, "CONCEPT SW VERB SW CONCEPT SW:to"):
               self._6gram_c_v_c_to(_6gram, before, after)
            #if self.pr.recognize(_6gram, "CONCEPT SW:is VERB SW VERB CONCEPT"):
            #    self._6gram_verb_prep(_6gram, before, after)


    def interpret_7grams(self, parsed_sentence):
        _7grams = [(t,u,v,w,x,y,z) for t,u,v,w,x,y,z in zip(parsed_sentence, 
                                                            parsed_sentence[1:],
                                                            parsed_sentence[2:],
                                                            parsed_sentence[3:],
                                                            parsed_sentence[4:],
                                                            parsed_sentence[5:],
                                                            parsed_sentence[6:])]
        for i, _7gram in enumerate(_7grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+7:]
            if self.pr.recognize(_7gram, "CONCEPT SWS:is_what CONCEPT VERB SW:to VERB CONCEPT"):
                self._7gram_what(_7gram, before, after)
            

    def unigram_sws(self, unigram, before, after):
        sws = unigram
        stopwords = [Stopword(sw) for sw in sws.string.split(' ')]
        self.add_interpretation(before + stopwords + after)

    def unigram_on_then(self, unigram, before, after):
        sws = unigram
        concept_name = sws.string.split(' ')[0]
        concept_or_none = get_object_or_None(Concept, name=concept_name)
        if concept_or_none:
            print concept_or_none
            self.add_interpretation(before + [concept_or_none, Stopword('THEN')] + after)

    def unigram_are(self, unigram, before, after):
        pass
        #sw = unigram
        #self.interpret(before + [Stopword('IS')] + after)

    def unigram_it(self, unigram, before, after):
        if self.topic:
            #print before + [self.topic] + after
            self.interpret(before + [self.topic] + after)

    def unigram_so(self, unigram, before, after):
        self.interpret(before + after)

    def unigram_was_an(self, unigram, before, after):
        was_a = get_object_or_None(StopwordSequence, string="was a".upper())
        self.add_interpretation(before + [was_a] + after)

    def unigram_comma(self, unigram, before, after):
        comma = unigram
        self.add_interpretation(before + after)

    def unigram_verb(self, unigram, before, after):
        verb = unigram
        if verb.form == 'participle':
            concept_or_none = get_object_or_None(Concept, name=verb.participle_name)
            if concept_or_none:
                self.add_interpretation(before + [concept_or_none] + after)
        #for verb_syn in self.word_mgr.get_verb_syns(verb, size=3):
        #    self.add_interpretation(before + [verb_syn] + after, recurse=False)

    def unigram_are_a(self, unigram, before, after):
        sws = unigram
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [is_a] + after)

    def unigram_i(self, unigram, before, after):        
        self.add_interpretation(before + [self.user] + after)

    def unigram_concept(self, unigram, before, after):
        concept = unigram
        self.remember(concept)
        if ' OF ' in concept.name:
            concept_name1, concept_name2 = concept.name.split(' OF ')
            if concept_name1 not in ('THE') and concept_name2 not in ('THE'):
                concept1 = get_object_or_None(Concept, name=concept_name1)
                concept2 = get_object_or_None(Concept, name=concept_name2)
                if concept1 and concept2:
                    self.add_interpretation(before + [concept1, Stopword('OF'), concept2] + after)
        if concept.name.startswith('THE '):
            new_concept_name = concept.name.replace('THE ','',1)
            new_concept = get_object_or_None(Concept, name=new_concept_name)
            if new_concept:
                if concept.hit < 1:
                    concept.hit += 1
                    new_concept.hit += 1
                    self.add_interpretation(before + [Stopword('THE'), new_concept] + after)
        if self.time_mgr.recognize_time(concept.name):
            self.add_interpretation(before + [Time(concept.name)] + after)

        alias_concepts = self.word_mgr.get_aliases(concept)
        for ac in alias_concepts:
            if ac not in self.restrict:
                self.restrict.add(ac)
                self.add_interpretation(before + [ac] + after)

        # try:
        #     name_or_none = get_object_or_None(PersonName, name=concept.name)
        # except MultipleObjectsReturned:
        #     PersonName.objects.filter(name=concept.name).all().delete()
        #     name_or_none, created = PersonName.objects.get_or_create(name=concept.name)
        # if name_or_none:
        #     self.add_interpretation(before + [name_or_none] + after)

        # adj_or_none = get_object_or_None(Adjective, name=concept.name)
        # if adj_or_none:
        #     self.add_interpretation(before + [adj_or_none] + after)
        # else:
        #     adj_or_none = get_object_or_None(Adjective, superlative=concept.name) 
        #     if adj_or_none:
        #         self.add_interpretation(before + [adj_or_none] + after)       

        #verb_or_none = get_object_or_None(Verb, name=concept.name)
        #if verb_or_none:
        #    self.add_interpretation(before + [verb_or_none] + after)

    def unigram_exclude_word(self, unigram, before, after):
        self.add_interpretation(before + after)

    def unigram_we(self, unigram, before, after):
        if self.topic:
            self.add_interpretation(before + [self.topic] + after)

    def unigram_was_a(self, unigram, before, after):
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [is_a] + after)

    def unigram_am(self, unigram, before, after):
        sw_am = unigram
        sw_is = Stopword("IS")
        self.add_interpretation(before + [sw_is] + after)

    def unigram_double_quote(self, unigram, before, after):
        punc_dq = unigram
        self.add_interpretation(before + [Punctuation("'")] + after)

    def unigram_name(self, unigram, before, after):
        pn = unigram
        concept = get_object_or_None(Concept, name=pn.name)
        if concept:
            if concept not in self.learned.get('concepts', []):
                self.add_item(concept)
                self.add_interpretation(before + [concept] + after)

    def unigram_an(self, unigram, before, after):
        sw_an = unigram
        sw_a = Stopword("A")
        self.add_interpretation(before + [sw_a] + after)

    def unigram_prep(self, unigram, before, after):
        sw = unigram
        prep = get_object_or_None(Preposition, name=sw.name)
        if prep:
            self.add_interpretation(before + [prep] + after)

    def unigram_anaphora(self, unigram, before, after):
        sw_ref = unigram
        item = self.recall(sw_ref)
        if item:
            self.add_interpretation(before + [item] + after)


    def unigram_quantifier(self, sw, before, after):
        quantifier = get_object_or_None(Quantifier, name=sw.name)
        if quantifier:
            self.add_interpretation(before + [quantifier] + after)


    def unigram_my(self, unigram, before, after):
        my = unigram
        punc = Punctuation("'")
        s = Stopword('S')
        self.add_interpretation(before + [self.user, punc, s] + after)


    def unigram_you(self, unigram, before, after):
        category, created = Category.objects.get_or_create(
            parent__name="COMPUTER PROGRAM",
            child__name="AI")
        self.add_interpretation(before + [category] + after)


    def bigram_sw(self, bigram, before, after):
        sw1, sw2 = bigram
        sws = get_object_or_None(StopwordSequence, string=' '.join([sw1.name, sw2.name]))
        if sws:
            self.add_interpretation(before + [sws] + after, recurse=False)


    def bigram_exclude(self, bigram, before, after):
        self.add_interpretation(before + after)


    def bigram_the(self, bigram, before, after):
        sw, concept = bigram
        bigram = list(bigram)
        concept_as_the = get_object_or_None(Concept, name='THE ' + concept.name)
        if concept_as_the:
            if concept_as_the not in self.restrict:
                self.restrict.add(concept_as_the)
                self.add_interpretation(before + [concept_as_the] + after)


    def bigram_adj_c(self, bigram, before, after):
        c1, c2 = bigram
        adj = self.word_mgr.concept_to_adj(c1)
        if adj:
            self.add_interpretation(before + [adj, c2] + after)


    def bigram_q_concept(self, bigram, before, after):
        q, c1 = bigram
        amount, created = Amount.objects.get_or_create(
            quantifier=q,
            concept=c1)
        self.add_interpretation(before + [amount] + after)


    def bigram_type_of(self, bigram, before, after):
        c1, sw = bigram
        self.add_interpretation(before + after)


    def bigram_a(self, bigram, before, after):
        sw, concept = bigram
        bigram = list(bigram)
        concept_as_a = get_object_or_None(Concept, name='a '.upper() + concept.name)
        if concept_as_a:
            self.add_interpretation(before + [concept_as_a] + after)
        self.add_interpretation(before + [concept] + after)


    def bigram_a_verb(self, bigram, before, after):
        sw, verb = bigram
        concept_or_none = get_object_or_None(Concept, name=verb.name)
        if concept_or_none:
            self.add_interpretation(before + [sw, concept_or_none] + after)


    def bigram_are_an(self, bigram, before, after):
        concept, sws = bigram
        bigram = list(bigram)
        lemmatizer = WordNetLemmatizer()
        singular_concept_name = lemmatizer.lemmatize(concept.name.lower())
        singular_concept = get_object_or_None(Concept, name=singular_concept_name)
        sw = get_object_or_None(StopwordSequence, string="is a".upper())
        if singular_concept:
            self.add_interpretation(before + [singular_concept, sw] + after)

        
    def bigram_recall(self, bigram, before, after):
        sw, concept = tuple(bigram)
        item = self.recall(concept.name)
        if item:
            self.add_interpretation(before + [item] + after)


    def bigram_are_a(self, bigram, before, after):
        sw_are, sw_a = bigram
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [is_a] + after)        

    def bigram_amount_or_time(self, bigram, before, after):
        number, concept = tuple(bigram)

        amount, created = Amount.objects.get_or_create(
            number=number.number,
            concept=concept)
        self.add_interpretation(before + [amount] + after)

        if self.time_mgr.recognize_time(concept):
            time = Time("%s %s" % (int(number.number), concept.name))
            self.add_interpretation(before + [time] + after)

        if isinstance(number.number, int) and number.number < 1000:
            concept = self.word_mgr.get_singular_concept(concept)
            _list = List([concept for i in xrange(int(number.number))])
            self.add_interpretation(before + [_list] + after)

    def bigram_verb_prep(self, bigram, before, after):
        verb, sw = bigram
        prep = get_object_or_None(Preposition, name=sw.name)
        if prep:
            self.add_interpretation(before + [verb, prep] + after)

    def bigram_your(self, bigram, before, after):
        sw, c1 = bigram
        _property, created = Property.objects.get_or_create(
            parent=self.ai,
            key_concept=c1)
        self.add_interpretation(before + [_property] + after)

    def bigram_anaphoric_ref(self, bigram, before, after):
        sw, concept = bigram
        if sw.name in self.ref_words:
            recalled_item = self.recall(concept)
            if recalled_item:
                self.add_interpretation(before + [recalled_item] + after)

    def bigram_year(self, bigram, before, after):
        _in, number = bigram
        if number.number.is_integer():
            year = Time(int(number.number))
            self.add_interpretation(before + [_in, year] + after)

    def bigram_small_date(self, bigram, before, after):
        c1_month, num1 = bigram
        if self.time_mgr.is_month(c1_month):
            if self.time_mgr.is_day(num1):
                time = Time("%s %s" % (c1_month.name, int(num1.number)), _type="DATE")
                self.add_interpretation(before + [time] + after)
            elif self.time_mgr.is_year(num1):
                time = Time("%s %s" % (c1_month.name, int(num1.number)), _type="DATE")
                self.add_interpretation(before + [time] + after)                


    def bigram_date_year(self, bigram, before, after):
        time, num1 = bigram
        if time.type == "DATE" and not time.year:
            time.add_year(int(num1.number))
            self.add_interpretation(before + [time] + after)


    def trigram_verb_construct(self, trigram, before, after):
        c1, v1, c2 = trigram
        #verb_construct, created = VerbConstruct.objects.get_or_create(
        #    concept1=c1,
        #    verb=v1,
        #    concept2=c2)
        vc = VerbConstruct(
            concept1=c1,
            verb=v1,
            concept2=c2)
        vc2 = self.struct_mgr.new_vc(vc)
        self.add_interpretation(before + [vc2] + after)


    def trigram_isa_number_c(self, trigram, before, after):
        sws_isa, num1, c1 = trigram
        c1.time = Time(int(num1.number))
        self.add_interpretation(before + [sws_isa, c1] + after)


    def trigram_and_to_list(self, trigram, before, after):
        c1, sw, c2 = trigram
        new_list = List([c1, c2])
        self.add_interpretation(before + [new_list] + after)

    def trigram_punc_list(self, trigram, before, after):
        c1, punc, c2 = trigram
        _list = List([c1,c2])
        self.add_interpretation(before + [_list] + after)

    def trigram_concat_list(self, trigram, before, after):
        _list, punc, c2 = trigram
        new_list = List(_list.items + [c2])
        self.add_interpretation(before + [new_list] + after)

    def trigram_and_list(self, trigram, before, after):
        _list, sw, c2 = trigram
        new_list = List(_list.items + [c2])
        self.add_interpretation(before + [new_list] + after)

    def trigram_to_the(self, trigram, before, after):
        verb, sws, concept = trigram
        trigram = list(trigram)
        self.add_interpretation(before + [verb, concept] + after)

    def trigram_is_an(self, trigram, before, after):
        concept1, sws, concept2 = trigram
        trigram = list(trigram)
        new_sws = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [concept1, new_sws, concept2] + after)

    def trigram_comma(self, trigram, before, after):
        item1, punc, item2 = trigram
        self.add_interpretation(before + [item1])
        self.add_interpretation([item2] + after)

    def trigram_float(self, trigram, before, after):
        num1, punc_period, num2 = trigram
        decimal_number = num2.number/float(10**len(num2.name))
        new_number = Number(num1.number + decimal_number)
        self.add_interpretation(before + [new_number] + after)

    def trigram_exp(self, trigram, before, after):
        num1, punc_exp, num2 = trigram
        if num2.number > 100:
            return
        exp_number = num1.number**num2.number
        new_number = Number(exp_number)
        self.add_interpretation(before + [new_number] + after)

    def trigram_multiply(self, trigram, before, after):
        num1, c_x, num2 = trigram
        new_number = Number(num1.number * num2.number)
        self.add_interpretation(before + [new_number] + after)

    def trigram_are_list(self, trigram, before, after):
        concept, sw, _list = trigram
        self.add_interpretation(before + [_list, sw, concept] + after)

    def trigram_are(self, trigram, before, after):
        concept1, sw, concept2 = trigram
        sw_is = Stopword('IS')
        concept1 = self.word_mgr.get_singular_concept(concept1)
        self.add_interpretation(before + [concept1, sw_is, concept2] + after)

    def trigram_such_as(self, trigram, before, after):
        concept1, sws, concept2 = trigram
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        concept1 = self.word_mgr.get_singular_concept(concept1)
        self.add_interpretation(before + [concept2, is_a, concept1] + after)

    def trigram_such_as(self, trigram, before, after):
        concept1, am_a, concept2 = trigram
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [concept1, is_a, concept2] + after)

    def trigram_will_be(self, trigram, before, after):
        concept1, will_be, concept2 = trigram
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation)
            #concept2=concept2)
        self.struct_mgr.add_av(ass=assertion, concept=concept2)
        self.add_interpretation(before + [assertion] + after)

    def trigram_time(self, trigram, before, after):
        sws, time, concept = trigram
        concept.time = time.name
        self.add_interpretation(before + [sws, concept] + after)

    def trigram_v_and_v(self, trigram, before, after):
        v1, sw_and, v2 = trigram
        self.add_interpretation(before + [v1] + after)
        self.add_interpretation(before + [v2] + after)

    def trigram_adj_and_adj(self, trigram, before, after):
        adj1, sw_or, adj2 = trigram
        self.add_interpretation(before + [adj1] + after)
        self.add_interpretation(before + [adj2] + after)

    def trigram_year_range(self, trigram, before, after):
        num1, punc, num2 = trigram
        if num1.number <= 10000 and num1.number <= 10000:
            if num1.number.is_integer() and num1.number.is_integer():
                time = Time("%d-%d" % (num1.number, num2.number), _type="RANGE")
                self.add_interpretation(before + [time] + after)

    def trigram_alt_date(self, trigram, before, after):
        num1, concept_month, num2 = trigram
        if self.time_mgr.is_day(num1):
            if self.time_mgr.is_month(concept_month):
                if self.time_mgr.is_year(num1):
                    time = Time("%s %s %s" % (concept_month.name, int(num1.number), int(num2.number)), _type="DATE")
                    self.add_interpretation(before + [time] + after)
            
    def _4gram_file(self, _4gram, before, after):
        file_concept, file_name_concept, punc, csv = tuple(_4gram)
        new_concept, created = Concept.objects.get_or_create(
            name=file_name_concept.name + punc.name + csv.name)
        new_category, created = Category.objects.get_or_create(
            parent=file_concept,
            child=new_concept)
        self.add_interpretation(before + [new_concept] + after)

    def _4gram_adj(self, _4gram, before, after):
        concept1, sws, adj, concept2 = tuple(_4gram)
        self.add_interpretation(before + [concept1, sws, concept2] + after)

    def _4gram_amount(self, _4gram, before, after):
        number, unit_concept, sw, concept = tuple(_4gram)
        amount, created = Amount.objects.get_or_create(
            number=number.number,
            unit=unit_concept,
            concept=concept)
        self.add_interpretation(before + [amount] + after)

    def _4gram_is_the(self, _4gram, before, after):
        concept1, sws, concept2, concept3 = _4gram
        sws = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [concept1, sws, concept3] + after)

    def _4gram_is_the_of(self, _4gram, before, after):
        concept1, sws, concept2, sw = _4gram
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation([concept1, is_a, concept2])

    def _4gram_was_the_number(self, _4gram, before, after):
        concept1, sws, number, concept2 = _4gram
        is_a = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [concept1, is_a, concept2] + after)

    def _4gram_and(self, _4gram, before, after):
        sws, c1, _and, c2 = _4gram
        self.add_interpretation(before + [sws, c1] + after)
        self.add_interpretation(before + [sws, c2] + after)

    def _4gram_verb_and(self, _4gram, before, after):
        verb, c2, _and, c3 = _4gram
        self.add_interpretation(before + [verb, c2] + after)
        self.add_interpretation(before + [verb, c3] + after)

    def _4gram_date(self, _4gram, before, after):
        prep_on, c1_month, number_day, number_year = _4gram
        if c1_month.name in self.time_mgr.month_names:
            if number_day.number <= 31:
                date = Time("%s %s %s" % (c1_month.name, int(number_day.number), int(number_year.number)), _type="DATE")
                self.add_item(date)
                self.add_interpretation(before + [prep_on, date] + after)

    def _4gram_quoted_item(self, _4gram, before, after):
        punc1, x1, x2, punc2 = _4gram
        qi = QuotedItem([x1,x2])
        self.add_item(qi)
        self.add_interpretation(before + [qi] + after)

    def _4gram_x_to_c(self, _4gram, before, after):
        x, punc, sw_s, c2 = _4gram
        if isinstance(x, Concept):
            return
        c1 = None
        try:
            c1 = get_object_or_None(Concept, name=x.name)
        except:
            pass
        if c1:
            self.add_interpretation(before + [c1, punc, sw_s, c2] + after)
            self.correct(c1)

    def _5gram_small_list_3(self, _5gram, before, after):
        concept1, punc, concept2, sw, concept3 = _5gram
        _list = List([concept1, concept2, concept3])
        self.add_interpretation(before + [_list] + after)
        self.print_once(before + [_list] + after)

    def _5gram_cvcvc(self, _5gram, before, after):
        c1, v1, c2, v2, c3 = _5gram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c2,
            verb=v2,
            concept2=c3)
        self.add_interpretation(before + [c1, v1, verb_construct] + after)

    def _5gram_and(self, _5gram, before, after):
        c1, verb, c2, _and, c3 = _5gram
        self.add_interpretation(before + [c1, verb, c2] + after)
        self.add_interpretation(before + [c1, verb, c3] + after)
        
    def _5gram_by(self, _5gram, before, after):
        c1, sw1, verb, sw2, c2 = _5gram
        self.add_interpretation(before + [c2, verb, c1] + after)

    def _5gram_date(self, _5gram, before, after):
        prep_on, c1_month, number_day, punc, number_year = _5gram
        if c1_month.name in self.time_mgr.month_names:
            if number_day.number <= 31:
                date = Time("%s %s %s" % (c1_month.name, int(number_day.number), int(number_year.number)), _type="DATE")
                self.add_item(date)
                self.add_interpretation(before + [prep_on, date] + after)

    def _5gram_long_slash_date(self, _5gram, before, after):
        n1, punc_slash1, n2, punc_slash2, n3 = _5gram
        if self.time_mgr.is_month(n1) and self.time_mgr.is_day(n2) and self.time_mgr.is_year(n3):
            time = Time("%s/%s/%s" % (n1.number, n2.number, n3.number), _type="DATE")
            self.add_item(time)
            self.add_interpretation(before + [time] + after)

    def _5gram_break_complex_verb(self, _5gram, before, after):
        verb, prep1, c1, prep2, c2 = _5gram
        self.add_interpretation(before + [verb, prep1, c1] + after)
        self.add_interpretation(before + [verb, prep2, c2] + after)

    def _6gram_c_v_c_to(self, _6gram, before, after):
        c1, sw1, v1, sw2, c2, sw_to = _6gram
        self.add_interpretation(before + [c2, v1, c1, sw_to] + after)

    # def _6gram_verb_prep(_6gram, before, after):
    #     c1, sw1, v1, sw2, v2, c2 = _6gram
    #     sub_verb_construct, created = VerbConstruct.objects.get_or_create(
    #         verb=v2,
    #         )

    def _7gram_what(self,_7gram, before, after):
        c1, sws, c2, v1, sw, v2, c3 = _7gram
        self.add_interpretation(before + [c2, v1, c1, sw, v2, c3] + after)

    def ngram_if(self, parsed_sentence):
        statement1 = []
        statement2 = []
        then_index = None
        for i, item in enumerate(parsed_sentence):
            if isinstance(item, Stopword):
                if item.name == "then".upper():
                    then_index = i
                    break
                if item.name == "if".upper():
                    continue
            statement1 += [item]
        for item in parsed_sentence[then_index+1:]:
            statement2 += [item]

        item1 = item2 = None
        item1_results = self.thought_processor.process_thought(statement1)
        if item1_results:
            item1 = item1_results[0]
        item2_results = self.thought_processor.process_thought(statement2)
        if item2_results:
            item2 = item2_results[0]
        if item1 and item2:
            self.add_interpretation([parsed_sentence[0], item1, parsed_sentence[then_index],  item2]) 
        else:
            print 'Could not understance if statement:'
            print '\t %s' % item1_results
            print '\t %s' % item2_results

    def ngram_past_verb(self, parsed_sentence):
        past_verb_name = parsed_sentence[0]
        verb_as_concept = parsed_sentence[-1]
        verb = get_object_or_None(Verb, name=verb_as_concept.name)
        if verb:
            verb.past_name = past_verb_name
            verb.save()
            print 'Past tense of verb %s is %s' % (verb.name, verb.past_name)

    def ngram_everything(self, parsed_sentence):
        everything, sws, concept = tuple(parsed_sentence[:3])
        assertions = Assertion.objects.filter(
            relation__name="IsA",
            concept2=concept).all()
        things = [a.concept1 for a in assertions]
        list_of_everything = List(things, concept)
        self.add_interpretation([list_of_everything] + parsed_sentence[3:])        

    #def the(
        #concept_wo_the = get_object_or_None(Concept, name=' '.join(first_concept.name.split(' ')[1:]))
        #if concept_wo_the:
        #    self.interpret(before + [concept_wo_the] + after)

    # def process_if(self, parsed_sentence, causation=None):
    #     if causation:
    #         self.causation = causation
    #     statement1 = []
    #     statement2 = []
    #     then_index = None
    #     for i, item in enumerate(parsed_sentence[1:]):
    #         if isinstance(item, Stopword):
    #             if item.name.upper() == "then".upper():
    #                 then_index = i
    #                 break
    #         statement1 += [item]
    #     for item in parsed_sentence[then_index+2:]:
    #         statement2 += [item]
    #     assertion = self.interpret(statement1)
    #     verb_construct = self.interpret(statement2)

    #     if_stmt, created = IfStmt.objects.get_or_create(
    #         assertion1=assertion,
    #         vc2=verb_construct)

    #     print if_stmt
    #     return if_stmt


    def is_a(self, triple, before, after):
        concept = triple[0]
        concept_category = triple[2]

        if concept == concept_category:
            return
            
        concept.category = concept_category
        concept.save()

        assertion, created = Assertion.objects.get_or_create(
            concept1=concept,
            relation=Relation.objects.get(name="IsA"))
            #concept2=concept_category)

        self.struct_mgr.add_av(ass=assertion, concept=concept_category)

        self.interpret(before + [concept] + after, last_transform="is_a")
        print '%s is a %s' % (concept, concept_category)
        return assertion

    def of(self, triple, before, after):
        concept = triple[2]
        concept_category = triple[0]
        concept.category = concept_category
        concept.save()
        self.interpret(before + [concept] + after)
        print '%s is a %s' % (concept, concept_category)

    def on_the(self, triple, before, after):
        concept1 = triple[0]
        concept2 = triple[2]
        if self.group_mgr.check_and_form_group(concept2, concept1):
            print '%s is in %s' % (concept1, concept2)

    def is_the(self, triple, before, after):
        concept = triple[0]
        concept_category = triple[2]
        is_a = StopwordSequence.objects.get(string="is a".upper())
        if concept_category.pos == "JJS":
            self.interpret(before + [concept, is_a] + after, last_transform="is_the (JJS)")
            return
        self.interpret(before + [concept, is_a, concept_category] + after, last_transform="is_the")

    def has(self, triple, before, after):
        concept1 = triple[0]
        concept2 = triple[2]
        if self.group_mgr.form_group(concept1, concept2):
            print '%s consist of %s' % (concept1, concept2)

    def attach_pos_tags(self, latest):
        start = 0
        for item in latest:
            if isinstance(item, Concept):
                i = 0
                for word, pos_tag in tags[start:]:
                    if item.name == word.upper():
                        #print item, (word, pos_tag)
                        item.pos = pos_tag
                        start = i
                    i += 1


    def correct(self, new):
        if not new:
            raise Exception('No new item specified in correction')

        print "--> Correction: %s" % [new]
        self.interpretations = [x for x in self.interpretations if new in x]

    def add_interpretation(self, interpretation, recurse=True):
        if len(self.interpretations) > 5000:
            self.print_once("> 5000 interpretations")
            return
        else:
            if interpretation not in self.interpretations:
                self.interpretations += [interpretation]
        if recurse:
            self.interpret(interpretation)

    def add_item(self, item):
        key_name = item.__class__.__name__.lower() + 's'
        self.learned[key_name] = self.learned.get(key_name, [])
        if item not in self.learned.get(key_name, []):
            self.learned[key_name] += [item]

    def remember(self, val, key=None):
        self.thinker.remember(val, key=key)

    def recall(self, item):
        return self.thinker.recall(item)

    def return_interpretations(self):
        tmp = self.interpretations[:]
        self.interpretations = []
        return tmp

    def clear_interpretations(self):
        self.interpretations = []
        self.learned = {}

    def print_once(self, string):
        self.one_item = string
        
    def track_topic(self, parsed_sentence):
        # Store Topic
        if self.topic == None:
            for item in parsed_sentence:
                if isinstance(item, Concept):
                    self.topic = item
                    break
