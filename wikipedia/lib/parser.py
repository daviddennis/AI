from nltk.corpus import stopwords
from annoying.functions import get_object_or_None
from wikipedia.models import Concept, Connection, StopwordSequence, Stopword
import sys

stop_words = set([x.upper() for x in stopwords.words('english')])

class Parser():

    def __init__(self):
        pass

    def parse(self, latest):
        before = []
        remaining = latest
        success = None
        while len(remaining) > 0:
            item = remaining.pop()
            if isinstance(item, str):
                items, success = self.parse_stopword_sequence(item)
                if success:
                    before += [items[0]]
                    remaining = items[1:]                     
                else:
                    items, success = self.parse_concept(item)
                    if success:
                        before += [items[0]]
                        remaining = items[1:]
                    else:
                        subitems = self.tokenize(items[0])
                        before += [subitems[0]]
                        remaining += [' '.join(subitems[1:])]
                        
            if remaining == ['']:
                break
            else:
                latest = before + remaining

        return latest

    def append_word(self, before, subitems):
        last_str = before[-1]
        last_str = ' '.join([last_str, subitems[0]])
        before = before[:-1]
        new_str = ' '.join(subitems[1:])
        return before, [new_str]

    def tokenize(self, string):
        if isinstance(string, str):
            return [x for x in string.split(' ') if x not in ('', ' ')]
        else:
            return []

    def parse_stopword_sequence(self, string):
        tokens = self.tokenize(string)
        potential_stopword_sequence = []
        sws = None
        rest = []
        for i, token in enumerate(tokens):
            if token in stop_words:
                potential_stopword_sequence += [token]
            else:
                break
            if len(potential_stopword_sequence) > 1:
                sws, created = StopwordSequence.objects.get_or_create(string=' '.join(potential_stopword_sequence))
            rest = [' '.join(tokens[i+1:])]
        if sws:
            sws.save()
            return ([sws] + rest, True)
        elif len(potential_stopword_sequence) == 1:
            return ([Stopword(potential_stopword_sequence[0])] + rest, True)
        return ([string], False)

    def parse_concept(self, string):
        tokens = self.tokenize(string)
        concept = None
        potential_concept = ''
        rest = tokens
        for i, token in enumerate(tokens):
            potential_concept += token + ' '
            concept_or_none = get_object_or_None(Concept, name=potential_concept)
            if concept_or_none:
                concept = concept_or_none
                rest = [' '.join(tokens[i+1:])]
        rest = [x for x in rest if x not in ('', ' ')]
        if concept:
            return ([concept] + rest, True)
        else:
            return ([string], False)
    

    def remove_parentheses(self, sentence):
        new_text = ""
        stop=False
        for c in sentence:
            if c == "(":
                stop = True
            if stop:
                if c == ")":
                    stop = False
                continue
            new_text += c
        return new_text



    # def parse(self, latest):
    #     before = []
    #     remaining = after = latest
    #     last_was_concept = False
    #     success = None
    #     while len(remaining) > 0:
    #         item = remaining.pop()
    #         if isinstance(item, str):
    #             if last_was_concept:
    #                 items, success = self.parse_stopword_sequence(item)
    #                 last_was_concept = False
    #             else:
    #                 items, success = self.parse_concept(item)
    #                 #success = True
    #                 # if not success:
    #                 #     subitems = self.tokenize(items[0])
    #                 #     if isinstance(before[-1], str):
    #                 #         if len(subitems) > 0:
    #                 #             before, items = self.append_word(before, subitems)
    #                 #     else:
    #                 #         before += [subitems[0]]
    #                 #         if subitems[1:]:
    #                 #             items = [' '.join(subitems[1:])]
    #                 last_was_concept = True

    #             if success:
    #                 before += [items[0]]
    #                 after = items[1:] + remaining            
    #             else:
    #                 after = items + remaining

    #         remaining = after
    #         latest = before + after
    #     return latest
