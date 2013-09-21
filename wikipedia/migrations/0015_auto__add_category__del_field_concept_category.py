# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'wikipedia_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='category_set', to=orm['wikipedia.Concept'])),
            ('child', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instance_set', to=orm['wikipedia.Concept'])),
        ))
        db.send_create_signal(u'wikipedia', ['Category'])

        # Deleting field 'Concept.category'
        db.delete_column(u'wikipedia_concept', 'category_id')


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'wikipedia_category')

        # Adding field 'Concept.category'
        db.add_column(u'wikipedia_concept', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wikipedia.Concept'], null=True, blank=True),
                      keep_default=False)


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
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