from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from annoying.functions import get_object_or_None
from wikipedia.models import *
import string
import sys

stop_words = set([x.upper() for x in stopwords.words('english') if x not in ('have', 'had', 'has')] \
                     + [x.upper() for x in ('mine', 'several', 'also')])

class Parser():

    def __init__(self):
        self.en = None
        self.text_numbers = {
            'ONE': 1,
            'TWO': 2,
            'THREE': 3,
            'FOUR': 4,
            'FIVE': 5,
            'SIX': 6,
            'SEVEN': 7,
            'EIGHT': 8,
            'NINE': 9,
            'TEN': 10,
            
            'FIRST': 1,
            'SECOND': 2,
            'THIRD': 3,
            'FOURTH': 4,
            'FIFTH': 5,
            'SIXTH': 6,
            'SEVENTH': 7,
            'EIGHTH': 8,
            'NINTH': 9,
            'TENTH': 10
            }

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
                            items, success = self.parse_number(item)
                            if success:
                                before += [items[0]]
                                remaining = items[1:]
                            else:
                                #items, success = self.parse_name(item)
                                #if success:
                                #    before += [items[0]]
                                #    remaining = items[1:]
                                #else:
                                items, success = self.parse_concept(item)
                                if success:
                                    before += [items[0]]
                                    remaining = items[1:]
                                else:
                                    items, success = self.parse_adjective(item)
                                    if success:
                                        before += [items[0]]
                                        remaining = items[1:]
                                    else:
                                        subitems = self.tokenize(items[0])
                                        before += [subitems[0]]
                                        remaining += [' '.join(subitems[1:])]
                                        
            if remaining == ['']:
                latest = before
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
        if isinstance(string, str) or isinstance(string, unicode):
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

    def parse_number(self, item):
        tokens = self.tokenize(item)
        number_token = tokens[0]
        if number_token in self.text_numbers:
            return ([Number(self.text_numbers[number_token])] + [' '.join(tokens[1:])], True)
        number_token = number_token.replace('ST','').replace('ND','').replace('RD','').replace('TH','')
        number_set = set([str(x) for x in range(10)])
        is_number = True
        for c in number_token:
            if c not in number_set:
                is_number = False
        if is_number:
            return ([Number(number_token)] + [' '.join(tokens[1:])], True)
        else:
            return ([item], False)

    def parse_name(self, item):
        tokens = self.tokenize(item)
        name = get_object_or_None(PersonName, name=tokens[0])
        if name and name.rank:
            return ([name] + [' '.join(tokens[1:])], True)
        else:
            return ([item], False)

    def parse_adjective(self, item):
        tokens = self.tokenize(item)        
        adjective = get_object_or_None(Adjective, superlative=tokens[0])
        if adjective:
            adjective.form = 'superlative'
        else:
            adjective = get_object_or_None(Adjective, name=tokens[0])
        if adjective:
            return ([adjective] + [' '.join(tokens[1:])], True)
        else:
            return ([item], False)

    def parse_verb(self, item, tags):
        tokens = self.tokenize(item)
        verb = None

        if tags:
            for word, pos_tag in tags:
                if 'V' in pos_tag:
                    if word == tokens[0]:
                        verb_or_none = get_object_or_None(Verb, name=tokens[0])
                        if verb_or_none:
                            verb = verb_or_none
                        else:
                            verb_or_none = get_object_or_None(Verb, past_name=tokens[0])
                            if verb_or_none:
                                verb = verb_or_none
                                verb.form = 'past'
                            else:
                                verb_or_none = get_object_or_None(Verb, participle_name=tokens[0])
                                if verb_or_none:
                                    verb = verb_or_none
                                    verb.form = 'participle'
                                    verb_or_none = get_object_or_None(Verb, participle_name=tokens[0])
                                else:
                                    verb_or_none = get_object_or_None(Verb, s_form=tokens[0])
                                    if verb_or_none:
                                        verb = verb_or_none
                                        verb.form = 's'
        else:
            verb_or_none = get_object_or_None(Verb, past_name=tokens[0])
            if verb_or_none:
                verb = verb_or_none
                verb.form = 'past'

        if verb:
            return ([verb] + [' '.join(tokens[1:])], True)
        else:
            return ([tokens[0]] + [' '.join(tokens[1:])], False)


    def parse_verb_old(self, item, tags):
        tokens = self.tokenize(item)
        verb = None
        verb_or_none = get_object_or_None(Verb, past_name=tokens[0])
        past = False
        participle = False
        if verb_or_none:
            verb = verb_or_none
            verb.form = 'past'
            past = True
        else:
            verb_or_none = get_object_or_None(Verb, participle_name=tokens[0])
            if verb_or_none:
                verb = verb_or_none
                verb.form = 'participle'
                participle = True
            else:
                verb_or_none = get_object_or_None(Verb, name=tokens[0])
                if verb_or_none:
                    verb = verb_or_none
                else:
                    if not tags:
                        return ([tokens[0]] + [' '.join(tokens[1:])], False)
                    #import en
                    for word, pos_tag in tags:
                        if 'V' in pos_tag:
                            if word == tokens[0]:
                                lemmatizer = WordNetLemmatizer()
                                present_verb_name = lemmatizer.lemmatize(word.lower(), 'v')
                                verb_or_none = get_object_or_None(Verb, name=present_verb_name)
                                #en.verb.present(word.lower())
                                if verb_or_none:
                                    verb = verb_or_none
        
        if verb and not past and not participle:
            concept_or_none = get_object_or_None(Concept, name=verb.name)
            if concept_or_none:
                verb = None
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
