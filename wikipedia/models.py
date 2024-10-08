import itertools
from django.db import models
from django.dispatch import receiver
from wikipedia.lib.utils import autoconnect_to_signals, safe_get_or_create

class Concept(models.Model):
    name = models.CharField(db_index=True, max_length=1000)

    plural_name = models.CharField(max_length=500, null=True, blank=True)
    frequency = models.IntegerField(null=True)
    stats_status = models.CharField(max_length=200, default="needs update", null=False)
    url = models.CharField(max_length=2000, null=True)

    sense = None

    time = None

    hit = 0

    the = False
    a = False

    pos = None

    def __unicode__(self):
        output = ""
        name = self.name
        if self.a:
            if name[0] in "AEIOU".split():
                output += "AN "
            else:
                output += "A "
        if self.the:
            output += "THE "
        if self.time:
            output += '%s at %s' % (name, self.time)
        else:
            output += name
        if self.sense:
            output += " (%s)" % self.sense.sense_concept
        return output



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

class Sense(models.Model):
    concept = models.ForeignKey(Concept, related_name="sense_c_set")
    sense_concept = models.ForeignKey(Concept, related_name="sense_sense_set")

    def __unicode__(self):
        return "%s (%s)" % (self.concept, self.sense_concept)

class Context(models.Model):
    concept = models.ForeignKey(Concept, related_name="context_set")
    
    def __unicode__(self):
        return 'Context "%s"' % self.concept.name

class Category(models.Model):
    parent = models.ForeignKey(Concept, related_name="instance_set")
    child = models.ForeignKey(Concept, related_name="category_set")

    qf_s = models.ManyToManyField('QuestionFragment', null=True, blank=True)
    #assertions = models.ManyToManyField('Assertion', null=True, blank=True)

    def __unicode__(self):
        output = "%s is a type of" % self.child
        #assertions = self.assertions.all()
        #if assertions:
        #    output += " " + str([x. assertions)
        output += " " + str(self.parent)
        qf_s = self.qf_s.all()
        if qf_s:
            output += " " + str(qf_s)
        return output

# class ConceptType(models.Model):
#     concept = models.ForeignKey(Concept, related_name="ctype_c_set")
#     _type = models.ForeignKey(Concept, related_name="ctype_type_set")

