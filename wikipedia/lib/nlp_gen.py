from wikipedia.models import *
from wikipedia.lib.english_customs import a_form
from annoying.functions import get_object_or_None

class NLPGenerator():
    
    def __init__(self):
        self.word_mgr = None

    def deparse(self, thought_parse):
        tokens = ['I','do','not','understand']

        if thought_parse['type'] == 'definition':
            tokens = self.process_definition(thought_parse)
        if thought_parse['type'] == 'verification':
            tokens = self.process_verification(thought_parse)
        if thought_parse['type'] == 'question':
            tokens = self.process_question(thought_parse)
        
        sentence = self.make_sentence(tokens)
        return sentence


    def process_question(self, thought_parse):
        question_parse = []
        first_token = None
        tokens = []
        
        for item in thought_parse['sentence']:
            if isinstance(item, str):
                tokens += [item]
            if isinstance(item, VerbConstruct):
                vc = item
                question_parse = [vc]
                verb_token = None
                if vc.verb:
                    verb_token = vc.verb.name
                    first_token = "CAN"
                elif vc.complex_verb:
                    verb_token = "%s" % (vc.complex_verb.verb.name)
                    if vc.complex_verb.preposition:
                        verb_token += " %s" % (vc.complex_verb.preposition.name)
                    prep1 = vc.complex_verb.preposition
                    if prep1:
                        if prep1.name == "BY":
                            first_token = "IS"
                        else:
                            first_token = "CAN"
                    else:
                        first_token = "CAN"
                        
                arg1 = vc.arg1
                arg2 = vc.arg2


                # bedroom is a room in a house
                if arg1 and arg2:

                    arg1_name = arg1.name
                    if ' ' in arg1.name:
                        person_concept = get_object_or_None(Concept, name="PERSON")
                        if self.word_mgr.is_a(arg1, person_concept):
                            sub_tokens = self.parser.tokenize(arg1.name)
                            arg1_name = ' '.join([x.capitalize() for x in sub_tokens])

                    tokens += [arg1_name, verb_token, arg2.name]

                

        if first_token:
            tokens = [first_token] + tokens
            question_parse = [Stopword(first_token)] + question_parse + [Punctuation("?")]
        sentence = self.make_sentence(tokens, question=True)

        return question_parse, sentence

    def process_definition(self, thought_parse):
        tokens = []

        for item in thought_parse['sentence']:
            if isinstance(item, str):
                tokens += [item]
            if isinstance(item, Assertion):
                tokens += [a_form(item.concept1.name)]
                if item.relation.name == "IsA":
                    link_words = ['is'] + [a_form(item.concept2.name)]
                tokens += [item.concept1.name] + link_words + [item.concept2.name]
                
        return tokens

    def process_verification(self, thought_parse):
        tokens = []

        for item in thought_parse['sentence']:
            if isinstance(item, str):
                tokens += [item]

        return tokens

    def make_sentence(self, tokens, question=False):
        sentence = ''

        num_tokens = len(tokens)
        for i, token in enumerate(tokens):
            if ' ' in token:
                sentence += token
            elif get_object_or_None(PersonName, name=token.upper()):
                sentence += token.capitalize()
            else:
                if i == 0:
                    sentence += token.capitalize()
                else:
                    sentence += token.lower()
            
            if i < num_tokens-1:
                sentence += ' '
            else:
                if question:
                    sentence += '?'
                else:
                    sentence += '.'
            
        return sentence
