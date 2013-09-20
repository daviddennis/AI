from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.group_manager import GroupManager
from wikipedia.models import (Concept, Connection, StopwordSequence, Group, 
                              GroupInstance, Verb, VerbConstruct, Assertion,
                              Relation, IfStmt)
import sys
from annoying.functions import get_object_or_None

group_stopword_seqs = set([x.upper() for x in ["on the", "in the"]])

class Interpreter():

    def __init__(self):
        self.parser = Parser()        
        self.pr = PatternRecognizer()
        self.group_mgr = GroupManager()

    def interpret(self, parsed_sentence, last_transform=None, thinker=None):
        if thinker:
            self.thinker = thinker
        print parsed_sentence
        item_groups = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        thought = None
        for i, item_group in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if isinstance(item_group[0], Concept):
                concept = item_group[0]
                if concept.name.startswith("the".upper()):
                    self.the(item_group[0], before, list(item_group[1:]) + after)
            #if self.pr.recognize(item_group, 'PUNC:" CONCEPT PUNC:"'):
            #    self.quotes(item_group, before, after, thinker)
            if self.pr.recognize(item_group, "VERB:add CONCEPT:concept STRING"):
                self.add_concept(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT VERB"):
                thought = self._verb(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SWS CONCEPT"):
                stopword_sequence = item_group[1]
                if stopword_sequence.string.upper() == "is the".upper():
                    self.is_the(item_group, before, after)
                if stopword_sequence.string.upper() == "is a".upper():
                    thought = self.is_a(item_group, before, after)
                if stopword_sequence.string.upper() in group_stopword_seqs:
                    self.on_the(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SW CONCEPT"):
                stopword = item_group[1]
                if stopword.string.upper() == "is".upper():
                    thought = self._is(item_group, before, after)
                if stopword.string.upper() == "of".upper():
                    self.of(item_group, before, after)
                if stopword.string.upper() == "have".upper():
                    self.has(item_group, before, after)
        return thought

    def process_if(self, parsed_sentence, causation=None):
        if causation:
            self.causation = causation
        statement1 = []
        statement2 = []
        then_index = None
        for i, item in enumerate(parsed_sentence[1:]):
            if isinstance(item, Stopword):
                if item.string.upper() == "then".upper():
                    then_index = i
                    break
            statement1 += [item]
        for item in parsed_sentence[then_index+2:]:
            statement2 += [item]
        assertion = self.interpret(statement1)
        verb_construct = self.interpret(statement2)

        if_stmt, created = IfStmt.objects.get_or_create(
            assertion1=assertion,
            vc2=verb_construct)

        print if_stmt
        return if_stmt

    def _is(self, triple, before, after):
        concept1, stopword, concept2 = triple
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation,
            concept2=concept2)
        if created:
            print 'Created %s' % assertion
        self.causation.consider_implications(assertion)
        return assertion

    def add_concept(self, triple, before, after):
        concept_name = triple[2]
        concept, created = Concept.objects.get_or_create(
            name=concept_name)
        if created:
            print 'Created %s' % concept
        
    def _verb(self, triple, before, after):
        concept1, verb, x = triple
        if isinstance(x, Stopword):
            if isinstance(after[0], Concept):
                concept2 = after[0]
            else:
                return
        else:
            concept2 = x
        verb_construct, created = VerbConstruct.objects.get_or_create(
                    concept1=concept1,
                    verb=verb,
                    concept2=concept2)
        print verb_construct
        return verb_construct

    def is_a(self, triple, before, after):
        concept = triple[0]
        concept_category = triple[2]

        if concept == concept_category:
            return
            
        concept.category = concept_category
        concept.save()

        assertion, created = Assertion.objects.get_or_create(
            concept1=concept,
            relation=Relation.objects.get(name="IsA"),
            concept2=concept_category)

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

    def the(self, first_concept, before, after):
        concept_wo_the = get_object_or_None(Concept, name=' '.join(first_concept.name.split(' ')[1:]))
        if concept_wo_the:
            self.interpret(before + [concept_wo_the] + after)

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
