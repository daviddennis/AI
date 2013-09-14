from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.group_manager import GroupManager
from wikipedia.models import Concept, Connection, StopwordSequence, Group, GroupInstance
import sys
from annoying.functions import get_object_or_None

group_stopword_seqs = set([x.upper() for x in ["on the", "in the"]])

class Interpreter():

    def __init__(self):
        self.parser = Parser()        
        self.pr = PatternRecognizer()
        self.group_mgr = GroupManager()

    def interpret(self, parsed_sentence, last_transform=None):
        #print parsed_sentence
        item_groups = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        for i, item_group in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if isinstance(item_group[0], Concept):
                concept = item_group[0]
                if concept.name.startswith("the".upper()):
                    self.the(item_group[0], before, list(item_group[1:]) + after)
            if self.pr.recognize(item_group, "CONCEPT SWS CONCEPT"):
                stopword_sequence = item_group[1]
                if stopword_sequence.string.upper() == "is the".upper():
                    self.is_the(item_group, before, after)
                if stopword_sequence.string.upper() == "is a".upper():
                    self.is_a(item_group, before, after)
                if stopword_sequence.string.upper() in group_stopword_seqs:
                    self.on_the(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SW CONCEPT"):
                stopword = item_group[1]
                if stopword.string.upper() == "of".upper():
                    self.of(item_group, before, after)
                if stopword.string.upper() == "have".upper():
                    self.has(item_group, before, after)
        return parsed_sentence

    def is_a(self, triple, before, after):
        concept = triple[0]
        concept_category = triple[2]
        concept.category = concept_category
        concept.save()
        self.interpret(before + [concept] + after, last_transform="is_a")
        print '%s is a %s' % (concept, concept_category)

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
