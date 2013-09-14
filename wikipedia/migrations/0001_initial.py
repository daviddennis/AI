# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Concept'
        db.create_table('wikipedia_concept', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('wikipedia', ['Concept'])

        # Adding model 'Connection'
        db.create_table('wikipedia_connection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conceptA', self.gf('django.db.models.fields.related.ForeignKey')(related_name='concept_a_set', to=orm['wikipedia.Concept'])),
            ('conceptB', self.gf('django.db.models.fields.related.ForeignKey')(related_name='concept_b_set', to=orm['wikipedia.Concept'])),
        ))
        db.send_create_signal('wikipedia', ['Connection'])


    def backwards(self, orm):
        # Deleting model 'Concept'
        db.delete_table('wikipedia_concept')

        # Deleting model 'Connection'
        db.delete_table('wikipedia_connection')


    models = {
        'wikipedia.concept': {
            'Meta': {'object_name': 'Concept'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'wikipedia.connection': {
            'Meta': {'object_name': 'Connection'},
            'conceptA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_a_set'", 'to': "orm['wikipedia.Concept']"}),
            'conceptB': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'concept_b_set'", 'to': "orm['wikipedia.Concept']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['wikipedia']