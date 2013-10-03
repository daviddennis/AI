import itertools
from django.db import models

class Concept(models.Model):
    name = models.CharField(max_length=1000)
    frequency = models.IntegerField(null=True)
    stats_status = models.CharField(max_length=200, default="needs update", null=False)
    url = models.CharField(max_length=2000, null=True)

    time_keyword = None

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
    rank = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        if self.rank:
            return "%s -> [%s] (rank: %d)" % (self.parent_concept, self.child_concept, self.rank)
        else:
            return "%s -> [%s]" % (self.parent_concept, self.child_concept)
    

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
    relation = models.ForeignKey(Relation)
    concept1 = models.ForeignKey(Concept, related_name="assertion_1_set")
    concept2 = models.ForeignKey(Concept, related_name="assertion_2_set")
    adj2 = models.ForeignKey(Adjective, related_name="adj_2_set", null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    context = models.ForeignKey(Context, related_name="assertion_context_set", null=True, blank=True)
    
    def __unicode__(self):
        orig = "%s %s %s" % (self.concept1, self.relation, self.concept2)
        if self.context:
            orig += " in the context of %s" % self.context.concept.name
        return orig

class Amount(models.Model):
    number = models.FloatField()
    concept = models.ForeignKey(Concept, related_name="amount_set")
    unit = models.ForeignKey(Concept, related_name="unit_set", null=True, blank=True)

    def __unicode__(self):
        if self.unit:
            return "%d %s of %s" % (self.number, self.unit, self.concept)
        else:
            return "%d %s" % (self.number, self.concept)

class Verb(models.Model):
    name = models.CharField(max_length=500)
    past_name = models.CharField(max_length=500, null=True, blank=True)
    participle_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return "%s" % (self.name)

class VerbConstruct(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="verb_1_set", null=True, blank=True)
    verb = models.ForeignKey(Verb)
    concept2 = models.ForeignKey(Concept, related_name="verb_2_set", null=True, blank=True)
    amount2 = models.ForeignKey(Amount, related_name="amount_2_set", null=True, blank=True)
    assertion2 = models.ForeignKey(Adjective, related_name="vc_adj_2_set", null=True, blank=True)
    verb_construct2 = models.ForeignKey('self', related_name='vc_2_set', null=True, blank=True)

    context = models.ForeignKey(Context, related_name="verb_context_set", null=True, blank=True)

    def __unicode__(self):
        if self.concept1 and self.concept2:
            return "%s(%s, %s)" % (self.verb.name, self.concept1.name, self.concept2.name)
        else:
            if self.amount2:
                return "%s(%s, %s)" % (self.verb.name, self.concept1.name, self.amount2)
            else:
                if self.verb_construct2:
                    return "%s(%s, %s)" % (self.verb.name, self.concept1.name, self.verb_construct2)
                else:
                    return "%s(%s)" % (self.verb.name, (self.concept1 or self.concept2).name)

class IfStmt(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="concept_1_set", null=True, blank=True)
    assertion1 = models.ForeignKey(Assertion, related_name="if_1_ass_set", null=True, blank=True)
    vc1 = models.ForeignKey(VerbConstruct, related_name="if_1_set", null=True, blank=True)
    concept2 = models.ForeignKey(Concept, related_name="concept_2_set", null=True, blank=True)
    assertion2 = models.ForeignKey(Assertion, related_name="if_2_ass_set", null=True, blank=True)
    vc2 = models.ForeignKey(VerbConstruct, related_name="if_2_set", null=True, blank=True)

    def __unicode__(self):
        arg1 = self.vc1 or self.assertion1 or self.concept1
        arg2 = self.vc2 or self.assertion2 or self.concept2
        return "IF: %s -> %s" % (arg1, arg2)


# class SentenceRecord

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
        self.name = name

    @property
    def number(self):
        return float(self.name)

    def __repr__(self):
        return 'Number: %s' % self.name

class Time():
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Time: %s' % self.name

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

