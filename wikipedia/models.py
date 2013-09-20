from django.db import models

class Concept(models.Model):
    name = models.CharField(max_length=1000)
    frequency = models.IntegerField(null=True)
    stats_status = models.CharField(max_length=200, default="needs update", null=False)
    category = models.ForeignKey('self', null=True, blank=True)
    url = models.CharField(max_length=2000, null=True)

    def __unicode__(self):
        return self.name

    def with_category(self):
        return '%s is a %s' % (self.name, self.category.name)

    pos = None

class Connection(models.Model):
    conceptA = models.ForeignKey(Concept, related_name="concept_a_set")
    conceptB = models.ForeignKey(Concept, related_name="concept_b_set")
    weight = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s - %s -> %s' % (self.weight, self.conceptA.name, self.conceptB.name)

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
    vc1 = models.ForeignKey(VerbConstruct, related_name="if_1_set", null=True, blank=True)
    assertion1 = models.ForeignKey(Assertion, related_name="if_1_ass_set", null=True, blank=True)
    vc2 = models.ForeignKey(VerbConstruct, related_name="if_2_set", null=True, blank=True)
    assertion2 = models.ForeignKey(Assertion, related_name="if_2_ass_set", null=True, blank=True)

    def __unicode__(self):
        arg1 = self.vc1 or self.assertion1
        arg2 = self.vc2 or self.assertion2
        return "IF %s THEN %s" % (arg1, arg2)

# Non-table models
class Stopword():
    def __init__(self, stopword):
        self.string = stopword

    def __repr__(self):
        return 'Stopword: %s' % self.string

class Punctuation():
    def __init__(self, punctuation):
        self.string = punctuation

    def __repr__(self):
        return 'Punctuation: %s' % self.string

    
