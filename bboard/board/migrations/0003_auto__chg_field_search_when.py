# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Search.when'
        db.alter_column('board_search', 'when', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))


    def backwards(self, orm):
        
        # Changing field 'Search.when'
        db.alter_column('board_search', 'when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))


    models = {
        'board.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'board.entry': {
            'Meta': {'object_name': 'Entry'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'rid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'board.search': {
            'Meta': {'object_name': 'Search'},
            'hit_count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['board']
