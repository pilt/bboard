# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('board_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Category'])),
        ))
        db.send_create_signal('board', ['Entry'])

        # Adding model 'Category'
        db.create_table('board_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('board', ['Category'])


    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('board_entry')

        # Deleting model 'Category'
        db.delete_table('board_category')


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
        }
    }

    complete_apps = ['board']
