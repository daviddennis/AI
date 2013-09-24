# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IfStmt.concept1'
        db.add_column(u'wikipedia_ifstmt', 'concept1',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='concept_1_set', null=True, to=orm['wikipedia.Concept']),
                      keep_default=False)

        # Adding field 'IfStmt.concept2'
        db.add_column(u'wikipedia_ifstmt', 'concept2',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='concept_2_set', null=True, to=orm['wikipedia.Concept']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'IfStmt.concept1'
        db.delete_column(u'wikipedia_ifstmt', 'concept1_id')

        # Deleting field 'IfStmt.concept2'
        db.delete_column(u'wikipedia_ifstmt', 'concept2_id')


    models = {
        u'wikipedia.assertion': {
            'Meta': {'object_name': 'Assertion'},
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertion_1_set'", 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertion_2_set'", 'to': u"orm['wikipedia.Concept']"}),
            'frequency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Relation']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.category': {
            'Meta': {'object_name': 'Category'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instance_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category_set'", 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.concept': {
            'Meta': {'object_name': 'Concept'},
            'frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'stats_status': ('django.db.models.fields.CharField', [], {'default': "'needs update'", 'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        u'wikipedia.connection': {
            'Meta': {'object_name': 'Connection'},
            'conceptA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_a_set'", 'to': u"orm['wikipedia.Concept']"}),
            'conceptB': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_b_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'wikipedia.group': {
            'Meta': {'object_name': 'Group'},
            'child_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstract_child_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstract_parent_set'", 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.groupinstance': {
            'Meta': {'object_name': 'GroupInstance'},
            'child_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'to': u"orm['wikipedia.Concept']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_set'", 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.ifstmt': {
            'Meta': {'object_name': 'IfStmt'},
            'assertion1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'if_1_ass_set'", 'null': 'True', 'to': u"orm['wikipedia.Assertion']"}),
            'assertion2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'if_2_ass_set'", 'null': 'True', 'to': u"orm['wikipedia.Assertion']"}),
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'concept_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'concept_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vc1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'if_1_set'", 'null': 'True', 'to': u"orm['wikipedia.VerbConstruct']"}),
            'vc2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'if_2_set'", 'null': 'True', 'to': u"orm['wikipedia.VerbConstruct']"})
        },
        u'wikipedia.personname': {
            'Meta': {'object_name': 'PersonName'},
            'female_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'first_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rank': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.relation': {
            'Meta': {'object_name': 'Relation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'wikipedia.stopwordsequence': {
            'Meta': {'object_name': 'StopwordSequence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'wikipedia.verb': {
            'Meta': {'object_name': 'Verb'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'past_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.verbconstruct': {
            'Meta': {'object_name': 'VerbConstruct'},
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'verb_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'verb_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'verb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Verb']"})
        }
    }

    complete_apps = ['wikipedia']