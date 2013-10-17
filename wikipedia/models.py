import itertools
from django.db import models
from django.dispatch import receiver
from wikipedia.lib.utils import autoconnect_to_signals

class Concept(models.Model):
    name = models.CharField(max_length=1000)
    plural_name = models.CharField(max_length=500, null=True, blank=True)
    frequency = models.IntegerField(null=True)
    stats_status = models.CharField(max_length=200, default="needs update", null=False)
    url = models.CharField(max_length=2000, null=True)

    time_keyword = None

    hit = 0

    def __unicode__(self):
        if self.time_keyword:
            return self.name + ' at ' + self.time_keyword
        else:
            return self.name

    #def with_category(self):
    #    return '%s is a %s' % (self.name, self.category.name)

    pos = None

class Connection(models.Model):
    conceptA = models.ForeignKey(Concept, related_name="concept_a_set")
    conceptB = models.ForeignKey(Concept, related_name="concept_b_set")
    weight = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s - %s -> %s' % (self.weight, self.conceptA.name, self.conceptB.name)

class Alias(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="alias_1_set")
    concept2 = models.ForeignKey(Concept, related_name="alias_2_set")

    def __unicode__(self):
        return '%s = %s' % (self.concept1, self.concept2)

class Context(models.Model):
    concept = models.ForeignKey(Concept, related_name="context_set")
    
    def __unicode__(self):
        return 'Context "%s"' % self.concept.name

class Category(models.Model):
    parent = models.ForeignKey(Concept, related_name="instance_set")
    child = models.ForeignKey(Concept, related_name="category_set")

    def __unicode__(self):
        return "%s is a type of %s" % (self.child, self.parent)

class PersonName(models.Model):
    name = models.CharField(max_length=500)
    frequency = models.FloatField(null=True, blank=True)
    rank = models.FloatField(null=True, blank=True)
    male_pct = models.FloatField(null=True, blank=True)
    female_pct = models.FloatField(null=True, blank=True)
    first_pct = models.FloatField(null=True, blank=True)
    last_pct = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class StopwordSequence(models.Model):
    string = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.string


class Group(models.Model):
    parent_concept = models.ForeignKey(Concept, related_name="abstract_parent_set")
    child_concept = models.ForeignKey(Concept, related_name="abstract_child_set")
    size = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        if self.size:
            if self.size == 3:
                val = "%s -> [%s, %s, %s]" % (self.parent_concept, 
                                              self.child_concept, 
                                              self.child_concept,
                                              self.child_concept)
            elif self.size == 2:
                val = "%s -> [%s, %s]" % (self.parent_concept, 
                                          self.child_concept, 
                                          self.child_concept)
            else:
                val = "%s -> [%s, %s, %s, ...]" % (self.parent_concept, 
                                                   self.child_concept, 
                                                   self.child_concept,
                                                   self.child_concept)
        else:   
            val = "%s -> [%s, %s, %s, ...]" % (self.parent_concept, 
                                               self.child_concept, 
                                               self.child_concept,
                                               self.child_concept)
        if self.size:
            val += "*(%d)" % self.size
        return val


class GroupInstance(models.Model):
    group = models.ForeignKey(Group, related_name="instance_set")
    parent_concept = models.ForeignKey(Concept, related_name="parent_set")
    child_concept = models.ForeignKey(Concept, related_name="child_set")

    def __unicode__(self):
        return "%s -> [%s]" % (self.parent_concept, self.child_concept)


class Rank(models.Model):
    group_instance = models.ForeignKey(GroupInstance, related_name="rank_set")
    rank = models.IntegerField()
    
    concept = models.ForeignKey(Concept, null=True, blank=True)
    #prep_construct = 

    sws = models.ForeignKey(StopwordSequence, null=True, blank=True)

    def __unicode__(self):
        if self.concept:
            if self.sws:
                return "%s #%s %s %s" % (self.group_instance, self.rank, self.sws, self.concept)
            else:
                return "%s #%s %s" % (self.group_instance, self.rank, self.concept)


class Relation(models.Model):
    name = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.name


class Adjective(models.Model):
    name = models.CharField(max_length=500)
    superlative = models.CharField(max_length=500, blank=True, null=True)

    form = None
    #form = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        if self.form == 'superlative':
            return self.superlative
        else:
            return self.name


