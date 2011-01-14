import datetime
from haystack.indexes import *
from haystack import site
from models import Entry, Category


class EntryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    mail = CharField(model_attr='mail')
    submitted = DateTimeField(model_attr='submitted')
    title = CharField(model_attr='title')
    body = CharField(model_attr='body')

    def get_queryset(self):
        return Entry.objects.all()


site.register(Entry, EntryIndex)
