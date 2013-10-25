# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Negation'
        db.create_table(u'wikipedia_negation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('verb_construct', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wikipedia.VerbConstruct'], null=True, blank=True)),
            ('prep_construct', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wikipedia.PrepConstruct'], null=True, blank=True)),
            ('assertion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wikipedia.Assertion'], null=True, blank=True)),
        ))
        db.send_create_signal(u'wikipedia', ['Negation'])


    def backwards(self, orm):
        # Deleting model 'Negation'
        db.delete_table(u'wikipedia_negation')


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
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assertion_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'context': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assertion_context_set'", 'null': 'True', 'to': u"orm['wikipedia.Context']"}),
            'frequency': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'property1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ass_prop_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Property']"}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Relation']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.assertionvalue': {
            'Meta': {'object_name': 'AssertionValue'},
            'adj': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ass_adj_value_set'", 'null': 'True', 'to': u"orm['wikipedia.Adjective']"}),
            'assertions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ass_value_set'", 'symmetrical': 'False', 'to': u"orm['wikipedia.Assertion']"}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ass_c_value_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
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
            'parent_concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'abstract_parent_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'parent_property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Property']", 'null': 'True', 'blank': 'True'}),
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
        u'wikipedia.name': {
            'Meta': {'object_name': 'Name'},
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_c_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_e_set'", 'null': 'True', 'to': u"orm['wikipedia.Entity']"}),
            'group_instance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_gi_set'", 'null': 'True', 'to': u"orm['wikipedia.GroupInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prep_construct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_pc_set'", 'null': 'True', 'to': u"orm['wikipedia.PrepConstruct']"}),
            'verb_construct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_vc_set'", 'null': 'True', 'to': u"orm['wikipedia.VerbConstruct']"})
        },
        u'wikipedia.negation': {
            'Meta': {'object_name': 'Negation'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Assertion']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prep_construct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.PrepConstruct']", 'null': 'True', 'blank': 'True'}),
            'verb_construct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.VerbConstruct']", 'null': 'True', 'blank': 'True'})
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
            'concept1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pc_c_1_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            'concept2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pc_2_set'", 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preposition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Preposition']"}),
            'vc1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pc_vc_1_set'", 'null': 'True', 'to': u"orm['wikipedia.VerbConstruct']"})
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
            'sub_prop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Property']", 'null': 'True', 'blank': 'True'})
        },
        u'wikipedia.propertyvalue': {
            'Meta': {'object_name': 'PropertyValue'},
            'amount': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prop_amount_set'", 'null': 'True', 'to': u"orm['wikipedia.Amount']"}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prop_value_c_set'", 'null': 'True', 'to': u"orm['wikipedia.Concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'props': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pv_set'", 'symmetrical': 'False', 'to': u"orm['wikipedia.Property']"}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'past_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            's_form': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            'property2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vc_prop_2_set'", 'null': 'True', 'to': u"orm['wikipedia.Property']"}),
            'quantifier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vc_quant_set'", 'null': 'True', 'to': u"orm['wikipedia.Quantifier']"}),
            'question_fragment2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'qf_2_set'", 'null': 'True', 'to': u"orm['wikipedia.QuestionFragment']"}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'verb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wikipedia.Verb']", 'null': 'True', 'blank': 'True'}),
            'verb_construct2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vc_2_set'", 'null': 'True', 'to': u"orm['wikipedia.VerbConstruct']"})
        }
    }

    complete_apps = ['wikipedia']