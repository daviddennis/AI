from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.word_mgr import WordManager
from wikipedia.models import *
import operator
import sys
from annoying.functions import get_object_or_None

class MediumThoughtProcessor():

    def __init__(self):
        self.thinker = None
        self.word_mgr = WordManager()
        self.pr = PatternRecognizer()
        self.interpretations = []
        self.learned = {}
        self.struct_mgr = None
        
    def process_thought(self, parsed_sentence, thinker=None):
        if thinker:
            self.thinker = thinker

        self.process_unigrams(parsed_sentence)
        self.process_bigrams(parsed_sentence)
        self.process_trigrams(parsed_sentence)
        self.process_4grams(parsed_sentence)
        self.process_5grams(parsed_sentence)

    def process_unigrams(self, parsed_sentence):
        for i, unigram in enumerate(parsed_sentence):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+1:]
            if self.pr.recognize([unigram], "PROPERTY"):
                self.unigram_property(unigram, before, after)
            if self.pr.recognize([unigram], "GI"):
                self.unigram_gi(unigram, before, after)
            

    def process_bigrams(self, parsed_sentence):
        bigrams = [(x,y) for x,y in zip(parsed_sentence,
                                         parsed_sentence[1:])]

        for i, bigram in enumerate(bigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+2:]
            if self.pr.recognize(bigram, "PROPERTY AMOUNT"):
                self.bigram_prop_amt(bigram, before, after)
            if self.pr.recognize(bigram, "PROPERTY CONCEPT"):
                self.bigram_prop_c(bigram, before, after)
            if self.pr.recognize(bigram, "CONCEPT VERBCONSTRUCT"):
                self.bigram_c_vc(bigram, before, after)
            if self.pr.recognize(bigram, "CATEGORY QFRAG"):
                self.bigram_ca_qfrag(bigram, before, after)
            if self.pr.recognize(bigram, "VERBCONSTRUCT CONCEPT"):
                self.bigram_vc_c(bigram, before, after)
            if self.pr.recognize(bigram, "PROPERTY VERBCONSTRUCT"):
                self.bigram_prop_vc(bigram, before, after)

    def process_trigrams(self, parsed_sentence):
        trigrams = [(x,y,z) for x,y,z in zip(parsed_sentence,
                                             parsed_sentence[1:],
                                             parsed_sentence[2:])]

        for i, trigram in enumerate(trigrams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+3:]
            if self.pr.recognize(trigram, "CONCEPT SWS GROUP"):
                self.trigram_group(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY SW:because ASSERTION"):
                self.trigram_ca_ass_group(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY SW:in CONCEPT"):
                self.trigram_ca_in_c(trigram, before, after)
            if self.pr.recognize(trigram, "AMOUNT CVERB CONCEPT"):
                self.trigram_cverb(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT CVERB AMOUNT"):
                self.trigram_cverb_ca(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY CVERB CONCEPT"):
                self.trigram_ca_cverb_c(trigram, before, after)
            if self.pr.recognize(trigram, "PROPERTY SW:is CONCEPT"):
                self.trigram_property(trigram, before, after)
            if self.pr.recognize(trigram, "PROPERTY SW:is AMOUNT"):
                self.trigram_property_amount(trigram, before, after)
            if self.pr.recognize(trigram, "PROPERTY SW:is ADJ"):
                self.trigram_property_is_adj(trigram, before, after)
            if self.pr.recognize(trigram, "PROPERTY SW:of AMOUNT"):
                self.trigram_property_amount(trigram, before, after)
            if self.pr.recognize(trigram, "CONCEPT SW:is PROPERTY"):
                self.trigram_c_is_property(trigram, before, after)
            if self.pr.recognize(trigram, "PROPERTY VERB:has AMOUNT"):
                self.trigram_p_v_amount(trigram, before, after)
            if self.pr.recognize(trigram, "PROPERTY PREP PROPERTY"):
                self.trigram_ppp(trigram, before, after)
            if self.pr.recognize(trigram, "CPREP SWS:is_a ASSERTION"):
                self.trigram_cprep_isa_ass(trigram, before, after)
            if self.pr.recognize(trigram, "VERBCONSTRUCT PREP CONCEPT"):
                self.trigram_vc_prep_c(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY SW:that VERBCONSTRUCT"):
                self.trigram_ca_that_vc(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY PREPOSITION:in CONCEPT"):
                self.trigram_ca_prep_c(trigram, before, after)
            if self.pr.recognize(trigram, "VERB SW:the PROPERTY"):
                self.trigram_verb_the_prop(trigram, before, after)
            if self.pr.recognize(trigram, "VERBCONSTRUCT ADJ:like LIST"):
                self.trigram_vc_like_list(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY SWS:which_was VERB|CVERB"):
                self.trigram_ca_was_verb(trigram, before, after)
            if self.pr.recognize(trigram, "CATEGORY SWS:that_was VERB|CVERB"):
                self.trigram_ca_was_verb(trigram, before, after)
        


    def process_4grams(self, parsed_sentence):
        _4grams = [(w,x,y,z) for w,x,y,z in zip(parsed_sentence, 
                                                parsed_sentence[1:],
                                                parsed_sentence[2:],
                                                parsed_sentence[3:])]
        for i, _4gram in enumerate(_4grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+4:]
            if self.pr.recognize(_4gram, "CONCEPT SW CVERB CONCEPT"):
               self._4gram_cverb(_4gram, before, after)
            if self.pr.recognize(_4gram, "CATEGORY PREP SW CONCEPT"):
               self._4gram_category_group(_4gram, before, after)
            if self.pr.recognize(_4gram, "PROPERTY SW:is VERB:name CONCEPT"):
               self._4gram_property(_4gram, before, after)
            if self.pr.recognize(_4gram, "PROPERTY SW:is VERB:call CONCEPT"):
               self._4gram_property(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT SW:was CVERB NUMBER"):
               self._4gram_date(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT CVERB SW:the CONCEPT"):
               self._4gram_cvc(_4gram, before, after)
            if self.pr.recognize(_4gram, "ASSERTION SW:can VERB CONCEPT"):
               self._4gram_can(_4gram, before, after)
            if self.pr.recognize(_4gram, "AMOUNT SW:in SW CONCEPT"):
                self._4gram_amount_group(_4gram, before, after)
            if self.pr.recognize(_4gram, "PROPERTY PUNC:' SW:s CONCEPT"):
                self._4gram_sub_prop(_4gram, before, after)
            if self.pr.recognize(_4gram, "CONCEPT SWS:that_was CVERB TIME"):
                self._4gram_thatwas_cv_time(_4gram, before, after)
            #if self.pr.recognize(_4gram, "CATEGORY SW:because ASSERTION"):
            #    print _4gram,'!!!!\n\n\n'


    def process_5grams(self, parsed_sentence):
        _5grams = [(v,w,x,y,z) for v,w,x,y,z in zip(parsed_sentence, 
                                                    parsed_sentence[1:],
                                                    parsed_sentence[2:],
                                                    parsed_sentence[3:],
                                                    parsed_sentence[4:])]
        for i, _5gram in enumerate(_5grams):
            before = parsed_sentence[:i]
            after = parsed_sentence[i+5:]
            if self.pr.recognize(_5gram, "CONCEPT SW NUMBER SWS GROUP"):
                self._5gram_group(_5gram, before, after)


    def unigram_property(self, _property, before, after):
        if self.word_mgr.is_plural(_property.key_concept):
            group, created = Group.objects.get_or_create(
                parent_concept=_property.parent,
                child_concept=self.word_mgr.get_singular_concept(_property.key_concept))
            self.add_item(group)
            self.reinterpret(before + [group] + after)

    def unigram_gi(self, group_instance, before, after):
        self.reinterpret(before + [group_instance.parent_concept] + after)

    def bigram_prop_amt(self, bigram, before, after):
        prop, amount = bigram
        prop.value_amount = amount
        prop.save()
        self.add_item(prop)

    def bigram_prop_c(self, bigram, before, after):
        prop, c = bigram
        #new_prop = self.struct_mgr.add_pvalue(prop=prop, concept=c)

        sub_prop, created = Property.objects.get_or_create(
            parent=prop.key_concept,
            key_concept=c)

        new_prop, created = Property.objects.get_or_create(
            parent=prop.parent,
            key_concept=prop.key_concept,
            sub_prop=sub_prop)

        self.add_item(new_prop)
        self.reinterpret(before + [new_prop] + after)


    def bigram_c_vc(self, bigram, before, after):
        c1, vc = bigram
        if not vc.arg1:
            vc.concept1 = c1
            vc.save()
            self.add_item(vc)
            self.reinterpret(before + [vc] + after)


    def bigram_ca_qfrag(self, bigram, before, after):
        ca, qf = bigram
        if not qf.verb_construct.arg1:
            vc = self.struct_mgr.copy(VerbConstruct, qf.verb_construct, add={'concept1_id': ca.child_id})
        elif not qf.verb_construct.arg2:
            vc = self.struct_mgr.copy(VerbConstruct, qf.verb_construct, add={'concept2_id': ca.child_id})
        self.add_item(vc)
        self.reinterpret(before + [vc] + after)

        
    def bigram_vc_c(self, bigram, before, after):
        vc, c1 = bigram
        if not vc.arg2:
            vc.concept2 = c1
            vc2 = self.struct_mgr.new_vc(vc)
            self.add_item(vc2)
            self.reinterpret(before + [vc2] + after)

    def bigram_prop_vc(self, bigram, before, after):
        prop, vc = bigram
        if not vc.arg1:
            vc.property1 = prop
            new_vc = self.struct_mgr.new_vc(vc)
            self.add_item(new_vc)
            self.reinterpret(before + [new_vc] + after)

    def trigram_group(self, trigram, before, after):
        c1, sws, group = trigram
        if group.parent_concept:
            if self.word_mgr.is_a(c1, group.parent_concept):
                new_group, created = Group.objects.get_or_create(
                    parent_concept=c1,
                    child_concept=group.child_concept)
                self.add_item(new_group)
                self.reinterpret(before + [new_group] + after)
            elif self.word_mgr.is_a(c1, group.child_concept):
                group_instance, created = GroupInstance.objects.get_or_create(
                    group=group,
                    parent_concept=group.parent_concept,
                    child_concept=c1)
                self.add_item(group_instance)
                self.reinterpret(before + [group_instance] + after)
        else:
            new_group, created = Group.objects.get_or_create(
                parent_concept=c1,
                child_concept=group.child_concept)
            self.add_item(new_group)
            self.reinterpret(before + [new_group] + after)


    def trigram_ca_ass_group(self, trigram, before, after):
        category, sw, assertion = trigram
        if_stmt, created = IfStmt.objects.get_or_create(
            assertion1=assertion,
            category2=category)
        self.add_item(if_stmt)

        # shared_parent1 = self.word_mgr.get_shared_parent([category.parent, category.child])
        # if shared_parent1 and category.child == assertion.concept1:
        #     category, created
        #     if_stmt, created = If_Stmt.objects.get_or_create(
        #         assertion1=assertion,
        #         )

    def trigram_ca_in_c(self, trigram, before, after):
        category, sw_in, c2 = trigram
        c1_type = category.parent
        c1 = category.child
        groups = Group.objects.filter(parent_concept=c2, child_concept=c1_type).all()
        if groups:
            group = groups[0]
            group_instance, created = GroupInstance.objects.get_or_create(
                group=group,
                parent_concept=c2,
                child_concept=c1)
            self.add_item(group_instance)
            self.reinterpret(before + [group_instance] + after)

    def trigram_cverb(self, trigram, before, after):
        amount, cverb, concept = trigram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            amount1=amount,
            complex_verb=cverb,
            concept2=concept)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def trigram_ca_cverb_c(self, trigram, before, after):
        category, cverb, concept = trigram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=category.child,
            complex_verb=cverb,
            concept2=concept)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def trigram_cverb_ca(self, trigram, before, after):
        concept, cverb, amount = trigram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=concept,
            complex_verb=cverb,
            amount2=amount)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def trigram_property(self, trigram, before, after):
        prop, sw, c1 = trigram
        pv, created = PropertyValue.objects.get_or_create(
            concept=c1)
        if not pv.props.filter(pk=prop.id).count():
            pv.props.add(prop)
        #prop.value_concept = c1
        #prop.save()
        self.add_item(prop)

    def trigram_property_amount(self, trigram, before, after):
        prop, sw, amount = trigram
        pv, created = PropertyValue.objects.get_or_create(
            amount=amount)
        if not pv.props.filter(pk=prop.id).count():
            pv.props.add(prop)
        #prop.value_amount = amount
        #prop.save()
        self.add_item(prop)

    def trigram_property_is_adj(self, trigram, before, after):
        prop, sw_is, adj = trigram
        relation = get_object_or_None(Relation, name="HasProperty")
        ass, created = Assertion.objects.get_or_create(
            property1=prop,
            relation=relation)
        self.struct_mgr.add_av(ass=ass, adj=adj)
        self.add_item(ass)
        self.reinterpret(before + [ass] + after)

    def trigram_c_is_property(self, trigram, before, after):
        c1, sw_is, prop = trigram
        pv, created = PropertyValue.objects.get_or_create(
            concept=c1)
        if not pv.props.filter(pk=prop.id).count():
            pv.props.add(prop)
        # prop.value_concept = c1
        # prop.save()
        self.add_item(prop)

    def trigram_p_v_amount(self, trigram, before, after):
        p, verb_has, amount = trigram
        pv, created = PropertyValue.objects.get_or_create(
            amount=amount)
        if not pv.props.filter(pk=p.id).count():
            pv.props.add(p)
        # p.value_amount = amount
        # p.save()
        self.add_item(p)

    def trigram_ppp(self, trigram, before, after):
        prop1, prep, prop2 = trigram
        pc, created = PrepConstruct.objects.get_or_create(
            concept1=prop1.key_concept,
            preposition=prep,
            concept2=prop2.key_concept)
        self.add_item(pc)
        self.reinterpret(before + [pc] + after)

    # TODO: FIX!!!
    def trigram_cprep_isa_ass(self, trigram, before, after):
        cprep, sws_isa, assertion = trigram
        relation = get_object_or_None(Relation, name="HasProperty")
        raise Exception('FIX!!!')
        # if assertion.adj2:
        #     new_assertion, created = Assertion.objects.get_or_create(
        #         concept1=cprep.concept1,
        #         relation=relation,
        #         adj2=assertion.adj2)
        #     self.add_item(new_assertion)
        # if assertion.concept2:
        #     new_assertion, created = Assertion.objects.get_or_create(
        #         concept1=cprep.concept1,
        #         relation=relation,
        #         concept2=assertion.concept2)
        #     self.add_item(new_assertion)

    def trigram_vc_prep_c(self, trigram, before, after):
        vc, prep, concept = trigram
        prep_construct, created = PrepConstruct.objects.get_or_create(
            vc1=vc,
            preposition=prep,
            concept2=concept)
        self.add_item(prep_construct)
        self.reinterpret(before + [prep_construct] + after)

    def trigram_ca_that_vc(self, trigram, before, after):
        ca, sw, vc = trigram
        if not vc.arg1:
            verb_construct, created = VerbConstruct.objects.get_or_create(
                concept1=ca.child,
                verb=vc.verb,
                complex_verb=vc.complex_verb,
                concept2=vc.concept2,
                amount2=vc.amount2,
                assertion2=vc.assertion2,
                question_fragment2=vc.question_fragment2,
                verb_construct2=vc.verb_construct2,
                property2=vc.property2)
            self.add_item(verb_construct)
            self.reinterpret(before + [verb_construct] + after)


    def trigram_ca_prep_c(self, trigram, before, after):
        ca, prep, c1 = trigram
        group, created = Group.objects.get_or_create(
            parent_concept=c1,
            child_concept=ca.parent)
        self.add_item(group)
        self.reinterpret(before + [group] + after)
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=c1,
            child_concept=ca.child)
        self.add_item(group_instance)
        self.reinterpret(before + [group_instance] + after)

    def trigram_verb_the_prop(self, trigram, before, after):
        verb, sw_the, _property = trigram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=None,
            amount1=None,
            verb=verb,
            property2=_property)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)


    def trigram_vc_like_list(self, trigram, before, after):
        vc, adj_like, _list = trigram
        for item in _list.items:
            if isinstance(item, Concept):
                if vc.concept2:
                    
                    ca, created = Category.objects.get_or_create(
                        parent=vc.concept2,
                        child=item)
                    self.add_item(ca)
                    
                    new_vc, created = VerbConstruct.objects.get_or_create(
                        concept1_id=vc.concept1_id,
                        verb_id=vc.verb_id,
                        complex_verb_id=vc.complex_verb_id,
                        concept2_id=item.id, # item id
                        amount2=vc.amount2,
                        assertion2=vc.assertion2,
                        question_fragment2=vc.question_fragment2,
                        verb_construct2=vc.verb_construct2,
                        property2=vc.property2)
                    self.add_item(new_vc)

                    #new_vc = self.struct_mgr.copy(VerbConstruct, vc, add={'concept2_id': item.id})
                    #self.add_item(new_vc)


    def trigram_ca_was_verb(self, trigram, before, after):
        ca, sws_which_that_was, c_verb = trigram
        verb = c_verb if isinstance(c_verb, Verb) else None
        cverb = c_verb if isinstance(c_verb, ComplexVerb) else None
        # vc, created = VerbConstruct.objects.get_or_create(
        #     concept1=ca.child,
        #     verb=verb,
        #     complex_verb=cverb,
        #     concept2=None)
        vc = self.struct_mgr.new_vc(VerbConstruct(
                concept1=ca.child,
                verb=verb,
                complex_verb=cverb))
        self.add_item(vc)
        self.reinterpret(before + [vc] + after)

    def _4gram_cverb(self, _4gram, before, after):
        c1, sw, cverb, c2 = _4gram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            complex_verb=cverb,
            concept2=c2)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def _4gram_category_group(self, _4gram, before, after):
        category, prep, sw, concept = _4gram
        groups = Group.objects.filter(
            parent_concept=concept,
            child_concept=category.parent).all()
        if groups:
            group = groups[0]
            group_instance, created = GroupInstance.objects.get_or_create(
                group=group,
                parent_concept=concept,
                child_concept=category.child)
            self.add_item(group_instance)
        
    def _4gram_property(self, _4gram, before, after):
        prop, sw, verb, c1 = _4gram
        if not prop.value_concept:
            pv, created = PropertyValue.objects.get_or_create(
                concept=c1)
            if not pv.props.filter(pk=prop.id).count():
                pv.props.add(prop)
            # prop.value_concept = c1
            # prop.save()
            self.add_item(prop)

    def _4gram_date(self, _4gram, before, after):
        c1, sw_was, cverb, number = _4gram
        time_name = str(number.number)
        if cverb.preposition.name == "IN":
            time_name = str(int(number.number))
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            verb=cverb.verb,
            concept2=None,
            time=time_name)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def _4gram_cvc(self, _4gram, before, after):
        c1, cverb, sw_the, c2 = _4gram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=c1,
            complex_verb=cverb,
            concept2=c2)
        self.add_item(verb_construct)
        self.reinterpret(before + [verb_construct] + after)

    def _4gram_can(self, _4gram, before, after):
        ass, sw_can, verb, concept = _4gram
        verb_construct, created = VerbConstruct.objects.get_or_create(
            concept1=ass.concept1,
            verb=verb,
            concept2=concept)
        self.add_item(verb_construct)
        if_stmt, created = IfStmt.objects.get_or_create(
            assertion1=ass,
            vc2=verb_construct)
        self.add_item(if_stmt)

    def _4gram_amount_group(self, _4gram, before, after):
        amount, sw1_in, sw2, c = _4gram
        group, created = Group.objects.get_or_create(
            parent_concept=c,
            child_concept=amount.concept or amount.unit,
            size=amount.number)
        self.add_item(group)
        self.reinterpret(before + [group] + after)

    def _4gram_sub_prop(self, _4gram, before, after):
        prop, punc, sw_s, c = _4gram
        new_prop = prop.add_subprop(concept=c)
        self.add_item(new_prop)
        self.reinterpret(before + [new_prop] + after)

        if self.word_mgr.is_plural(c):
            group, created = Group.objects.get_or_create(
                parent_property=prop,
                child_concept=self.word_mgr.get_singular_concept(c))
            self.add_item(group)
            self.reinterpret(before + [group] + after)

    def _4gram_thatwas_cv_time(self, _4gram, before, after):
        c1, sws_thatwas, cverb, time = _4gram
        vc, created = VerbConstruct.objects.get_or_create(
           concept1=c1,
           complex_verb=cverb,
           time=time.name)        
        self.add_item(vc)
        self.reinterpret(before + [vc] + after)

    def _5gram_group(self, _5gram, before, after):
        concept, sw, number, sws, group = _5gram
        group_instance, created = GroupInstance.objects.get_or_create(
            group=group,
            parent_concept=group.parent_concept,
            child_concept=concept)
        self.add_item(group_instance)
        self.reinterpret(before + [group_instance] + after)

    def add_item(self, item):
        key_name = item.__class__.__name__.lower() + 's'
        self.learned[key_name] = self.learned.get(key_name, [])
        if item not in self.learned.get(key_name, []):
            self.learned[key_name] += [item]

    def reinterpret(self, interpretation):
        interpretation_size = len(interpretation)
        should_add = True
        for existing_interpretation in self.interpretations:
            same = True
            if len(existing_interpretation) == interpretation_size:
                for i, item in enumerate(existing_interpretation):
                    if self.word_mgr.is_model(item):
                        if item != interpretation[i]:
                            same = False
                            break
                    else:
                        if not self.word_mgr.equals(item, interpretation[i]):
                            same = False
                            break
            else:
                same = False

            if same:
                should_add = False
                break
            # else:
            #     try:
            #         print existing_interpretation[0].id,existing_interpretation[0],existing_interpretation
            #         print interpretation[0].id,interpretation[0],interpretation
            #         print '!!!'
            #     except:
            #         pass

        if should_add:
            self.interpretations += [interpretation]
            self.process_thought(interpretation)
                
    
                