#     def __unicode__(self):
#         return "%s TYPE %s" % (self.concept, self._type)

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

    quantifier = models.ForeignKey('Quantifier', null=True, blank=True)

    parent_property = models.ForeignKey('Property', null=True, blank=True)
    parent_concept = models.ForeignKey(Concept, related_name="abstract_parent_set", null=True, blank=True)

    child_concept = models.ForeignKey(Concept, related_name="abstract_child_set")

    size = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        val = ""
        if self.quantifier:
            val += "%s+" % self.quantifier
        parent = self.parent_concept or self.parent_property
        if self.size:
            if self.size == 3:
                val += "%s -> [%s, %s, %s]" % (parent, 
                                              self.child_concept, 
                                              self.child_concept,
                                              self.child_concept)
            elif self.size == 2:
                val += "%s -> [%s, %s]" % (parent, 
                                          self.child_concept, 
                                          self.child_concept)
            else:
                val += "%s -> [%s, %s, %s, ...]" % (parent, 
                                                   self.child_concept, 
                                                   self.child_concept,
                                                   self.child_concept)
        else:   
            val += "%s -> [%s, %s, %s, ...]" % (parent,
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
        if self.parent_concept == self.group.parent_concept:
            return "%s -> [%s:%s]" % (self.parent_concept, self.group.child_concept, self.child_concept)
        else:
            return "%s:%s -> [%s:%s]" % (self.group.parent_concept, self.parent_concept, 
                                         self.group.child_concept, self.child_concept)


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


class Adverb(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Assertion(models.Model):
    #quantifier = models.ForeignKey('Quantifier', null=True, blank=True)

    concept1 = models.ForeignKey(Concept, related_name="assertion_1_set", null=True, blank=True)
    property1 = models.ForeignKey('Property', related_name="ass_prop_1_set", null=True, blank=True)

    relation = models.ForeignKey(Relation)

    score = models.IntegerField(null=True, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    context = models.ForeignKey(Context, related_name="assertion_context_set", null=True, blank=True)

    def __unicode__(self):
        output = ""
        #if self.quantifier:
        #    output += "%s+" % (self.quantifier)
        output = "%s %s " % (self.concept1 or self.property1, self.relation)
        values = self.ass_value_set.all()
        if values:
            if len(values) == 1:
                output += str(values[0])
            else:
                output += str(values)
        if self.context:
            output += " in the context of %s" % self.context.concept.name
        return output


class AssertionValue(models.Model):
    assertions = models.ManyToManyField(Assertion, related_name="ass_value_set")
    
    concept = models.ForeignKey(Concept, related_name="ass_c_value_set", null=True, blank=True)
    adj = models.ForeignKey(Adjective, related_name="ass_adj_value_set", null=True, blank=True)

    @property                            
    def arg2(self):
        return self.concept or self.adj

    def __unicode__(self):
        return str(self.arg2)


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
    s_form = models.CharField(max_length=100, null=True, blank=True)

    form = None

    def __unicode__(self):
        form = self.form
        if form:
            if form == 'past':
                return "%s" % (self.past_name)
            elif form == 'participle':
                return "%s" % (self.participle_name)
            elif form == 's':
                return self.s_form
            else:
                return "%s" % (self.name)
        else:
            return "%s" % (self.name)

class ComplexVerb(models.Model):
    verb = models.ForeignKey(Verb)
    preposition = models.ForeignKey(Preposition, null=True, blank=True)
    prep2 = models.ForeignKey(Preposition, related_name="prep2_set", null=True, blank=True)
    adverb = models.ForeignKey(Adverb, related_name="cverb_adverb_set", null=True, blank=True)

    def __unicode__(self):
        output = str(self.verb)

        if self.preposition:
            output += " %s" % self.preposition
        if self.prep2:
            output += " %s" % self.prep2
        if self.adverb:
            output += " %s" % self.adverb

        return output
        

# NL Structure
@autoconnect_to_signals
class VerbConstruct(models.Model):
    quantifier = models.ForeignKey('Quantifier', related_name="vc_quant_set", null=True, blank=True)

    concept1 = models.ForeignKey(Concept, related_name="verb_1_set", null=True, blank=True)
    amount1 = models.ForeignKey(Amount, related_name="amount_1_set", null=True, blank=True)
    #assertion1 = models.ForeignKey(Adjective, related_name="vc_adj_1_set", null=True, blank=True)
    property1 = models.ForeignKey('Property', related_name='vc_prop_1_set', null=True, blank=True)

    verb = models.ForeignKey(Verb, null=True, blank=True)
    complex_verb = models.ForeignKey(ComplexVerb, null=True, blank=True)
    
    concept2 = models.ForeignKey(Concept, related_name="verb_2_set", null=True, blank=True)
    amount2 = models.ForeignKey(Amount, related_name="amount_2_set", null=True, blank=True)
    assertion2 = models.ForeignKey(Assertion, related_name="vc_adj_2_set", null=True, blank=True)
    question_fragment2 = models.ForeignKey('QuestionFragment', related_name="qf_2_set", null=True, blank=True)
    verb_construct2 = models.ForeignKey('self', related_name='vc_2_set', null=True, blank=True)
    property2 = models.ForeignKey('Property', related_name='vc_prop_2_set', null=True, blank=True)
    
    context = models.ForeignKey(Context, related_name="verb_context_set", null=True, blank=True)
    
    time = models.CharField(max_length=200, null=True, blank=True)
    
    verb_form = None

    @property
    def arg1(self):
        return self.concept1 or self.amount1 or self.property1#or self.assertion1

    @property
    def arg2(self):
        return self.concept2 or self.amount2 or self.assertion2 or self.question_fragment2 or self.verb_construct2 or self.property2

    def pre_save(self):
        if self.verb:
            if self.verb.form == 'past':
                self.time = 'THE PAST'

    def __unicode__(self):
        output = ''

        if self.verb:
            if self.verb.form:
                if self.verb.form.lower() == "past":
                    verb_name = self.verb.past_name
                elif self.verb.form.lower() == "participle":
                    verb_name = self.verb.participle_name
                elif self.verb.form.lower() == "s":
                    verb_name = self.verb.s_form
            else:
                verb_name = self.verb.name
        elif self.complex_verb:
            verb_name = str(self.complex_verb)

        item1 = self.arg1
        item2 = self.arg2

        if item1:
            if item2:
                output = "%s(%s, %s)" % (verb_name, item1, item2)
            else:
                output = "%s(%s,)" % (verb_name, item1)
        else:
            output = "%s(,%s)" % (verb_name, item2)
            
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
    verb_construct = models.ForeignKey(VerbConstruct, null=True, blank=True)
    prep_construct = models.ForeignKey('PrepConstruct', null=True, blank=True)
    
    def __unicode__(self):
        if self.verb_construct:
            return "%s-%s" % (self.q_word, self.verb_construct)
        elif self.prep_construct:
            return "%s-%s" % (self.q_word, self.prep_construct)


class PrepConstruct(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="pc_c_1_set", null=True, blank=True)
    vc1 = models.ForeignKey(VerbConstruct, related_name="pc_vc_1_set", null=True, blank=True)
    property1 = models.ForeignKey('Property', related_name="pc_prop_1_set", null=True, blank=True)
    
    preposition = models.ForeignKey(Preposition)

    concept2 = models.ForeignKey(Concept, related_name="pc_2_set")

    @property
    def arg1(self):
        return self.concept1 or self.vc1 or self.property1

    def __unicode__(self):
        return "%s %s %s" % (self.arg1, 
                             self.preposition.name.lower(),
                             self.concept2)


class Property(models.Model):
    parent = models.ForeignKey(Concept, related_name="prop_parent_set", null=True, blank=True)
    parent_vc = models.ForeignKey(VerbConstruct, null=True, blank=True)

    key_concept = models.ForeignKey(Concept, related_name="prop_key_set")

    sub_prop = models.ForeignKey('self', null=True, blank=True)

    def add_subprop(self, prop=None, concept=None):

        if prop:
            raise Exception('No add subprop prop handling')

        if concept:
            new_sp, created = safe_get_or_create(Property,
                                                 parent=self.key_concept,
                                                 key_concept=concept)
            prop, created = safe_get_or_create(Property,
                                               parent=self.parent,
                                               key_concept=self.key_concept,
                                               sub_prop=new_sp)
            #new_sp, created = Property.objects.get_or_create(
            #    parent=self.key_concept,
            #    key_concept=concept)
            #prop, created = Property.objects.get_or_create(
            #    parent=self.parent,
            #    key_concept=self.key_concept,
            #    sub_prop=new_sp)
            return prop

    @property
    def num_sub_props(self):
        num = 0
        if self.sub_prop:
            num += 1 + self.sub_prop.num_sub_props
        return num
        
    def __unicode__(self):
        output = ""
        parent = self.parent or self.parent_vc
        if self.sub_prop:
            output = "%s-%s" % (parent, self.sub_prop)
        else:
            output = "%s-%s" % (parent, self.key_concept)
        if self.pv_set:
            values = [x.value for x in self.pv_set.all()]
            if len(values) > 1:
                output += " = " + str(values)
            else:
                if values:
                    output += " = " + str(values[0])
        return output


class PropertyValue(models.Model):

    props = models.ManyToManyField(Property, related_name="pv_set")

    concept = models.ForeignKey(Concept, related_name="prop_value_c_set", null=True, blank=True)
    amount = models.ForeignKey(Amount, related_name="prop_amount_set", null=True, blank=True)

    time = models.CharField(max_length=200, null=True, blank=True)

    @property
    def value(self):
        return self.concept or self.amount

    def __unicode__(self):
        return str(self.prop) + " = " + str(self.value)

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
    prop = models.ForeignKey(Property, related_name="name_prop_set", null=True, blank=True)

    @property
    def arg2(self):
        return self.entity or self.prep_construct or self.verb_construct or self.group_instance or self.prop
    
    def __unicode__(self):
        return "(%s) name for (%s)" % (self.concept, self.arg2)


class Negation(models.Model):

    verb_construct = models.ForeignKey(VerbConstruct, null=True, blank=True)
    prep_construct = models.ForeignKey(PrepConstruct, null=True, blank=True)
    assertion = models.ForeignKey(Assertion, null=True, blank=True)

    @property
    def item(self):
        return self.verb_construct or self.prep_construct or self.assertion

    def __unicode__(self):
        return self.item


class Title(models.Model):
    concept = models.ForeignKey(Concept)

    def __unicode__(self):
        return self.concept.name


# class Definition(models.Model):
#     concept = models.ForeignKey(Concept)

#     vc = models.ForeignKey(VerbConstruct, related_name="def_vc_set", null=True, blank=True)
#     pc = models.ForeignKey(PrepConstruct, related_name="def_pc_set", null=True, blank=True)
#     ass = models.ForeignKey(Assertion, related_name="def_ass_set", null=True, blank=True)
#     prop = models.ForeignKey(Assertion, related_name="def_prop_set", null=True, blank=True)
    
#     @property
#     def definition(self):
#         return self.vc or self.pc or self.ass or self.prop

#     def __unicode__(self):
#         return "%s DEFINITION: %s" % (self.concept, self.definition)


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
        num = float(self.name)
        if num.is_integer():
            return int(num)
        else:
            return num

    def __repr__(self):
        num = float(self.name)
        if num.is_integer():
            return "Number: %s" % (int(num))
        else:
            return "Number: %s" % ("{:,.2f}".format(float(self.name)))


class Time():
    
    def __init__(self, name, _type=None):
        self.name = name
        self.type = _type
        
        self.adj = None

        self.month = None
        self.day = None
        self.year =  None

        if self.type == "DATE":
            if ' ' in self.name:
                tokens = self.name.split(' ')
                if len(tokens) == 2:
                    self.month = tokens[0]
                    self.day = tokens[1]
            elif '/' in self.name:
                tokens = self.name.split('/')
                if len(tokens) == 2:
                    self.month = tokens[0]
                    self.year = tokens[1]
                if len(tokens) == 3:
                    self.month = tokens[0]
                    self.day = tokens[1]
                    self.year = tokens[2]

    def add_adj(self, adj):
        if self.adj == None:
            self.name = adj.name + " " + self.name 
        else:
            self.name = ' '.join(self.name.split(' ')[1:])
        self.adj = adj

    def add_year(self, year):
        self.year = year
        self.name += " %s" % (year)

    def __repr__(self):
        if self.type:
            return '(%s) %s' % (self.type, self.name)
        else:
            return 'Time: %s' % (self.name)

class Money():
    
    def __init__(self, name, sign="$"):
        self.name = name
        self.sign = sign
        self.number = Number(name)
        
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
        self.type = the_category
            

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




        # item1 = self.concept1 or self.amount1 #or self.assertion1

        # if item1 and self.concept2:
        #     output = "%s(%s, %s)" % (verb_name, item1, self.concept2.name)
        # else:
        #     if self.amount2:
        #         output = "%s(%s, %s)" % (verb_name, item1, self.amount2)
        #     else:
        #         if self.verb_construct2:
        #             output = "%s(%s, %s)" % (verb_name, item1, self.verb_construct2)
        #         else:
        #             output = "%s(%s)" % (verb_name, (item1 or self.concept2).name)

class QuotedItem():

    def __init__(self, items):
        self.items = items

    @property
    def name(self):
        return ' '.join([x.name for x in self.items])

    def __repr__(self):
        return "QuotedItem: '%s'" % self.name
