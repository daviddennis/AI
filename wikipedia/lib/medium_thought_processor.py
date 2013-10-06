from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.word_mgr import WordManager
from wikipedia.models import *
import operator
import sys
from annoying.functions import get_object_or_None

class MediumThoughtProcessor():

    def __init__(self):
        self.thinker = None
        self.word_mgr = WordManager()
        self.pr = PatternRecognizer()
        self.learned = {}
        
    def process_thought(self, parsed_sentence, thinker=None):
        if thinker:
            self.thinker = thinker

        self.process_trigrams(parsed_sentence)
        self.process_4grams(parsed_sentence)
        self.process_5grams(parsed_sentence)

    def process_trigrams(self, parsed_sentence):
        trigrams = [(x,y,z) for x,y,z in zip(parsed_sentence,
                                             parsed_sentence[1:],
                                             parsed_sentence[2:])]

        for i, trigram in enumerate(trigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if self.pr.recognize(trigram, "CONCEPT SWS GROUP"):
                self.trigram_group(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY SW:because ASSERTION"):
                self.trigram_ca_ass_group(trigram, before, after)
            if self.pr.recognize(trigram, "AMOUNT CVERB CONCEPT"):
                self.trigram_cverb(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY CVERB CONCEPT"):
                self.trigram_ca_cverb_c(trigram, before, after)

    def process_4grams(self, parsed_sentence):
        _4grams = [(w,x,y,z) for w,x,y,z in zip(parsed_sentence, 
                                                parsed_sentence[1:],
                                                parsed_sentence[2:],
                                                parsed_sentence[3:])]
        for i, _4gram in enumerate(_4grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+4:]
            if self.pr.recognize(_4gram, "CONCEPT SW CVERB CONCEPT"):
               self._4gram_cverb(_4gram, before, after)
            if self.pr.recognize(_4gram, "CATEGORY PREP SW CONCEPT"):
               self._4gram_category_group(_4gram, before, after)
            #if self.pr.recognize(_4gram, "CATEGORY SW:because ASSERTION"):
            #    print _4gram,'!!!!\n\n\n'


    def process_5grams(self, parsed_sentence):
        _5grams = [(v,w,x,y,z) for v,w,x,y,z in zip(parsed_sentence, 
                                                    parsed_sentence[1:],
                                                    parsed_sentence[2:],
                                                    parsed_sentence[3:],
                                                    parsed_sentence[4:])]
        for i, _5gram in enumerate(_5grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+5:]
            if self.pr.recognize(_5gram, "CONCEPT SW NUMBER SWS GROUP"):
                self._5gram_group(_5gram, before, after)


    def trigram_group(self, trigram, before, after):
        c1, sws, group = trigram
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=group.parent_concept,
            child_concept=c1)
        self.add_item(group_instance)        

    def trigram_ca_ass_group(self, trigram, before, after):
        category, sw, assertion = trigram
        if_stmt, created = IfStmt.objects.get_or_create(
            assertion1=assertion,
            category2=category)
        self.add_item(if_stmt)

        # shared_parent1 = self.word_mgr.get_shared_parent([category.parent, category.child])
        # if shared_parent1 and category.child == assertion.concept1:
        #     category, created
        #     if_stmt, created = If_Stmt.objects.get_or_create(
        #         assertion1=assertion,
        #         )

    def trigram_cverb(self, trigram, before, after):
        amount, cverb, concept = trigram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            amount1=amount,
            complex_verb=cverb,
            concept2=concept)
        self.add_item(verb_construct)

    def trigram_ca_cverb_c(self, trigram, before, after):
        category, cverb, concept = trigram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=category.child,
            complex_verb=cverb,
            concept2=concept)
        self.add_item(verb_construct)

    def _4gram_cverb(self, _4gram, before, after):
        c1, sw, cverb, c2 = _4gram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            complex_verb=cverb,
            concept2=c2)
        self.add_item(verb_construct)

    def _4gram_category_group(self, _4gram, before, after):
        category, prep, sw, concept = _4gram
        groups = Group.objects.filter(
            parent_concept=concept,
            child_concept=category.parent).all()
        if groups:
            group = groups[0]
            group_instance, created = GroupInstance.objects.get_or_create(
                group=group,
                parent_concept=concept,
                child_concept=category.child)
            self.add_item(group_instance)
        

    def _5gram_group(self, _5gram, before, after):
        concept, sw, number, sws, group = _5gram
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=group.parent_concept,
            child_concept=concept)
        self.add_item(group_instance)

    def add_item(self, item):
        key_name = item.__class__.__name__.lower() + 's'
        self.learned[key_name] = self.learned.get(key_name, [])
        if item not in self.learned.get(key_name, []):
            self.learned[key_name] += [item]
