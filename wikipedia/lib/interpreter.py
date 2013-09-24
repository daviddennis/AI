from nltk.stem.wordnet import WordNetLemmatizer
from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.group_manager import GroupManager
from wikipedia.models import (Concept, Connection, StopwordSequence, Group, 
                              GroupInstance, Verb, VerbConstruct, Assertion,
                              Relation, IfStmt, Category, List)
import operator
import sys
from annoying.functions import get_object_or_None

group_stopword_seqs = set([x.upper() for x in ["on the", "in the"]])

class Interpreter():

    def __init__(self):
        self.parser = Parser()        
        self.pr = PatternRecognizer()
        self.group_mgr = GroupManager()
        self.interpretations = []

    def interpret(self, parsed_sentence, last_transform=None, thinker=None):
        if thinker:
            self.thinker = thinker
        print parsed_sentence
        self.add_interpretation(parsed_sentence)

        if self.pr.recognize(parsed_sentence, "SW:if ... ... ... SW:then ... ... ..."):
            self.ngram_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "STRING SW:is CONCEPT:past CONCEPT:verb SW:of CONCEPT"):
            self.ngram_past_verb(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT:everything SWS:that_is_a CONCEPT"):
            self.ngram_everything(parsed_sentence)

        self.interpret_unigrams(parsed_sentence)
        self.interpret_bigrams(parsed_sentence)
        self.interpret_trigrams(parsed_sentence)
        self.interpret_4grams(parsed_sentence)
        # item_groups = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        # for i, item_group in enumerate(item_groups):
        #     before = parsed_sentence[:i]
        #     after = parsed_sentence[i+3:]
        #     print item_group
        #     if self.pr.recognize(item_group, "SW:the CONCEPT"):
        #         self.the(item_group, before, after)
            #if self.pr.recognize(item_group, 'PUNC:" CONCEPT PUNC:"'):
            #    self.quotes(item_group, before, after, thinker)
            # if self.pr.recognize(item_group, "CONCEPT VERB"):
            #     self._verb(item_group, before, after)
            # if self.pr.recognize(item_group, "CONCEPT SWS CONCEPT"):
            #     stopword_sequence = item_group[1]
            #     if stopword_sequence.string.upper() == "is the".upper():
            #         self.is_the(item_group, before, after)
            #     if stopword_sequence.string.upper() == "is a".upper():
            #         self.is_a(item_group, before, after)
            #     if stopword_sequence.string.upper() in group_stopword_seqs:
            #         self.on_the(item_group, before, after)
        return self.return_interpretations()

    def process_thought(self, parsed_sentence):
        output = []

        item_groups = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        for i, item_group in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            # if self.pr.recognize(item_group, "CONCEPT VERB:cause CONCEPT"):
            #     result = self.process_cause(item_group, before, after)
            #     output += [result]
            if self.pr.recognize(item_group, "CONCEPT VERB CONCEPT"):
                result = self.process_verb(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT SW:is CONCEPT"):
                result = self.process_is(item_group, before, after)
                output += [result]
                # if stopword.name.upper() == "of".upper():
                #     self.of(item_group, before, after)
                # if stopword.name.upper() == "have".upper():
                #     self.has(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SWS:is_a CONCEPT"):
                result = self.process_is_a(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT SWS:is_not_a CONCEPT"):
                result = self.process_is_not_a(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT SWS:is_not CONCEPT"):
                result = self.process_is_not(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "VERB:add CONCEPT:concept STRING"):
                result = self.process_add_concept(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "VERB:list SW:all CONCEPT"):
                result = self.process_list_concepts(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "VERB:ask SW:a CONCEPT:question"):
                result = self.process_ask_question(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "LIST SWS:is_in_a CONCEPT"):
                result = self.process_list_in(item_group, before, after)
                output += [result]     
            if self.pr.recognize(item_group, "VERB:show SWS:what_you CONCEPT:know"):
                result = self.process_show_mind(item_group, before, after)
                output += [result]     
            if self.pr.recognize(item_group, "VERB:remove CONCEPT:concept CONCEPT"):
                result = self.process_remove_concept(item_group, before, after)
                output += [result]

        if self.pr.recognize(parsed_sentence, "SW:if ASSERTION SW:then VERBCONSTRUCT"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "SW:if VERBCONSTRUCT SW:then ASSERTION"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "SW:if ASSERTION SW:then ASSERTION"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "SW:if VERBCONSTRUCT SW:then VERBCONSTRUCT"):
            self.process_if(parsed_sentence)

        if self.pr.recognize(parsed_sentence, "CONCEPT SW:is VERB:use SW:to CONCEPT"):
            self.process_used_to(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT VERB:contain SW:a CONCEPT:list SW:of CONCEPT"):
            self.process_file(parsed_sentence)
            
        return output

    def interpret_unigrams(self, parsed_sentence):
        for i, unigram in enumerate(parsed_sentence):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+1:]
            if self.pr.recognize([unigram], "SWS"):
                self.unigram_sws(unigram, before, after)
            if self.pr.recognize([unigram], "SW:are"):
                self.unigram_are(unigram, before, after)
            if self.pr.recognize([unigram], "SWS:on_then"):
                self.unigram_on_then(unigram, before, after)

    def interpret_bigrams(self, parsed_sentence):
        bigrams = [(x,y) for x,y in zip(parsed_sentence, parsed_sentence[1:])]
        for i, bigram in enumerate(bigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+2:]
            if self.pr.recognize(bigram, "SW:the CONCEPT"):
                self.bigram_the(bigram, before, after)
            if self.pr.recognize(bigram, "SW:a CONCEPT"):
                self.bigram_a(bigram, before, after)
            if self.pr.recognize(bigram, "CONCEPT SWS:are_an"):
                self.bigram_are_an(bigram, before, after)
            if self.pr.recognize(bigram, "SW:that CONCEPT"):
                self.bigram_recall(bigram, before, after)

    def interpret_trigrams(self, parsed_sentence):
        trigrams = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        for i, trigram in enumerate(trigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if self.pr.recognize(trigram, "VERB SWS:to_the CONCEPT"):
                self.trigram_to_the(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SWS:is_an CONCEPT"):
                self.trigram_is_an(trigram, before, after)

    def interpret_4grams(self, parsed_sentence):
        _4grams = [(w,x,y,z) for w,x,y,z in zip(parsed_sentence, 
                                                parsed_sentence[1:],
                                                parsed_sentence[2:],
                                                parsed_sentence[3:])]
        for i, _4gram in enumerate(_4grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+4:]
            if self.pr.recognize(_4gram, "CONCEPT SWS:is_the CONCEPT CONCEPT"):
                self._4gram_is_the(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT:file CONCEPT PUNC:. CONCEPT:CSV"):
                self._4gram_file(_4gram, before, after)

    def unigram_sws(self, unigram, before, after):
        sws = unigram
        stopwords = [Stopword(sw) for sw in sws.string.split(' ')]
        self.add_interpretation(before + stopwords + after)

    def unigram_on_then(self, unigram, before, after):
        sws = unigram
        concept_name = sws.string.split(' ')[0]
        concept_or_none = get_object_or_None(Concept, name=concept_name)
        if concept_or_none:
            print concept_or_none
            self.add_interpretation(before + [concept_or_none, Stopword('THEN')] + after)

    def unigram_are(self, unigram, before, after):
        sw = unigram
        self.interpret(before + [Stopword('IS')] + after)

    def bigram_the(self, bigram, before, after):
        sw, concept = bigram
        bigram = list(bigram)
        concept_as_the = get_object_or_None(Concept, name='the '.upper() + concept.name)
        if concept_as_the:
            self.add_interpretation(before + [concept_as_the] + after)

    def bigram_a(self, bigram, before, after):
        sw, concept = bigram
        bigram = list(bigram)
        concept_as_a = get_object_or_None(Concept, name='a '.upper() + concept.name)
        if concept_as_a:
            self.add_interpretation(before + [concept_as_a] + after)

    def bigram_are_an(self, bigram, before, after):
        concept, sws = bigram
        bigram = list(bigram)
        lemmatizer = WordNetLemmatizer()
        singular_concept_name = lemmatizer.lemmatize(concept.name.lower())
        singular_concept = get_object_or_None(Concept, name=singular_concept_name)
        sw = get_object_or_None(StopwordSequence, string="is a".upper())
        if singular_concept:
            self.add_interpretation(before + [singular_concept, sw] + after)
        
    def bigram_recall(self, bigram, before, after):
        sw, concept = tuple(bigram)
        item = self.recall(concept.name)
        if item:
            self.add_interpretation(before + [item] + after)

    def trigram_to_the(self, trigram, before, after):
        verb, sws, concept = trigram
        trigram = list(trigram)
        self.add_interpretation(before + [verb, concept] + after)

    def trigram_is_an(self, trigram, before, after):
        concept1, sws, concept2 = trigram
        trigram = list(trigram)
        new_sws = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [concept1, new_sws, concept2] + after)

    def _4gram_file(self, _4gram, before, after):
        file_concept, file_name_concept, punc, csv = tuple(_4gram)
        new_concept, created = Concept.objects.get_or_create(
            name=file_name_concept.name + punc.name + csv.name)
        new_category, created = Category.objects.get_or_create(
            parent=file_concept,
            child=new_concept)
        self.add_interpretation(before + [new_concept] + after)

    def _4gram_is_the(self, _4gram, before, after):
        concept1, sws, concept2, concept3 = _4gram
        _4gram = list(_4gram)
        sws = get_object_or_None(StopwordSequence, string="is a".upper())
        self.add_interpretation(before + [concept1, sws, concept3] + after)

    def ngram_if(self, parsed_sentence):
        statement1 = []
        statement2 = []
        then_index = None
        for i, item in enumerate(parsed_sentence):
            if isinstance(item, Stopword):
                if item.name == "then".upper():
                    then_index = i
                    break
                if item.name == "if".upper():
                    continue
            statement1 += [item]
        for item in parsed_sentence[then_index+1:]:
            statement2 += [item]

        item1 = item2 = None
        item1_results = self.process_thought(statement1)
        if item1_results:
            item1 = item1_results[0]
        item2_results = self.process_thought(statement2)
        if item2_results:
            item2 = item2_results[0]
        if item1 and item2:
            self.add_interpretation([parsed_sentence[0], item1, parsed_sentence[then_index],  item2]) 
        else:
            print 'Could not understance if statement:'
            print '\t %s' % item1_results
            print '\t %s' % item2_results

    def ngram_past_verb(self, parsed_sentence):
        past_verb_name = parsed_sentence[0]
        verb_as_concept = parsed_sentence[-1]
        verb = get_object_or_None(Verb, name=verb_as_concept.name)
        if verb:
            verb.past_name = past_verb_name
            verb.save()
            print 'Past tense of verb %s is %s' % (verb.name, verb.past_name)

    def ngram_everything(self, parsed_sentence):
        everything, sws, concept = tuple(parsed_sentence[:3])
        assertions = Assertion.objects.filter(
            relation__name="IsA",
            concept2=concept).all()
        things = [a.concept1 for a in assertions]
        list_of_everything = List(things, concept)
        self.add_interpretation([list_of_everything] + parsed_sentence[3:])

    def process_if(self, parsed_sentence):
        _if, item1, then, item2 = tuple(parsed_sentence)
        vc1 = assertion1 = vc2 = assertion2 = None
        if isinstance(item1, Assertion):
            assertion1 = item1
        if isinstance(item1, VerbConstruct):
            vc1 = item1
        if isinstance(item2, Assertion):
            assertion2 = item2
        if isinstance(item2, VerbConstruct):
            vc2 = item2
        if_stmt, created = IfStmt.objects.get_or_create(
            vc1=vc1,
            assertion1=assertion1,
            vc2=vc2,
            assertion2=assertion2)
        print if_stmt
        
    def process_used_to(self, parsed_sentence):
        concept1, sw, verb, sw, concept2 = tuple(parsed_sentence)
        if verb.name == "USE":
            relation = get_object_or_None(Relation, name="UsedFor")
            assertion, created = Assertion.objects.get_or_create(
                concept1=concept1,
                relation=relation,
                concept2=concept2)
            print assertion

    def process_file(self, parsed_sentence):
        file_name_concept, verb, sw, list_concept, sw, category_concept = tuple(parsed_sentence)
        items = []
        try:
            input_file = open(file_name_concept.name, 'r')
        except:
            input_file = open(file_name_concept.name.lower(), 'r')
        for line in input_file:
            new_concept, created = Concept.objects.get_or_create(
                name=line.strip().upper())
            category, created = Category.objects.get_or_create(
                parent=category_concept,
                child=new_concept)
            items += [new_concept]
        _list = List(items, category_concept)
        self.remember('LIST', _list)
        self.remember('LIST OF %s' % category_concept.name, _list)

    def process_show_mind(self, item_group, before, after):
        print self.thinker.computer_mind
        
    def process_remove_concept(self, item_group, before, after):
        remove_concept, c, concept = tuple(item_group)
        concept.delete()
        print 'Removed %s' % concept

    def process_list_in(self, parsed_sentence, before, after):
        _list, sws, concept = tuple(parsed_sentence)
        new_group, created = Group.objects.get_or_create(
           parent_concept=concept,
           child_concept=_list.type)
        print new_group
        for item in _list.items:
            try:
                new_group_instance, created = GroupInstance.objects.get_or_create(
                    group=new_group,
                    parent_concept=concept,
                    child_concept=item)
                print new_group_instance
            except:
                print 'Warning %s did not add' % item

    def process_ask_question(self, parsed_sentence, before, after):
        instances_explored = set()
        categories_explored = set()

        property_assertions = Assertion.objects.filter(
            relation__name="HasProperty").all()[:1000]

        for property_assertion in property_assertions:
            if property_assertion.concept1.name in instances_explored:
                continue
            instances_explored.add(property_assertion.concept1.name)
            if property_assertion.concept2.name in categories_explored:
                continue
            categories_explored.add(property_assertion.concept2.name)

            print ''
            print property_assertion

            property_name = property_assertion.concept2.name
            similar_assertions = Assertion.objects.filter(
                relation__name="HasProperty",
                concept2__name=property_name).all()
            instance_names = set([a.concept1.name for a in similar_assertions])
            if len(instance_names) > 1:
                print 'Some examples of things that are %s are %s' % (property_name, list(instance_names)[:3])
                #print instance_names
                similarities = {}
                for instance_name in instance_names:
                    is_a_assertions = Assertion.objects.filter(
                        concept1__name=instance_name,
                        relation__name="IsA").all()
                    if is_a_assertions:
                        #print 'Some examples that are %s' % (instance_name, [a.concept2.name for a in is_a_assertions][:5])
                        for is_a_assertion in is_a_assertions:
                            category_name = is_a_assertion.concept2.name
                            if category_name != property_name:
                                similarities[category_name] = similarities.get(category_name, 0) + 1
                            
                if similarities:
                    sorted_similarities = sorted(similarities.iteritems(), key=operator.itemgetter(1), reverse=True)
                    #print sorted_similarities
                    highest = sorted_similarities[0]
                    if highest[1] > 1:
                        print 'Many things that HasProperty %s are %s' % (property_name, highest[0])
                        print 'Are all %s %s?' % (property_name, highest[0])

    #def the(
        #concept_wo_the = get_object_or_None(Concept, name=' '.join(first_concept.name.split(' ')[1:]))
        #if concept_wo_the:
        #    self.interpret(before + [concept_wo_the] + after)

    # def process_if(self, parsed_sentence, causation=None):
    #     if causation:
    #         self.causation = causation
    #     statement1 = []
    #     statement2 = []
    #     then_index = None
    #     for i, item in enumerate(parsed_sentence[1:]):
    #         if isinstance(item, Stopword):
    #             if item.name.upper() == "then".upper():
    #                 then_index = i
    #                 break
    #         statement1 += [item]
    #     for item in parsed_sentence[then_index+2:]:
    #         statement2 += [item]
    #     assertion = self.interpret(statement1)
    #     verb_construct = self.interpret(statement2)

    #     if_stmt, created = IfStmt.objects.get_or_create(
    #         assertion1=assertion,
    #         vc2=verb_construct)

    #     print if_stmt
    #     return if_stmt

    def process_is(self, triple, before, after):
        concept1, stopword, concept2 = triple
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation,
            concept2=concept2)
        if created:
           print 'Created %s' % assertion
        return assertion
        #self.causation.consider_implications(assertion)
        #return assertion

    def process_is_a(self, triple, before, after):
        concept1, stopword, concept2 = triple
        relation = get_object_or_None(Relation, name="IsA")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation,
            concept2=concept2)
        if created:
           print 'Created %s' % assertion
        new_category, created = Category.objects.get_or_create(
            parent=concept2,
            child=concept1)
        if created:
            print 'Created %s' % new_category
        return assertion, new_category

    def process_is_not_a(self, triple, before, after):
        concept1, sws, concept2 = triple
        assertions = Assertion.objects.filter(
            concept1=concept1,
            relation__name="IsA",
            concept2=concept2)
        if assertions:
            for assertion in assertions:
                assertion.delete()
            print 'Removed %s' % assertions[0]

    def process_is_not(self, triple, before, after):
        concept1, sws, concept2 = triple
        assertions = Assertion.objects.filter(
            concept1=concept1,
            relation__name="HasProperty",
            concept2=concept2)
        if assertions:
            for assertion in assertions:
                assertion.delete()
            print 'Removed %s' % assertions[0]

    def process_add_concept(self, triple, before, after):
        concept_name = triple[2]
        concept, created = Concept.objects.get_or_create(
            name=concept_name)
        if created:
            print 'Created %s' % concept
        return concept

    def process_list_concepts(self, triple, before, after):
        concept = triple[2]
        assertions = Assertion.objects.filter(
            relation__name="IsA",
            concept2=concept).all()[:100]
        group_concepts = GroupInstance.objects.filter(
            parent_concept=concept).all()[:100]
        all_concepts = list(group_concepts) + [a.concept1 for a in assertions]
        print all_concepts
        return all_concepts
        
    def process_verb(self, triple, before, after):
        concept1, verb, concept2 = triple
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=concept1,
            verb=verb,
            concept2=concept2)
        print verb_construct
        return verb_construct

    def process_cause(self, triple, before, after):
        concept1, verb, concept2 = triple
        if_stmt, created = IfStmt.objects.get_or_create(
            concept1=concept1,
            concept2=concept2)
        print if_stmt
        return if_stmt

    def is_a(self, triple, before, after):
        concept = triple[0]
        concept_category = triple[2]

        if concept == concept_category:
            return
            
        concept.category = concept_category
        concept.save()

        assertion, created = Assertion.objects.get_or_create(
            concept1=concept,
            relation=Relation.objects.get(name="IsA"),
            concept2=concept_category)

        self.interpret(before + [concept] + after, last_transform="is_a")
        print '%s is a %s' % (concept, concept_category)
        return assertion

    def of(self, triple, before, after):
        concept = triple[2]
        concept_category = triple[0]
        concept.category = concept_category
        concept.save()
        self.interpret(before + [concept] + after)
        print '%s is a %s' % (concept, concept_category)

    def on_the(self, triple, before, after):
        concept1 = triple[0]
        concept2 = triple[2]
        if self.group_mgr.check_and_form_group(concept2, concept1):
            print '%s is in %s' % (concept1, concept2)

    def is_the(self, triple, before, after):
        concept = triple[0]
        concept_category = triple[2]
        is_a = StopwordSequence.objects.get(string="is a".upper())
        if concept_category.pos == "JJS":
            self.interpret(before + [concept, is_a] + after, last_transform="is_the (JJS)")
            return
        self.interpret(before + [concept, is_a, concept_category] + after, last_transform="is_the")

    def has(self, triple, before, after):
        concept1 = triple[0]
        concept2 = triple[2]
        if self.group_mgr.form_group(concept1, concept2):
            print '%s consist of %s' % (concept1, concept2)

    def attach_pos_tags(self, latest):
        start = 0
        for item in latest:
            if isinstance(item, Concept):
                i = 0
                for word, pos_tag in tags[start:]:
                    if item.name == word.upper():
                        #print item, (word, pos_tag)
                        item.pos = pos_tag
                        start = i
                    i += 1


    def add_interpretation(self, interpretation):
        if interpretation not in self.interpretations:
            self.interpretations += [interpretation]
            self.interpret(interpretation)

    def remember(self, key, val):
        self.thinker.computer_mind[key] = val

    def recall(self, key):
        return self.thinker.computer_mind.get(key, None)

    def return_interpretations(self):
        tmp = self.interpretations[:]
        self.interpretations = []
        return tmp
