from nltk.corpus import stopwords
from annoying.functions import get_object_or_None
from wikipedia.models import Concept, Connection, StopwordSequence, Stopword, Punctuation, Verb
import string
import sys

stop_words = set([x.upper() for x in stopwords.words('english')])

class Parser():

    def __init__(self):
        pass

    def parse(self, latest, tags=None):
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
                    items, success = self.parse_punctuation(item)
                    if success:
                        before += [items[0]]
                        remaining = items[1:]
                    else:
                        items, success = self.parse_verb(item, tags)
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
    
    def parse_punctuation(self, item):
        tokens = self.tokenize(item)
        if tokens[0] in string.punctuation:
            return ([Punctuation(tokens[0])] + [' '.join(tokens[1:])], True)
        else:
            return ([item], False)

    def parse_verb(self, item, tags):
        tokens = self.tokenize(item)
        if not tags:
            return ([tokens[0]] + [' '.join(tokens[1:])], False)
        import en
        verb = None
        for word, pos_tag in tags:
            if 'V' in pos_tag:
                if word == tokens[0]:
                    verb_or_none = get_object_or_None(Verb, name=en.verb.present(word.lower()))
                    if verb_or_none:
                        verb = verb_or_none
        if verb:
            return ([verb] + [' '.join(tokens[1:])], True)
        else:
            return ([tokens[0]] + [' '.join(tokens[1:])], False)

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

    def space_punctuation(self, sentence):
        new_sentence = ""
        for i,c in enumerate(sentence):
            if c in string.punctuation:
                if i != 0:
                    new_sentence += " "
                new_sentence += "%s " % c
            else:
                new_sentence += c

        for i in range(10): 
            if '  ' in new_sentence:
                new_sentence = ' '.join(new_sentence.split('  '))
            else:
                break

        return new_sentence
