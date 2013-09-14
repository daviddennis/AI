import sys
from wikipedia.models import StopwordSequence, Concept, Assertion, Stopword
from nltk.stem.wordnet import WordNetLemmatizer
from annoying.functions import get_object_or_None


class QueryManager():

    w_words = ['WHO', 'WHAT', 'WHEN', 'WHERE', 'WHY', 'HOW', 'CAN']

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def is_query(self, latest):
        for item in latest:
            if isinstance(item, StopwordSequence) or isinstance(item, Stopword):
                for w_word in self.w_words:
                    if w_word in item.string:
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
        if query['type'] == 'CAN':
            answer = self.process_can(query)

        return answer

    def process_can(self, query):
        answer = {
            'type': 'verification',
            'sentence': []
            }
        concept_thing = None
        concept_do = None
        for i, item in enumerate(query['parsed_sentence']):
            if isinstance(item, Concept):
                if i == 1:
                    concept_thing = item
                if i == 2:
                    concept_do = item
            if isinstance(item, str):
                if i == 2:
                    concept_or_none = get_object_or_None(Concept, name=item)
                    if concept_or_none:
                        concept_do = concept_or_none

        #for i in range(5):
        assertions = Assertion.objects.filter(
            concept1__name=concept_thing.name.upper(), 
            relation__name="CapableOf",
            concept2__name=concept_do.name.upper()).all()

        if assertions:
            answer['sentence'] = ['yes']
            answer['tf_result'] = True
        else:
            answer['sentence'] = ['i', "do", "not", "know"]
            answer['tf_result'] = None
            #break
                        
        return answer

    def process_what(self, query):
        concept_to_define = None
        for item in query['parsed_sentence']:
            if isinstance(item, Concept):
                concept_to_define = item

        assertions = Assertion.objects.filter(
            concept1__name=concept_to_define.name, 
            relation__name="IsA").all()

        answer = {
            'type': 'definition'
            }
        if assertions:
            answer['sentence'] = [assertions[0]]
        return answer
