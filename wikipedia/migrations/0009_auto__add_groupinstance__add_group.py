# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupInstance'
        db.create_table('wikipedia_groupinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wikipedia.Group'])),
            ('parent_concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_set', to=orm['wikipedia.Concept'])),
            ('child_concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_set', to=orm['wikipedia.Concept'])),
        ))
        db.send_create_signal('wikipedia', ['GroupInstance'])

        # Adding model 'Group'
        db.create_table('wikipedia_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abstract_parent_set', to=orm['wikipedia.Concept'])),
            ('child_concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abstract_child_set', to=orm['wikipedia.Concept'])),
        ))
        db.send_create_signal('wikipedia', ['Group'])


    def backwards(self, orm):
        # Deleting model 'GroupInstance'
        db.delete_table('wikipedia_groupinstance')

        # Deleting model 'Group'
        db.delete_table('wikipedia_group')


    models = {
        'wikipedia.concept': {
            'Meta': {'object_name': 'Concept'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wikipedia.Concept']", 'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'stats_status': ('django.db.models.fields.CharField', [], {'default': "'needs update'", 'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        'wikipedia.connection': {
            'Meta': {'object_name': 'Connection'},
            'conceptA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_a_set'", 'to': "orm['wikipedia.Concept']"}),
            'conceptB': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_b_set'", 'to': "orm['wikipedia.Concept']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'wikipedia.group': {
            'Meta': {'object_name': 'Group'},
            'child_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstract_child_set'", 'to': "orm['wikipedia.Concept']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstract_parent_set'", 'to': "orm['wikipedia.Concept']"})
        },
        'wikipedia.groupinstance': {
            'Meta': {'object_name': 'GroupInstance'},
            'child_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'to': "orm['wikipedia.Concept']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wikipedia.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_set'", 'to': "orm['wikipedia.Concept']"})
        },
        'wikipedia.personname': {
            'Meta': {'object_name': 'PersonName'},
            'female_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'first_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rank': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'wikipedia.stopwordsequence': {
            'Meta': {'object_name': 'StopwordSequence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['wikipedia']