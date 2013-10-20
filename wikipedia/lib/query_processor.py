from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.word_mgr import WordManager
from wikipedia.models import *
import sys
from annoying.functions import get_object_or_None


class QueryProcessor():

    def __init__(self):
        self.pr = PatternRecognizer()
        self.word_mgr = WordManager()
        self.learned = {}
        self.interpretations = []        

    def process_thought(self, parsed_sentence, thinker=None):
        self.thinker = thinker
        output = []

        #self.process_unigrams(parsed_sentence)
        #self.process_bigrams(parsed_sentence)
        self.process_trigrams(parsed_sentence)
        #self.process_4grams(parsed_sentence)
        #self.process_5grams(parsed_sentence)
        #self.process_6grams(parsed_sentence)
        
        return output

    def process_unigrams(self, parsed_sentence):

        return

        for i, unigram in enumerate(parsed_sentence):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+1:]


    def process_trigrams(self, parsed_sentence):
        output = []

        trigrams = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        for i, trigram in enumerate(trigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if self.pr.recognize(trigram, "SWS:what_is_a CONCEPT PUNC:?"):
                self.process_trigram_concept(trigram, before, after)


    def process_4grams(self, parsed_sentence):

        return

        item_groups = [(w,x,y,z) for w,x,y,z in zip(parsed_sentence, 
                                                    parsed_sentence[1:], 
                                                    parsed_sentence[2:],
                                                    parsed_sentence[3:])]
        for i, _4gram in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+4:]


    def process_trigram_concept(self, trigram, before, after):
        sws, c1, punc = trigram
        categories = Category.objects.filter(
            child=c1).all()
        #parents = [ca.parent for ca in categories]
        for ca in categories:
            self.add_item(ca)


    def add_item(self, item):
        key_name = item.__class__.__name__.lower() + 's'
        self.learned[key_name] = self.learned.get(key_name, [])
        if item not in self.learned.get(key_name, []):
            self.learned[key_name] += [item]

