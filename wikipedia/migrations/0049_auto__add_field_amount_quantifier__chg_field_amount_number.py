# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Amount.quantifier'
        db.add_column(u'wikipedia_amount', 'quantifier',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='quant_set', null=True, to=orm['wikipedia.Quantifier']),
                      keep_default=False)


        # Changing field 'Amount.number'
        db.alter_column(u'wikipedia_amount', 'number', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Amount.quantifier'
        db.delete_column(u'wikipedia_amount', 'quantifier_id')


        # User chose to not deal with backwards NULL issues for 'Amount.number'
        raise RuntimeError("Cannot reverse this migration. 'Amount.number' and its values cannot be restored.")

    models = {
        u'wikipedia.adjective': {
            'Meta': {'object_name': 'Adjective'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'superlative': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.alias': {
            'Meta': {'object_name': 'Alias'},
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alias_1_set'", 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alias_2_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'wikipedia.amount': {
            'Meta': {'object_name': 'Amount'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'amount_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'quantifier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quant_set'", 'null': 'True', 'to': u"orm['wikipedia.Quantifier']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'unit_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.assertion': {
            'Meta': {'object_name': 'Assertion'},
            'adj2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'adj_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Adjective']"}),
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertion_1_set'", 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assertion_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'context': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assertion_context_set'", 'null': 'True', 'to': u"orm['wikipedia.Context']"}),
            'frequency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Relation']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.category': {
            'Meta': {'object_name': 'Category'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instance_set'", 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.complexverb': {
            'Meta': {'object_name': 'ComplexVerb'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prep2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prep2_set'", 'null': 'True', 'to': u"orm['wikipedia.Preposition']"}),
            'preposition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Preposition']"}),
            'verb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Verb']"})
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
        u'wikipedia.context': {
            'Meta': {'object_name': 'Context'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'context_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'wikipedia.entity': {
            'Meta': {'object_name': 'Entity'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entity_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.group': {
            'Meta': {'object_name': 'Group'},
            'child_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstract_child_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstract_parent_set'", 'to': u"orm['wikipedia.Concept']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.groupinstance': {
            'Meta': {'object_name': 'GroupInstance'},
            'child_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'to': u"orm['wikipedia.Concept']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instance_set'", 'to': u"orm['wikipedia.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_set'", 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.ifstmt': {
            'Meta': {'object_name': 'IfStmt'},
            'assertion1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'if_1_ass_set'", 'null': 'True', 'to': u"orm['wikipedia.Assertion']"}),
            'assertion2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'if_2_ass_set'", 'null': 'True', 'to': u"orm['wikipedia.Assertion']"}),
            'category2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Category']"}),
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
            'last_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'male_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rank': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.prepconstruct': {
            'Meta': {'object_name': 'PrepConstruct'},
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pc_1_set'", 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pc_2_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preposition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Preposition']"})
        },
        u'wikipedia.preposition': {
            'Meta': {'object_name': 'Preposition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.property': {
            'Meta': {'object_name': 'Property'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prop_key_set'", 'to': u"orm['wikipedia.Concept']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prop_parent_set'", 'to': u"orm['wikipedia.Concept']"}),
            'value_amount': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prop_amount_set'", 'null': 'True', 'to': u"orm['wikipedia.Amount']"}),
            'value_concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prop_value_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"})
        },
        u'wikipedia.quantifier': {
            'Meta': {'object_name': 'Quantifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wikipedia.questionfragment': {
            'Meta': {'object_name': 'QuestionFragment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'q_word': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'verb_construct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.VerbConstruct']"})
        },
        u'wikipedia.rank': {
            'Meta': {'object_name': 'Rank'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Concept']", 'null': 'True', 'blank': 'True'}),
            'group_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rank_set'", 'to': u"orm['wikipedia.GroupInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'sws': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.StopwordSequence']", 'null': 'True', 'blank': 'True'})
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
            'participle_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'past_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.verbconstruct': {
            'Meta': {'object_name': 'VerbConstruct'},
            'amount1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'amount_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Amount']"}),
            'amount2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'amount_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Amount']"}),
            'assertion2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vc_adj_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Adjective']"}),
            'complex_verb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.ComplexVerb']", 'null': 'True', 'blank': 'True'}),
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'verb_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'verb_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'context': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'verb_context_set'", 'null': 'True', 'to': u"orm['wikipedia.Context']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_fragment2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'qf_2_set'", 'null': 'True', 'to': u"orm['wikipedia.QuestionFragment']"}),
            'verb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Verb']", 'null': 'True', 'blank': 'True'}),
            'verb_construct2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vc_2_set'", 'null': 'True', 'to': u"orm['wikipedia.VerbConstruct']"})
        }
    }

    complete_apps = ['wikipedia']