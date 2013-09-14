# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Concept.url'
        db.add_column('wikipedia_concept', 'url',
                      self.gf('django.db.models.fields.CharField')(max_length=2000, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Concept.url'
        db.delete_column('wikipedia_concept', 'url')


    models = {
        'wikipedia.concept': {
            'Meta': {'object_name': 'Concept'},
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
        'wikipedia.personname': {
            'Meta': {'object_name': 'PersonName'},
            'female_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'first_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rank': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wikipedia']