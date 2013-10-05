from nltk.stem.wordnet import WordNetLemmatizer
from wikipedia.lib.parser import Parser
from annoying.functions import get_object_or_None
from wikipedia.models import *
from nltk.corpus import stopwords

class WordManager():
    

    def __init__(self):
        self.parser = Parser()
        self.stop_words = set([x.upper() for x in stopwords.words('english') if x not in ('have', 'had')])

    def get_root_word(self, item):
        item_name = None
        if isinstance(item, Concept):
            item_name = item.name
        elif isinstance(item, str):
            item_name = item.name

        return item_name

    def get_singular_concept(self, concept):
        singular_concept = None
        lemmatizer = WordNetLemmatizer()
        if ' ' in concept.name:
            tokens = concept.name.split(' ')
            singular_last_token = lemmatizer.lemmatize(tokens[-1].lower())
            singular_concept_name = ' '.join(tokens[:-1] + [singular_last_token])
        else:
            singular_concept_name = lemmatizer.lemmatize(concept.name.lower()).upper()

        singular_concept = get_object_or_None(Concept, name=singular_concept_name)

        if singular_concept:
            return singular_concept
        else:
            return concept

    def get_forms(self, item):
        if isinstance(item, Concept):
            item_name = item.name.lower()
            print 'Loading en...'
            import en
            return [x.upper() for x in [en.noun.singular(item_name), en.noun.plural(item_name)]]

    def get_string(self, item):
        if isinstance(item, Concept):
            return item.name
        elif isinstance(item, str):
            return item
        elif isinstance(item, Verb):
            return item.name

        return item.name
    
    def is_stopword(self, string):
        print self.stop_words
        if string.upper() in self.stop_words:
            return True
        return False

    def verb_to_concept(self, verb):
        concept = None
        if verb.form == 'past':
            return get_object_or_None(Concept, name=verb.past_name)
        elif verb.form == 'participle':
            return get_object_or_None(Concept, name=verb.participle_name)
        elif not verb.form:
            return get_object_or_None(Concept, name=verb.name)
