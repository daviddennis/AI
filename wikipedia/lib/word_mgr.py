from nltk.stem.wordnet import WordNetLemmatizer
from wikipedia.lib.parser import Parser
from annoying.functions import get_object_or_None
from wikipedia.models import *
from nltk.corpus import stopwords
from nltk.corpus import wordnet

class WordManager():
    
    def __init__(self):
        self.parser = Parser()
        self.stop_words = set([x.upper() for x in stopwords.words('english') if x not in ('have', 'had')])

        self.has_prop = get_object_or_None(Relation, name="HasProperty")

    def get_root_word(self, item):
        item_name = None
        if isinstance(item, Concept):
            item_name = item.name
        elif isinstance(item, str):
            item_name = item.name

        return item_name

    def is_plural(self, item):

        if isinstance(item, Concept):
            plural_concept = get_object_or_None(Concept, plural_name=item.name)
            if plural_concept:
                return plural_concept
        elif isinstance(item, str):
            plural_concept = get_object_or_None(Concept, plural_name=item)
            if plural_concept:
                return plural_concept
        
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
                        
    def _is(self, item1, item2):
        c1 = item1
        c2 = None
        adj2 = None
        if isinstance(item1, str):
            c1 = get_object_or_None(Concept, name=item1)
        if isinstance(item2, str):
            c2 = get_object_or_None(Concept, name=item2)
            adj2 = get_object_or_None(Adjective, name=item2)
        if not c1 or not (c2 or adj2):
            return False
        if c2:
            assertions = Assertion.objects.filter(
                concept1=c1,
                relation=self.has_prop,
                concept2=c2).all()
            if assertions:
                return True
        if adj2:
            assertions = Assertion.objects.filter(
                concept1=c1,
                relation=self.has_prop,
                adj2=adj2).all()
            if assertions:
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

    def get_verb_syns(self, verb, size=None):
        verb_syns = list(set([lemma.name for lemma in sum([ss.lemmas for ss in wordnet.synsets(verb.name, wordnet.VERB)],[])] ))
        verbs = []
        for verb_syn in verb_syns:
            if size:
                if len(verbs) >= size:
                    break
            if '_' in verb_syn:
                continue
            verb_or_none = get_object_or_None(Verb, name=verb_syn)
            if verb_or_none:
                verbs += [verb_or_none]
                continue
            verb_or_none = get_object_or_None(Verb, past_name=verb_syn)
            if verb_or_none:
                verbs += [verb_or_none]
                continue
            verb_or_none = get_object_or_None(Verb, participle_name=verb_syn)
            if verb_or_none:
                verbs += [verb_or_none]
                continue

        return verbs

    def is_model(self, item):
        if hasattr(item, '__class__'):
            if hasattr(item.__class__, '__class__'):
                if item.__class__.__class__.__name__ == 'ModelBase':
                    return True
        return False

    def equals(self, item1, item2):
        if item1.__class__ == item2.__class__:
            try:
                same = item1.name == item2.name
                return same
            except:
                pass
        return False
