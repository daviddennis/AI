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
    
    def __unicode__(self):
        return "%s %s %s" % (self.concept1, self.relation, self.concept2)

# Non-table models
class Stopword():
    def __init__(self, stopword):
        self.string = stopword

    def __repr__(self):
        return self.string
