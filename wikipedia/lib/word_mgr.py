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

    def is_plural(self, concept):
        import en
        plural_concept = get_object_or_None(Concept, name=en.noun.plural(concept.name.lower()))
        if concept == plural_concept:
            return plural_concept
        else:
            return False
            

    def get_singular_concept(self, concept):
        import en
        singular_concept = None
        #lemmatizer = WordNetLemmatizer()
        if ' ' in concept.name:
            tokens = concept.name.split(' ')
            #singular_last_token = lemmatizer.lemmatize(tokens[-1].lower())
            singular_last_token = en.noun.singular(tokens[-1].lower())
            singular_concept_name = ' '.join(tokens[:-1] + [singular_last_token])
        else:
            #singular_concept_name = lemmatizer.lemmatize(concept.name.lower()).upper()
            singular_concept_name = en.noun.singular(concept.name.lower()).upper()

        singular_concept = get_object_or_None(Concept, name=singular_concept_name)

        if singular_concept:
            return singular_concept
        else:
            return concept

    def get_plural_concept(self, concept):
        plural_concept = None
        import en
        try:
            plural_concept = get_object_or_None(Concept, name=en.noun.plural(concept.name.lower()))
        except:
            pass
        
        if plural_concept:
            return plural_concept
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
            

    def concept_to_adj(self, concept):
        adj = get_object_or_None(Adjective, name=concept.name)
        if not adj:
            adj = get_object_or_None(Adjective, superlative=concept.name)
        return adj

    def adj_to_concept(self, adj):
        concept = get_object_or_None(Concept, name=adj.name)
        if not concept:
            concept = get_object_or_None(Concept, name=adj.superlative)
        return concept

    def get_shared_parent(self, items):
        is_all_concepts = True
        for item in items:
            if not isinstance(item, Concept):
                is_all_concepts = False
        if is_all_concepts:
            parent_set = set([x.parent for x in Category.objects.filter(child=items[0]).all()])
            for item in items[1:]:
                parent_set = set([x.parent for x in Category.objects.filter(child=item).all()]) & parent_set
            return list(parent_set)

    def is_a(self, child, parent):
        if isinstance(child, Concept):
            if isinstance(parent, Concept):
                try:
                    category = Category.objects.get(
                        parent=parent,
                        child=child)
                    if category:
                        return True
                except:
                    for category in child.category_set.all():
                        next_parent = category.parent
                        if self.is_a(next_parent, parent):
                            return True

        return False
                        

    def get_participle_verb(self, item):
        import en
        return self.get_verb(item, verb_func=en.verb.participle)

    def get_present_verb(self, item):
        import en
        return self.get_verb(item, verb_func=en.verb.present)        

    def get_past_verb(self, item):
        import en
        return self.get_verb(item, verb_func=en.verb.past)

    # TODO: FIX!!!
    def get_verb(self, item, verb_func=str):
        if isinstance(item, str):
            return get_object_or_None(Verb, past_name=verb_func(item.lower()))
        if isinstance(item, Concept):
            return get_object_or_None(Verb, past_name=verb_func(item.name.lower()))
        try:
            return get_object_or_None(Verb, past_name=verb_func(item.name.lower()))
        except:
            return get_object_or_None(Verb, past_name=verb_func(item.string.lower()))
