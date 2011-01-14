# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction

from board import models
from liuanslagstavlan import api

class Command(BaseCommand):
    args = ''
    help = 'Import data from remote web server.'

    def handle(self, *args, **options):
        valid = True 
        if not valid:
            raise CommandError('invalid config')

        remote_cats = api.Category.objects.all()

        with transaction.commit_on_success():
            old_entries = models.Entry.objects.all()
            print "removing %s old entries" % old_entries.count()
            old_entries.delete()

            old_cats = models.Category.objects.all()
            print "removing %s old categories" % old_cats.count()
            old_cats.delete()

            for remote_cat in remote_cats:
                new_cat, cat_created = models.Category.objects.get_or_create(
                    rid=remote_cat.id,
                    title=remote_cat.title,
                )
                assert cat_created

                for remote_entry in remote_cat.entries:
                    new_entry, entry_created = models.Entry.objects.get_or_create(
                        rid=remote_entry.id,
                        title=remote_entry.title,
                        mail=remote_entry.mail,
                        body=remote_entry.body,
                        submitted=remote_entry.submitted,
                        category=new_cat,
                    )
                    assert entry_created

                print "created category '%s' with %s entries" % (new_cat, new_cat.entry_set.count())