class Assertion(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="assertion_1_set")

    relation = models.ForeignKey(Relation)

    concept2 = models.ForeignKey(Concept, related_name="assertion_2_set", null=True, blank=True)
    adj2 = models.ForeignKey(Adjective, related_name="adj_2_set", null=True, blank=True)

    score = models.IntegerField(null=True, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    context = models.ForeignKey(Context, related_name="assertion_context_set", null=True, blank=True)
    
    def __unicode__(self):
        orig = "%s %s %s" % (self.concept1, self.relation, (self.concept2 or self.adj2))
        if self.context:
            orig += " in the context of %s" % self.context.concept.name
        return orig

# NL Structure
class Amount(models.Model):
    quantifier = models.ForeignKey('Quantifier', related_name="quant_set", null=True, blank=True)

    number = models.FloatField(null=True, blank=True)
    concept = models.ForeignKey(Concept, related_name="amount_set")
    unit = models.ForeignKey(Concept, related_name="unit_set", null=True, blank=True)

    def __unicode__(self):
        if self.number:
            if self.unit:
                return "%d %s of %s" % (self.number, self.unit, self.concept)
            else:
                return "%d %s" % (self.number, self.concept)
        else:
            return "%s %s" % (self.quantifier, self.concept)

# Lookup
class Preposition(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

# Lookup
class Verb(models.Model):
    name = models.CharField(max_length=500)
    past_name = models.CharField(max_length=500, null=True, blank=True)
    participle_name = models.CharField(max_length=100, null=True, blank=True)
    
    form = None

    def __unicode__(self):
        form = self.form
        if form:
            if form == 'past':
                return "%s" % (self.past_name)
            elif form == 'participle':
                return "%s" % (self.participle_name)
            else:
                return "%s" % (self.name)
        else:
            return "%s" % (self.name)

class ComplexVerb(models.Model):
    verb = models.ForeignKey(Verb)
    preposition = models.ForeignKey(Preposition)
    prep2 = models.ForeignKey(Preposition, related_name="prep2_set", null=True, blank=True)

    def __unicode__(self):
        if self.prep2:
            return "%s %s %s" % (self.verb.name, self.preposition.name, self.prep2.name)
        else:
            return "%s %s" % (self.verb.name, self.preposition.name)

# NL Structure
@autoconnect_to_signals
class VerbConstruct(models.Model):
    quantifier = models.ForeignKey('Quantifier', related_name="vc_quant_set", null=True, blank=True)

    concept1 = models.ForeignKey(Concept, related_name="verb_1_set", null=True, blank=True)
    amount1 = models.ForeignKey(Amount, related_name="amount_1_set", null=True, blank=True)
    #assertion1 = models.ForeignKey(Adjective, related_name="vc_adj_1_set", null=True, blank=True)

    verb = models.ForeignKey(Verb, null=True, blank=True)
    complex_verb = models.ForeignKey(ComplexVerb, null=True, blank=True)
    
    concept2 = models.ForeignKey(Concept, related_name="verb_2_set", null=True, blank=True)
    amount2 = models.ForeignKey(Amount, related_name="amount_2_set", null=True, blank=True)
    assertion2 = models.ForeignKey(Adjective, related_name="vc_adj_2_set", null=True, blank=True)
    question_fragment2 = models.ForeignKey('QuestionFragment', related_name="qf_2_set", null=True, blank=True)
    verb_construct2 = models.ForeignKey('self', related_name='vc_2_set', null=True, blank=True)

    context = models.ForeignKey(Context, related_name="verb_context_set", null=True, blank=True)

    time = models.CharField(max_length=200, null=True, blank=True)

    @property
    def arg1(self):
        return self.concept1 or self.amount1 #or self.assertion1

    @property
    def arg2(self):
        return self.concept2 or self.amount2 or self.assertion2 or self.question_fragment2 or self.verb_construct2

    def pre_save(self):
        if self.verb:
            if self.verb.form == 'past':
                self.time = 'THE PAST'

    def __unicode__(self):
        output = ''

        if self.verb:
            verb_name = self.verb.name
        elif self.complex_verb:
            verb_name = str(self.complex_verb)

        item1 = self.concept1 or self.amount1 #or self.assertion1

        if item1 and self.concept2:
            output = "%s(%s, %s)" % (verb_name, item1, self.concept2.name)
        else:
            if self.amount2:
                output = "%s(%s, %s)" % (verb_name, item1, self.amount2)
            else:
                if self.verb_construct2:
                    output = "%s(%s, %s)" % (verb_name, item1, self.verb_construct2)
                else:
                    output = "%s(%s)" % (verb_name, (item1 or self.concept2).name)

        if self.time:
            output += ' @ %s' % self.time

        if self.quantifier:
            output = str(self.quantifier) + '+' + output

        return output

# NL Structure
class IfStmt(models.Model):

    concept1 = models.ForeignKey(Concept, related_name="concept_1_set", null=True, blank=True)
    assertion1 = models.ForeignKey(Assertion, related_name="if_1_ass_set", null=True, blank=True)
    vc1 = models.ForeignKey(VerbConstruct, related_name="if_1_set", null=True, blank=True)

    concept2 = models.ForeignKey(Concept, related_name="concept_2_set", null=True, blank=True)
    assertion2 = models.ForeignKey(Assertion, related_name="if_2_ass_set", null=True, blank=True)
    vc2 = models.ForeignKey(VerbConstruct, related_name="if_2_set", null=True, blank=True)
    category2 = models.ForeignKey(Category, related_name="category_2_set", null=True, blank=True)

    def __unicode__(self):
        arg1 = self.vc1 or self.assertion1 or self.concept1
        arg2 = self.vc2 or self.assertion2 or self.concept2 or self.category2
        return "IF: %s -> %s" % (arg1, arg2)


class QuestionFragment(models.Model):
    q_word = models.CharField(max_length=50)
    verb_construct = models.ForeignKey(VerbConstruct)

    def __unicode__(self):
        return "%s-%s" % (self.q_word, self.verb_construct)


class PrepConstruct(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="pc_c_1_set", null=True, blank=True)
    vc1 = models.ForeignKey(VerbConstruct, related_name="pc_vc_1_set", null=True, blank=True)
    
    preposition = models.ForeignKey(Preposition)

    concept2 = models.ForeignKey(Concept, related_name="pc_2_set")

    def __unicode__(self):
        arg1 = self.concept1 or self.vc1
        return "%s %s %s" % (arg1, 
                             self.preposition.name.lower(),
                             self.concept2)


class Property(models.Model):
    parent = models.ForeignKey(Concept, related_name="prop_parent_set")

    key_concept = models.ForeignKey(Concept, related_name="prop_key_set")

    value_concept = models.ForeignKey(Concept, related_name="prop_value_set", null=True, blank=True)
    value_amount = models.ForeignKey(Amount, related_name="prop_amount_set", null=True, blank=True)

    def __unicode__(self):
        if self.value_concept or self.value_amount:
            return "%s-%s = %s" % (self.parent,
                                   self.key_concept,
                                   self.value_concept or self.value_amount)
        else:
            return "%s-%s" % (self.parent,
                              self.key_concept)

class Entity(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    concept = models.ForeignKey(Concept, related_name="entity_set", null=True, blank=True)

    def __unicode__(self):
        if self.concept:
            return self.concept.name
        else:
            return "%s %s" % (self.first_name, self.last_name)


class Quantifier(models.Model):
    name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name

class Name(models.Model):
    concept = models.ForeignKey(Concept, related_name="name_c_set", null=True, blank=True)

    entity = models.ForeignKey(Entity, related_name="name_e_set", null=True, blank=True)
    prep_construct = models.ForeignKey(PrepConstruct, related_name="name_pc_set", null=True, blank=True)
    verb_construct = models.ForeignKey(VerbConstruct, related_name="name_vc_set", null=True, blank=True)
    group_instance = models.ForeignKey(GroupInstance, related_name="name_gi_set", null=True, blank=True)

    @property
    def arg2(self):
        return self.entity or self.prep_construct or self.verb_construct or self.group_instance
    
    def __unicode__(self):
        return "(%s) name for (%s)" % (self.concept, self.arg2)

# Class SentenceRecord

# class Dialogue(models.Model):
#     sentence = models.CharField(max_length=2000)

# class History(models.Model):
#     dialogue

# Non-table models
class Stopword():
    def __init__(self, stopword):
        self.name = stopword

    def __repr__(self):
        return 'Stopword: %s' % self.name

class Punctuation():
    def __init__(self, punctuation):
        self.name = punctuation

    def __repr__(self):
        return 'Punctuation: %s' % self.name

class Number():
    def __init__(self, name):
        self.name = str(name)

    @property
    def number(self):
        return float(self.name)

    def __repr__(self):
        return "Number: %s" % ("{:,.2f}".format(float(self.name)))


class Time():
    
    def __init__(self, name, _type=None):
        self.name = name
        self.type = _type

    def __repr__(self):
        if self.type:
            return '(%s) %s' % (self.type, self.name)
        else:
            return 'Time: %s' % (self.name)

class Money():
    
    def __init__(self, name, sign="$"):
        self.name = name
        self.sign = sign
        
    def __repr__(self):
        return "Money: %s %s" % (self.sign, "{:,.2f}".format(float(self.name)))

class List():

    def __init__(self, items, _type=None):
        if len(items) > 1000:
            raise 'Too many items to make _list'
        self.items = items
        if _type:
            self.type = _type
        else:
            self.detect_type()
            # except:
            #     pass

    def detect_type(self):
        if len(set([c.name for c in self.items])) == 1:
            the_category = self.items[0]
        else:
            try:
                the_category = self.items[0].category_set.all()[0].parent
            except:
                the_category = self.items[0]
        # category_list = self.items[0].category_set.all()
        # for category in category_list:
        #     for item in self.items[1:]:
        #         if category not in item.category_set.all():
        #             continue
        #     the_category = category
        # print the_category,'!!!'
        self.type = the_category
        #for item in self.items[1:]:
        #    for category in item.category_set.all():
        #        if category not in category_list:
                    
    #     d = {}
    #     for item in self.items:
    #         for category_id in [c.id for c in item.category_set.all()]:
    #             d[category_id] = d.get(category_id, 0)
            

    # def __getitem__(self,index):
    #     try:
    #         return next(itertools.islice(self.items,index,index+1))
    #     except TypeError:
    #         return list(itertools.islice(self.items,index.start,index.stop,index.step))        

    def __repr__(self):
        if len(self.items) >= 3:
            return 'List: %s...' % self.items[:3]
        else:
            return 'List: %s' % self.items


