import itertools
from django.db import models

class Concept(models.Model):
    name = models.CharField(max_length=1000)
    frequency = models.IntegerField(null=True)
    stats_status = models.CharField(max_length=200, default="needs update", null=False)
    url = models.CharField(max_length=2000, null=True)

    def __unicode__(self):
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

class Category(models.Model):
    parent = models.ForeignKey(Concept, related_name="category_set")
    child = models.ForeignKey(Concept, related_name="instance_set")

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

    def __unicode__(self):
        return "%s -> [%s, %s, %s, ...]" % (self.parent_concept, 
                                            self.child_concept, 
                                            self.child_concept,
                                            self.child_concept)

class GroupInstance(models.Model):
    group = models.ForeignKey(Group)
    parent_concept = models.ForeignKey(Concept, related_name="parent_set")
    child_concept = models.ForeignKey(Concept, related_name="child_set")

    def __unicode__(self):
        return "%s -> [%s]" % (self.parent_concept, self.child_concept)
    

class Relation(models.Model):
    name = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.name

class Assertion(models.Model):
    relation = models.ForeignKey(Relation)
    concept1 = models.ForeignKey(Concept, related_name="assertion_1_set")
    concept2 = models.ForeignKey(Concept, related_name="assertion_2_set")
    score = models.IntegerField(null=True, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    
    def __unicode__(self):
        return "%s %s %s" % (self.concept1, self.relation, self.concept2)

class Verb(models.Model):
    name = models.CharField(max_length=500)
    past_name = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.name)

class VerbConstruct(models.Model):
    concept1 = models.ForeignKey(Concept, related_name="verb_1_set", null=True, blank=True)
    verb = models.ForeignKey(Verb)
    concept2 = models.ForeignKey(Concept, related_name="verb_2_set", null=True, blank=True)

    def __unicode__(self):
        if self.concept1 and self.concept2:
            return "%s(%s, %s)" % (self.verb.name, self.concept1.name, self.concept2.name)
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

class Adjective(models.Model):
    name = models.CharField(max_length=500)
    superlative = models.CharField(max_length=500, blank=True, null=True)
    form = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        if self.form == 'superlative':
            return self.superlative
        else:
            return self.name

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

    def __repr__(self):
        return 'Number: %s' % self.name

class List():

    def __init__(self, items, _type):
        self.items = items
        self.type = _type

    # def __getitem__(self,index):
    #     try:
    #         return next(itertools.islice(self.items,index,index+1))
    #     except TypeError:
    #         return list(itertools.islice(self.items,index.start,index.stop,index.step))        

    def __repr__(self):
        return 'List: %s...' % self.items[:3]

