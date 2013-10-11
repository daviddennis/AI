from nltk.stem.wordnet import WordNetLemmatizer
from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.word_mgr import WordManager
from wikipedia.models import *
import operator
import sys
from annoying.functions import get_object_or_None
from django.db import transaction

class ThoughtProcessor():
    
    def __init__(self):
        self.pr = PatternRecognizer()
        self.word_mgr = WordManager()
        self.learned = {}
            # 'assertions': [],
            # 'categories': [],
            # 'concepts': [],
            # 'verbs': [],
            # 'verb constructs': [],
            # 'if statements': [],
            # 'groups': [],
            # 'group instances': [],
            # 'aliases': []
            # }
        self.interpretations = []

    def process_thought(self, parsed_sentence, thinker=None):
        self.thinker = thinker
        output = []

        self.process_unigrams(parsed_sentence)
        self.process_bigrams(parsed_sentence)
        output = self.process_trigrams(parsed_sentence)
        self.process_4grams(parsed_sentence)
        self.process_5grams(parsed_sentence)
        self.process_6grams(parsed_sentence)

        if self.pr.recognize(parsed_sentence, "CONCEPT SW:is VERB:use SW:to CONCEPT"):
            self.process_used_to(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT VERB:contain SW:a CONCEPT:list SW:of CONCEPT"):
            self.process_file(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:is_the ADJ CONCEPT SWS:in_the CONCEPT"):
            self.process_range(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:is_the ADJ CONCEPT SW:in CONCEPT"):
            self.process_range(parsed_sentence)
        if self.pr.recognize(parsed_sentence, 'VERB:add CONCEPT:concept PUNC:" ... ...'):
            self.process_add_quoted_concept(parsed_sentence)
        if self.pr.recognize(parsed_sentence, 'VERB:add CONCEPT:concept PUNC:" ... ... ...'):
            self.process_add_quoted_concept(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT VERB CONCEPT ADJECTIVE CONCEPT"):
            self.process_cvca(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:was_the NUMBER CONCEPT SW:of CONCEPT"):
            self.process_rank(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:was_the NUMBER CONCEPT SWS:of_the CONCEPT"):
            self.process_rank(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:is_a CONCEPT SWS:on_the CONCEPT SW:of CONCEPT"):
            self.process_c_is_a_c_on_the_c_of_c(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT VERB SW:and VERB CONCEPT"):
            self.process_c_v_and_v_c(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT:alias CONCEPT SW:as CONCEPT"):
            self.process_alias(parsed_sentence)
        #if self.pr.recognize(parsed_sentence, "CONCEPT SWS:is_the NUMBER CONCEPT SWS CONCEPT"):
        #    self.process_group_distance(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:is_a CONCEPT SW:in CONCEPT"):
            self.process_group(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT VERB CONCEPT SW:to VERB CONCEPT"):
            self.process_to(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SW VERB PREPOSITION VERB"):
            self.process_prep(parsed_sentence)

        return output

    def process_unigrams(self, parsed_sentence):
        for i, item in enumerate(parsed_sentence):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+1:]
            if self.pr.recognize([item], "AMOUNT"):
                self.process_amount(item, before, after)
            if self.pr.recognize([item], "LIST"):
                self.process_unigram_list(item, before, after)
            if self.pr.recognize([item], "CATEGORY"):
                self.process_unigram_category(item, before, after)

    def process_bigrams(self, parsed_sentence):
        bigrams = [(x,y) for x,y in zip(parsed_sentence, parsed_sentence[1:])]
        for i, bigram in enumerate(bigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+2:]
            if self.pr.recognize(bigram, "NAME NAME"):
                self.process_bigram_names(bigram, before, after)
            if self.pr.recognize(bigram, "NUMBER CONCEPT"):
                self.process_bigram_amount(bigram, before, after)
            if self.pr.recognize(bigram, "SW VERBCONSTRUCT"):
                self.process_bigram_question_fragment(bigram, before, after)
            if self.pr.recognize(bigram, "VERB PREP"):
                self.process_bigram_complex_verb(bigram, before, after)
            if self.pr.recognize(bigram, "AMOUNT CONCEPT"):
                self.process_bigram_amount_unit(bigram, before, after)
            if self.pr.recognize(bigram, "ADJECTIVE CONCEPT"):
                self.process_bigram_adj_c(bigram, before, after)

    def process_trigrams(self, parsed_sentence):
        output = []

        item_groups = [(x,y,z) for x,y,z in zip(parsed_sentence, parsed_sentence[1:], parsed_sentence[2:])]
        for i, item_group in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            # if self.pr.recognize(item_group, "CONCEPT VERB:cause CONCEPT"):
            #     result = self.process_cause(item_group, before, after)
            #     output += [result]
            if self.pr.recognize(item_group, "CONCEPT VERB:have CONCEPT"):
                result = self.process_verb_have(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT VERB CONCEPT"):
                result = self.process_verb(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "VERB PREP PREP"):
                result = self.process_complex_verb_pp(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT VERB AMOUNT"):
                result = self.process_verb_amount(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT SW:is CONCEPT"):
                result = self.process_is(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT SW:has CONCEPT"):
                result = self.process_has(item_group, before, after)
                output += [result]
            if self.pr.recognize(item_group, "CONCEPT SWS:is_not_a CONCEPT"):
                self.process_trigram_c_isnota_c(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SWS:is_a ASSERTION"):
                self.process_trigram_c_isa_ass(item_group, before, after)
            if self.pr.recognize(item_group, "VERB SW:the CONCEPT"):
                self.process_trigram_v_the_c(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SW:to VERB"):
                self.process_trigram_c_to_v(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT PREP:of CONCEPT"):
                self.process_trigram_property_of(item_group, before, after)
            if self.pr.recognize(item_group, "NUMBER CONCEPT CONCEPT"):
                self.process_trigram_number_cc(item_group, before, after)
            if self.pr.recognize(item_group, "CONCEPT SWS:of_the CONCEPT"):
                self.process_of_the(item_group, before, after)
            if self.pr.recognize(item_group, 'VERB:switch CONCEPT:context CONCEPT'):
                self.process_switch_context(parsed_sentence)
            if self.pr.recognize(item_group, "CONCEPT SW:on CONCEPT"):
                result = self.process_on(item_group, before, after)
                output += [result]
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
            if self.pr.recognize(item_group, "CONCEPT SW:am CONCEPT"):
                result = self.process_am(item_group, before, after)
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
            if self.pr.recognize(item_group, "VERB:take CONCEPT CONCEPT:away"):
                result = self.process_subtract_concept(item_group, before, after)
                output += [result]                
            if self.pr.recognize(item_group, "CONCEPT VERB VERBCONSTRUCT"):
                result = self.process_c_v_vc(item_group, before, after)
                output += [result]     
            if self.pr.recognize(item_group, "CONCEPT SW:of CONCEPT"):
                result = self.process_group_check(item_group, before, after)
                output += [result]     

        return output

    def process_4grams(self, parsed_sentence):
        item_groups = [(w,x,y,z) for w,x,y,z in zip(parsed_sentence, 
                                                    parsed_sentence[1:], 
                                                    parsed_sentence[2:],
                                                    parsed_sentence[3:])]
        for i, _4gram in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+4:]
            if self.pr.recognize(_4gram, "NUMBER CONCEPT SWS:of_the CONCEPT"):
                self.process_group_size(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT VERB PREP LIST"):
                self.process_complex_verb_list(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT VERB PREP CONCEPT"):
                self.process_basic_prep(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT PUNC:' SW:s CONCEPT"):
                self.process_4gram_property(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT VERB:had SW:a CONCEPT"):
                self.process_4gram_property_had(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT VERB:had SW:an CONCEPT"):
                self.process_4gram_property_had(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT SW:or CONCEPT SWS:is_a"):
                self.process_4gram_alias(_4gram, before, after)


        if self.pr.recognize(parsed_sentence, "SW:if ASSERTION SW:then VERBCONSTRUCT"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "SW:if VERBCONSTRUCT SW:then ASSERTION"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "SW:if ASSERTION SW:then ASSERTION"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "SW:if VERBCONSTRUCT SW:then VERBCONSTRUCT"):
            self.process_if(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT PUNC:' SW:s CONCEPT"):
            self.process_apostrophe(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "VERB CONCEPT SW:into CONCEPT"):
            self.process_into(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT VERB:have NUMBER CONCEPT"):
            self.process_group_size_2(parsed_sentence)
        if self.pr.recognize(parsed_sentence, "CONCEPT SWS:is_a ADJECTIVE CONCEPT"):
            self.process_category_adj(parsed_sentence)


    def process_5grams(self, parsed_sentence):
        item_groups = [(v,w,x,y,z) for v,w,x,y,z in zip(parsed_sentence,
                                                        parsed_sentence[1:],
                                                        parsed_sentence[2:],
                                                        parsed_sentence[3:],
                                                        parsed_sentence[4:])]
        for i, _5gram in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+5:]
            if self.pr.recognize(_5gram, "CONCEPT SW:is VERB SW:as CONCEPT"):
                self.process_is_verb_as(_5gram, before, after)


    def process_6grams(self, parsed_sentence):
        item_groups = [(u,v,w,x,y,z) for u,v,w,x,y,z in zip(parsed_sentence, 
                                                            parsed_sentence[1:], 
                                                            parsed_sentence[2:],
                                                            parsed_sentence[3:],
                                                            parsed_sentence[4:],
                                                            parsed_sentence[5:])]
        for i, _6gram in enumerate(item_groups):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+6:]
            if self.pr.recognize(_6gram, "CONCEPT VERB PREP LIST PREP LIST"):
                self.process_prep_lists(_6gram, before, after)
            if self.pr.recognize(_6gram, "CONCEPT SWS NUMBER CONCEPT SWS:from_the CONCEPT"):
                self.process_from_the(_6gram, before, after)
            

    def process_c_is_a_c_on_the_c_of_c(self, parsed_sentence):
        c1, sws1, c2, sws2, c3, sw, c4 = parsed_sentence
        category, created = Category.objects.get_or_create(
            parent=c2,
            child=c1)
        self.add_category(category)
        category, created = Category.objects.get_or_create(
            parent=c3,
            child=c4)
        self.add_category(category)
        group, created = Group.objects.get_or_create(
            parent_concept=c3,
            child_concept=c2)
        self.add_group(group)
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=c4,
            child_concept=c1)
        self.add_group_instance(group_instance)

    def process_c_v_and_v_c(self, parsed_sentence):
        c1, verb1, sw, verb2, c2 = parsed_sentence
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=verb1,
            concept2=c2)
        self.add_verb_construct(verb_construct)
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=verb2,
            concept2=c2)
        self.add_verb_construct(verb_construct)
    
    def process_alias(self, parsed_sentence):
        alias, c1, sw, c2 = parsed_sentence
        alias, created = Alias.objects.get_or_create(
            concept1=c1,
            concept2=c2)
        self.add_alias(alias)
        
    def process_group_distance(self, parsed_sentence):
        c1, sws, number, c2, sws, c3 = parsed_sentence
        categories = c1.category_set.filter(parent=c2).all()
        if categories:
            groups = Group.objects.filter(
                child_concept=c2).all()
            print groups
            #if groups:
            #    group_instance, created = GroupInstance.objects.get_or_create(
            #        group=group,
            #        )

    def process_group(self, parsed_sentence):
        c1, sws, c2, sws, c3 = parsed_sentence
        categories = Category.objects.filter(
            child=c3).all()
        for category in categories:
            groups = Group.objects.filter(
                parent_concept=category.parent,
                child_concept=c2).all()
            for group in groups:
                group_instance, created = GroupInstance.objects.get_or_create(
                    group=group,
                    parent_concept=c3,
                    child_concept=c1)
                self.add_group_instance(group_instance)

    def process_to(self, parsed_sentence):
        c1, verb1, c2, to, verb2, c3 = parsed_sentence[:6]
        verb_construct1, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=verb1,
            concept2=c2)
        verb_construct2, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=verb2,
            concept2=c3)
        self.add_verb_construct(verb_construct1)
        self.add_verb_construct(verb_construct2)
        #self.process_if([Stopword('IF'), verb_construct1, Stopword('THEN'), verb_construct2])

    def process_prep(self, parsed_sentence):
        c1, sw, v1, prep, v2 = parsed_sentence[:5]
        complex_verb, created = ComplexVerb.objects.get_or_create(
            verb=v1,
            preposition=prep)
        v2_as_concept = self.word_mgr.verb_to_concept(v2)
        if v2_as_concept:
            verb_construct, created = VerbConstruct.objects.get_or_create(
                concept1=c1,
                complex_verb=complex_verb,
                concept2=v2_as_concept)
            self.add_verb_construct(verb_construct)
            
    def process_amount(self, amount, before, after):
        self.remember(amount)

    def process_unigram_list(self, _list, before, after):
        self.remember(_list)

    def process_unigram_category(self, category, before, after):
        c1 = category.child
        self.reinterpret(before + [c1] + after)

    def process_bigram_names(self, bigram, before, after):
        n1, n2 = bigram
        print n1.rank, n2.rank
        if not n1.rank or not n2.rank:
            return
        entity, created = Entity.objects.get_or_create(
            first_name=n1.name,
            last_name=n2.name)
        self.add_item(entity)
        self.reinterpret(before + [entity] + after)

    def process_bigram_amount(self, bigram, before, after):
        number, concept = bigram
        amount, created = Amount.objects.get_or_create(
            number=number.number,
            concept=concept)
        self.add_amount(amount)

    def process_bigram_amount_unit(self, bigram, before, after):
        amount, c1 = bigram
        if not amount.unit:
            if self.word_mgr.get_singular_concept(amount.concept).name in "DOZEN HUNDRED THOUSAND MILLION BILLION TRILLION".split(' '):
                new_amount, created = Amount.objects.get_or_create(
                    number=amount.number,
                    unit=amount.concept,
                    concept=c1)
                self.reinterpret(before + [new_amount] + after)

    def process_bigram_adj_c(self, bigram, before, after):
        adj, c1 = bigram
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=c1,
            relation=relation,
            adj2=adj)
        self.add_item(assertion)
        self.reinterpret(before + [assertion] + after)

    def process_bigram_question_fragment(self, bigram, before, after):
        sw, verb_construct = bigram
        if sw.name in "WHO WHAT WHEN WHERE WHY HOW WHICH CAN".split(' '):
            question_fragment, created = QuestionFragment.objects.get_or_create(
                q_word=sw.name,
                verb_construct=verb_construct)
            self.add_item(question_fragment)

    def process_bigram_complex_verb(self, bigram, before, after):
        verb, prep = bigram
        complex_verb, created = ComplexVerb.objects.get_or_create(
            verb=verb,
            preposition=prep,
            prep2=None)
        self.add_item(complex_verb)
        self.reinterpret(before + [complex_verb] + after)

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
        self.add_if_stmt(if_stmt)

    def process_used_to(self, parsed_sentence):
        concept1, sw, verb, sw, concept2 = tuple(parsed_sentence)
        if verb.name == "USE":
            relation = get_object_or_None(Relation, name="UsedFor")
            assertion, created = Assertion.objects.get_or_create(
                concept1=concept1,
                relation=relation,
                concept2=concept2)
            self.add_assertion(assertion)

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

    def process_range(self, parsed_sentence):
        concept1, sws1, adj, concept2, sws2, concept3 = tuple(parsed_sentence[:6])
        category, created = Category.objects.get_or_create(parent=concept2,
                                                           child=concept1)
        self.add_category(category)
        group, created = Group.objects.get_or_create(
            parent_concept=concept3,
            child_concept=concept2)        
        self.add_group(group)
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=concept3,
            child_concept=concept1)
        self.add_group_instance(group_instance)
        if adj.form == 'superlative':
            rank, created = Rank.objects.get_or_create(
                group_instance=group_instance,
                concept=self.word_mgr.adj_to_concept(adj),
                rank=1)
            self.add_item(rank)

    def process_is_verb_as(self, _5gram, before, after):
        concept1, sw1, verb, sw2, concept2 = _5gram
        #relation = get_object_or_None(Relation, name="IsA")
        #assertion, created = Assertion.objects.get_or_create(
        #    concept1=concept1,
        #    relation=relation,
        #    concept2=concept2)
        #self.add_assertion(assertion)
        category, created = Category.objects.get_or_create(
            parent=concept2,
            child=concept1)
        self.add_category(category)
        self.reinterpret(before + [category] + after)

    def process_4gram_alias(self, _4gram, before, after):
        c1, sw_or, c2, sws_isa = _4gram
        alias, created = Alias.objects.get_or_create(
            concept1=c1,
            concept2=c2)
        self.add_item(alias)
        self.reinterpret(before + [c1, sws_isa] + after)
        self.reinterpret(before + [c2, sws_isa] + after)

    def process_apostrophe(self, parsed_sentence):
        concept1, punc, sw, concept2 = tuple(parsed_sentence[:4])
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation,
            concept2=concept2)
        self.add_assertion(assertion)

    def process_add_quoted_concept(self, parsed_sentence):
        items = tuple(parsed_sentence[3:])
        print items
        item_strings = []
        for item in items:
            item_strings += [self.word_mgr.get_string(item)]
        concept, created = Concept.objects.get_or_create(
            name=' '.join(item_strings))
        self.add_concept(concept)

    def process_switch_context(self, parsed_sentence):
        context_concept = parsed_sentence[2]
        if self.thinker:
            new_context, created = Context.objects.get_or_create(concept=context_concept)
            self.thinker.context = new_context
            print 'Switched context to %s' % self.thinker.context

    def process_into(self, parsed_sentence):
        verb, concept1, sw, concept2 = tuple(parsed_sentence)
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=concept1,
            verb=verb,
            concept2=concept2)
        self.add_verb_construct(verb_construct)

    def process_cvca(self, parsed_sentence):
        c1, verb, c2, adj, x = tuple(parsed_sentence)
        relation = get_object_or_None(Relation, name='HasProperty')
        assertion, created = Assertion.objects.get_or_create(
           concept1=c2,
           relation=relation,
           adj2=adj)
        self.add_assertion(assertion)
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=verb,
            assertion2=assertion)
        self.add_verb_construct(verb_construct)

    def process_group_size(self, _4gram, before, after):
        number, c1, sws, c2 = _4gram
        group, created = Group.objects.get_or_create(
            parent_concept=self.word_mgr.get_singular_concept(c2),
            child_concept=self.word_mgr.get_singular_concept(c1),
            size=number.number)
        self.add_group(group)
        self.reinterpret(before + [group] + after)
        self.remember(group, key=c2.name)

    def process_group_size_2(self, parsed_sentence):
        c1, verb, number, c2 = parsed_sentence
        group, created = Group.objects.get_or_create(
            parent_concept=self.word_mgr.get_singular_concept(c1),
            child_concept=self.word_mgr.get_singular_concept(c2),
            size=number.number)
        self.add_group(group)
        self.remember(group, key=c2.name)

    def process_complex_verb_list(self, _4gram, before, after):
        c1, verb, prep, _list = _4gram
        complex_verb, created = ComplexVerb.objects.get_or_create(
            verb=verb,
            preposition=prep)
        self.add_item(complex_verb)
        for c2 in _list.items:
            if isinstance(c2, Concept):
                verb_construct, created = VerbConstruct.objects.get_or_create(
                    concept1=c1,
                    complex_verb=complex_verb,
                    concept2=c2)
                self.add_verb_construct(verb_construct)

    def process_basic_prep(self, _4gram, before, after):
        c1, verb, prep, c2 = _4gram
        complex_verb, created = ComplexVerb.objects.get_or_create(
            verb=verb,
            preposition=prep,
            prep2=None)
        self.add_item(complex_verb)
        self.reinterpret(before + [c1, complex_verb, c2] + after)
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            complex_verb=complex_verb,
            concept2=c2)
        self.add_verb_construct(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def process_4gram_property(self, _4gram, before, after):
        c1, punc, s, c2 = _4gram
        _property, created = Property.objects.get_or_create(
            parent=c1,
            key_concept=c2)
        self.add_item(_property)
        self.reinterpret(before + [_property] + after)
        self.reinterpret(before + [c2] + after)

    def process_4gram_property_had(self, _4gram, before, after):
        c1, verb, sw, c2 = _4gram
        _property, created = Property.objects.get_or_create(
            parent=c1,
            key_concept=c2)
        self.add_item(_property)
        self.reinterpret(before + [_property] + after)

    def process_category_adj(self, parsed_sentence):
        c1, sws, adj, c2 = parsed_sentence
        category, created = Category.objects.get_or_create(
            parent=c2,
            child=c1)
        self.add_category(category)

    def process_from_the(self, _6gram, before, after):
        c1, sws1, number, c2, sws2, c3 = _6gram
        potential_groups = Group.objects.filter(child_concept=c3).all()
        overarching_concept = None
        for potential_group in potential_groups:
            overarching_concept = potential_group.parent_concept
            potential_relevant_groups = Group.objects.filter(parent_concept=overarching_concept,
                                                         child_concept=c2)
            for potential_relevant_group in potential_relevant_groups:
                categories = Category.objects.filter(parent=potential_relevant_group.child_concept,
                                                     child=c1).all()
                if categories:
                    group_instance, created = GroupInstance.objects.get_or_create(
                        group=potential_relevant_group,
                        parent_concept=overarching_concept,
                        child_concept=c1)
                    self.add_group_instance(group_instance)
                    rank, created = Rank.objects.get_or_create(
                        rank=int(number.number),
                        concept=c3,
                        group_instance=group_instance,
                        sws=sws2)
                    self.add_item(rank)
                    return
                    #self.reinterpret(before + [number, group] + after)

    def process_prep_lists(self, _6gram, before, after):
        c1, verb, prep1, _list1, prep2, _list2 = _6gram
        complex_verb1, created = ComplexVerb.objects.get_or_create(
            verb=verb,
            preposition=prep1)
        self.add_item(complex_verb1)
        complex_verb2, created = ComplexVerb.objects.get_or_create(
            verb=verb,
            preposition=prep2)
        self.add_item(complex_verb2)
        for c2 in _list1.items:
            verb_construct, created = VerbConstruct.objects.get_or_create(
                concept1=c1,
                complex_verb=complex_verb1,
                concept2=c2)
            self.add_verb_construct(verb_construct)        
        for c2 in _list2.items:
            verb_construct, created = VerbConstruct.objects.get_or_create(
                concept1=c1,
                complex_verb=complex_verb2,
                concept2=c2)
            self.add_verb_construct(verb_construct)        
            

    def process_rank(self, parsed_sentence):
        c1, sws, number, c2, sw_s, c3 = parsed_sentence
        group, created = Group.objects.get_or_create(
            parent_concept=c3,
            child_concept=c2)
        self.add_group(group)
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=c3,
            child_concept=c1)#,
            #rank=number.number)
        self.add_group_instance(group_instance)
        rank, created = Rank.objects.get_or_create(
            group_instance=group_instance,
            rank=number.number)
        self.add_item(rank)

    def process_show_mind(self, item_group, before, after):
        print self.thinker.computer_mind
        
    def process_remove_concept(self, item_group, before, after):
        remove_concept, c, concept = tuple(item_group)
        concept.delete()
        print 'Removed %s' % concept

    def process_subtract_concept(self, item_group, before, after):
        verb, concept, away_concept = item_group
        item = self.recall(concept)
        if item:
            print 'Recalled %s' % item
            if isinstance(item, List):
                new_list = None
                for i, list_item in enumerate(item.items):
                    if list_item.name == concept.name:
                        new_list = List(item.items[:i] + item.items[i+1:])
                        self.remember(new_list)
                        break
            #print 'Removing %s from %s' % (concept, item)

    def process_c_v_vc(self, item_group, before, after):
        concept, verb, verb_construct = item_group
        meta_verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=concept,
            verb=verb,
            verb_construct2=verb_construct)
        self.add_verb_construct(meta_verb_construct)

    def process_group_check(self, trigram, before, after):
        c1, sw_of, c2 = trigram
        groups = Group.objects.filter(
            parent_concept=c2,
            child_concept=c1).all()
        if groups:
            group = groups[0]
            self.add_group(group)
            self.reinterpret(before + [group] + after)

    def process_list_in(self, parsed_sentence, before, after):
        _list, sws, concept = tuple(parsed_sentence)
        new_group, created = Group.objects.get_or_create(
           parent_concept=concept,
           child_concept=_list.type)
        self.add_group(new_group)
        print new_group
        for item in _list.items:
            try:
                new_group_instance, created = GroupInstance.objects.get_or_create(
                    group=new_group,
                    parent_concept=concept,
                    child_concept=item)
                print new_group_instance
                self.add_group_instance(group_instance)
            except:
                print 'Warning %s did not add' % item

    def process_list_are(self, parsed_sentence, before, after):
        _list, sw, concept = tuple(parsed_sentence)
        concept = self.word_mgr.get_singular_concept(concept)
        for item in _list.items:
            category, created = Category.objects.get_or_create(
                parent=concept,
                child=item)
            self.add_category(category)

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

    def process_has(self, triple, before, after):
        concept1, stopword, concept2 = triple
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation,
            concept2=concept2)
        self.add_assertion(assertion)        

    def process_is(self, triple, before, after):
        concept1, stopword, concept2 = triple
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
           concept1=concept1,
           relation=relation,
           concept2=concept2,
           context=self.get_context())
        self.add_assertion(assertion)
        self.reinterpret(before + [assertion] + after)
        return assertion
        #self.causation.consider_implications(assertion)
        #return assertion

    def process_on(self, triple, before, after):
        concept1, sw, concept2 = triple
        group, created = Group.objects.get_or_create(
            parent_concept=concept2,
            child_concept=self.word_mgr.get_singular_concept(concept1))
        self.add_group(group)

    def process_of_the(self, trigram, before, after):
        concept1, sws, concept2 = trigram
        group, created = Group.objects.get_or_create(
            parent_concept=concept2,
            child_concept=concept1)
        self.add_group(group)
        self.reinterpret(before + [group] + after)

    def process_trigram_number_cc(self, trigram, before, after):
        number, c1, c2 = trigram
        amount, created = Amount.objects.get_or_create(
            number=number.number,
            unit=c1,
            concept=c2)
        self.add_item(amount)
        self.reinterpret(before + [amount] + after)

    def process_trigram_c_to_v(self, item_group, before, after):
        c1, sw_to, v = item_group
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=v,
            concept2=None)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def process_trigram_v_the_c(self, item_group, before, after):
        verb, sw_the, c2 = item_group
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=None,
            verb=verb,
            concept2=c2)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)        

    def process_trigram_c_isa_ass(self, item_group, before, after):
        c1, sws_isa, ass1 = item_group
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=c1,
            relation=relation,
            concept2=None,
            adj2=None)
        if ass1.concept2:
            assertion.concept2 = ass1.concept2
        elif ass1.adj2:
            assertion.adj2 = ass1.adj2
        self.add_item(assertion)
        self.reinterpret(before + [c1, sws_isa, ass1.concept1] + after)

    def process_trigram_c_isnota_c(self, item_group, before, after):
        c1, isnota, c2 = item_group
        relation = get_object_or_None(Relation, name="IsNotA")
        assertion, created = Assertion.objects.get_or_create(
            concept1=c1,
            relation=relation,
            concept2=c2)
        self.add_assertion(assertion)

    def process_trigram_property_of(self, item_group, before, after):
        c1, sw_of, c2 = item_group
        _property, created = Property.objects.get_or_create(
            parent=c2,
            key_concept=c1)
        self.add_item(_property)
        self.reinterpret(before + [_property] + after)
        self.reinterpret(before + [c2] + after)

    def process_is_a(self, triple, before, after):
        concept1, stopword, concept2 = triple
        relation = get_object_or_None(Relation, name="IsA")
        assertion, created = Assertion.objects.get_or_create(
            concept1=concept1,
            relation=relation,
            concept2=concept2)
        self.add_assertion(assertion)
        new_category, created = Category.objects.get_or_create(
            parent=concept2,
            child=concept1)
        self.add_category(new_category)
        self.reinterpret(before + [new_category] + after)
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
        
    def process_am(self, trigram, before, after):
        c1, sw, c2 = trigram
        relation = get_object_or_None(Relation, name="HasProperty")
        assertion, created = Assertion.objects.get_or_create(
            concept1=c1,
            relation=relation,
            concept2=c2)
        self.add_assertion(assertion)
        self.reinterpret(before + [assertion] + after)

    def process_verb(self, triple, before, after):
        concept1, verb, concept2 = triple
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=concept1,
            verb=verb,
            concept2=concept2,
            context=self.get_context())
        self.add_verb_construct(verb_construct)
        return verb_construct

    def process_complex_verb_pp(self, trigram, before, after):
        verb, prep1, prep2 = trigram
        complex_verb, created = ComplexVerb.objects.get_or_create(
            verb=verb,
            preposition=prep1,
            prep2=prep2)
        self.add_item(complex_verb)
        self.reinterpret(before + [complex_verb] + after)

    def process_verb_have(self, triple, before, after):
        c1, verb, c2 = triple
        c1 = self.word_mgr.get_singular_concept(c1)
        c2 = self.word_mgr.get_singular_concept(c2)
        group, created = Group.objects.get_or_create(
            parent_concept=c1,
            child_concept=c2)
        self.add_group(group)

    def process_verb_amount(self, triple, before, after):
        concept1, verb, amount2 = triple
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=concept1,
            verb=verb,
            amount2=amount2,
            context=self.get_context())
        self.add_verb_construct(verb_construct)
        return verb_construct

    def process_cause(self, triple, before, after):
        concept1, verb, concept2 = triple
        if_stmt, created = IfStmt.objects.get_or_create(
            concept1=concept1,
            concept2=concept2)
        self.add_if_stmt(if_stmt)
        return if_stmt

    def add_concept(self, concept):
        self.learned['concepts'] = self.learned.get('concepts', [])
        if concept not in self.learned.get('concepts', []):
            self.learned['concepts'] += [concept]

    def add_assertion(self, assertion):
        self.learned['assertions'] = self.learned.get('assertions', [])
        if assertion not in self.learned.get('assertions', []):
            self.learned['assertions'] += [assertion]

    def add_category(self, category):
        self.learned['categories'] = self.learned.get('categories', [])
        if category not in self.learned.get('categories', []):
            self.learned['categories'] += [category]

    def add_verb_construct(self, verb_construct):
        key_name = 'verb constructs'
        self.learned[key_name] = self.learned.get(key_name, [])
        if verb_construct not in self.learned.get(key_name, []):
            self.learned[key_name] += [verb_construct]        

    def add_verb(self, verb):
        key_name = 'verbs'
        self.learned[key_name] = self.learned.get(key_name, [])
        if verb not in self.learned.get(key_name, []):
            self.learned[key_name] += [verb]

    def add_if_stmt(self, if_stmt):
        key_name = 'if statements'
        self.learned[key_name] = self.learned.get(key_name, [])
        if if_stmt not in self.learned.get(key_name, []):
            self.learned[key_name] += [if_stmt]

    def add_group(self, group):
        key_name = 'groups'
        self.learned[key_name] = self.learned.get(key_name, [])
        if group not in self.learned.get(key_name, []):
            self.learned[key_name] += [group]

    def add_group_instance(self, group_instance):
        key_name = 'group instances'
        self.learned[key_name] = self.learned.get(key_name, [])
        if group_instance not in self.learned.get(key_name, []):
            self.learned[key_name] += [group_instance]

    def add_alias(self, alias):
        key_name = 'aliases'
        self.learned[key_name] = self.learned.get(key_name, [])
        if alias not in self.learned.get(key_name, []):
            self.learned[key_name] += [alias]

    def add_amount(self, amount):
        key_name = 'amounts'
        self.learned[key_name] = self.learned.get(key_name, [])
        if amount not in self.learned.get(key_name, []):
            self.learned[key_name] += [amount]

    def add_item(self, item):
        key_name = item.__class__.__name__.lower() + 's'
        self.learned[key_name] = self.learned.get(key_name, [])
        if item not in self.learned.get(key_name, []):
            self.learned[key_name] += [item]

    def reinterpret(self, interpretation):
        if interpretation not in self.interpretations:
            self.process_thought(interpretation)
            self.interpretations += [interpretation]

    def get_interpretations(self):
        return self.interpretations
    
    def clear_interpretations(self):
        self.interpretations = []

    def remember(self, item, key=None):
        if self.thinker:
            self.thinker.remember(item, key)

    def recall(self, item):
        if self.thinker:
            return self.thinker.recall(item)

    def get_context(self):
        if self.thinker:
            return self.thinker.context
