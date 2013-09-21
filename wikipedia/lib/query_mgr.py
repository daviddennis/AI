import sys
from wikipedia.models import StopwordSequence, Concept, Assertion, Stopword, Punctuation, Verb
from nltk.stem.wordnet import WordNetLemmatizer
from annoying.functions import get_object_or_None


class QueryManager():

    w_words = ['WHO', 'WHAT', 'WHEN', 'WHERE', 'WHY', 'HOW', 'CAN', 'DO']

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def is_query(self, latest):
        if len(latest) <= 1:
            return False
        if isinstance(latest[-1], Punctuation):
            if latest[-1].string == "?":
                return True
        item = latest[0]
        if isinstance(item, StopwordSequence):
            for w_word in self.w_words:
                if w_word in item.string:
                    return True
        if isinstance(item, Stopword):
            for w_word in self.w_words:
                if w_word in item.name:
                    return True
        return False

    def construct_query(self, latest):
        query = {
            'type': None,
            'parsed_sentence': latest
            }
        first_item = latest[0]
        if isinstance(first_item, StopwordSequence) or isinstance(first_item, Stopword):

            for w_word in self.w_words:
                if w_word in first_item.string:
                    query['type'] = w_word
        return query

    def process_query(self, query):
        answer = None
        if query['type'] == 'WHAT':
            answer = self.process_what(query)
        if query['type'] in ('CAN', 'DO'):
            answer = self.process_can(query)

        return answer

    def process_can(self, query):
        answer = {
            'type': 'verification',
            'sentence': []
            }
        concept_thing = None
        verb_name = None
        verb_found = False
        for i, item in enumerate(query['parsed_sentence']):
            if isinstance(item, Concept):
                if i == 1:
                    concept_thing = item
                if i == 2:
                    verb_or_none = get_object_or_None(Verb, name=item.name)
                    if verb_or_none:
                        verb_found = True
                        verb_name = verb_or_none.name
                    else:
                        verb_name = item.name
            if isinstance(item, str):
                if i == 2:
                    verb_or_none = get_object_or_None(Verb, name=item)
                    if verb_or_none:
                        verb_found = True
                        verb_name = verb_or_none.name
                    concept_or_none = get_object_or_None(Concept, name=item)
                    if concept_or_none:
                        verb_name = concept_or_none.name

        can_do = False
        if concept_thing.name.lower() in ("things", "something", "a thing", "thing"):
            can_do = verb_found
        else:
            assertions = Assertion.objects.filter(
                concept1__name=concept_thing.name.upper(), 
                relation__name="CapableOf",
                concept2__name=verb_name.upper()).all()
            if assertions:
                can_do = True
                
        if can_do:
            answer['sentence'] = ['yes']
            answer['tf_result'] = True
        else:
            answer['sentence'] = ['i', "do", "not", "know"]
            answer['tf_result'] = None
                        
        return answer

    def process_what(self, query):
        concept_to_define = None
        for item in query['parsed_sentence']:
            if isinstance(item, Concept):
                concept_to_define = item

        assertions = Assertion.objects.filter(
            concept1=concept_to_define, 
            relation__name="IsA").\
            order_by('-score').\
            all()

        answer = {
            'type': 'definition'
            }
        if assertions:
            answer['sentence'] = [assertions[0]]
        else:
            print 'Loading en...'
            import en
            concept_name_singular = en.noun.singular(concept_to_define.name)
            assertions = Assertion.objects.filter(
                concept1__name=concept_name_singular, 
                relation__name="IsA").order_by('-score').all()
                
            if assertions:
                answer['sentence'] = [assertions[0]]        
            else:
                answer['sentence'] = ['i', "do", "not", "know"]
            
        return answer
