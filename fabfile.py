# -*- coding: utf-8 -*-
import os
import sys
import functools

from fabric.api import *
from fabric.contrib import django
from fabric import colors

django_project = 'bboard'
django.project(django_project)
from django.conf import settings

env.hosts = ['localhost']
env.solr_version = '1.3.0'
project_dir = os.path.dirname(os.path.abspath(__file__))
django_dir = os.path.join(project_dir, django_project)


class _msg(object):
    """Decorator for printing a message before and after executing the wrapped
    callable. """

    def __init__(self, pre_msg, post_msg, colored=True):
        self.pre_msg = pre_msg
        self.post_msg = post_msg

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwds):
            if kwds.pop('inner', False): # no colors
                pre_color = post_color = lambda x: x
            else:
                pre_color = colors.magenta
                post_color = colors.green

            puts(pre_color(self.pre_msg))
            ret = f(*args, **kwds)
            puts(post_color(self.post_msg))
            return ret
        return wrapper


@_msg('cleaning up project', 'project cleaned up')
def clean():
    """Remove pyc, swp, and other files like them from project.
    """
    # FIXME: The find command is executed two times for each file ending.

    endings = [
        'pyc',
        'swp',
    ]
    for ending in endings:
        with hide('running', 'stdout'):
            with cd(project_dir):
                find_cmd = "find . -name '*.%s'" % ending
                found = run(find_cmd)
                if found:
                    puts("found %s files, removing..." % ending)
                    run("%s | xargs rm" % find_cmd)


@_msg('installing pip packages', 'packages installed')
def pip():
    with cd(project_dir):
        run('workon bboard && pip -q install -r requirements.txt')


@_msg('installing yum packages', 'packages installed')
def yum():
    with cd(project_dir):
        sudo('yum -q -y shell yum.txt', pty=True)


@_msg('installing dependencies', 'dependencies installed')
def deps():
    """Install dependencies."""
    for dep in [ # the other is important
            yum,
            pip, 
        ]:
        dep(inner=True)


@_msg('initializing database', 'database initialized')
def init_db(drop='no'):
    """Create (or drop and create) role, create database. """
    sys.path.insert(0, project_dir) # XXX: figure out why this is needed

    def yesno(var):
        if var in ['yes', 'no']:
            return var == 'yes'
        return False

    def yn(var):
        var = var.lower()
        if var in ['y', 'n']:
            return var == 'y'
        return False

    drop = yesno(drop)

    username = settings.DATABASE_USER
    password = settings.DATABASE_PASSWORD
    engine = settings.DATABASE_ENGINE
    host = settings.DATABASE_HOST
    db_name = settings.DATABASE_NAME

    supported_engine = 'postgresql_psycopg2'
    if engine != supported_engine:
        abort('engine %r unsupported (must be %r)' % (engine, supported_engine))

    supported_host = 'localhost'
    if host != supported_host:
        abort('host %r unsupported (must be %r)' % (host, supported_host))
    
    if drop:
        sure = yn(prompt('are your sure you want to drop the database? [yN]: '))
        if not sure:
            abort('user aborted')

        run('dropdb -U postgres %s' % db_name)
        run('echo "DROP ROLE %s" | psql -U postgres' % username)

    with hide('running', 'aborts'): # or password will be shown
        run('echo "CREATE ROLE %s PASSWORD \'%s\' CREATEDB INHERIT LOGIN" | psql -v ON_ERROR_STOP=1 -U postgres' % (
            username,
            password,
        ))

    run('createdb %s' % db_name)

    with cd(django_dir):
        run('workon bboard && ./manage.py syncdb --noinput')

    migrate(inner=True)


@_msg('migrating database', 'database migrated')
def migrate():
    with cd(django_dir):
        run('workon bboard && ./manage.py migrate --noinput')


@_msg('updating i18n/l10n info', 'done updating i18n/l10n info')
def update_locale():
    with cd(django_dir):
        run('workon bboard && ./manage.py makemessages -a')


@_msg('compiling i18n/l10n', 'done compiling i18n/l10n')
def locale():
    """Compile i18n and l10n resources."""
    with cd(django_dir):
        run('workon bboard && ./manage.py compilemessages')


@_msg('building static files', 'done building static files')
def static():
    """Build static files."""
    with cd(django_dir):
        run('workon bboard && ./manage.py collectstatic --noinput')


@_msg('freshening resources', 'done freshening resources')
def freshen():
    locale(inner=True)
    static(inner=True)


@_msg('downloading and install Solr', 'finished installing Solr')
def setup_solr():
    version = env.solr_version
    with cd(project_dir):
        run('curl -O http://apache.mirrors.tds.net/lucene/solr/1.3.0/apache-solr-%s.tgz' % version)
        run('tar xzf apache-solr-%s.tgz' % version)


@_msg('sync with remote', 'finished syncing with remote')
def sync_remote():
    version = env.solr_version
    with cd(django_dir):
        run('workon bboard && python manage.py syncremote')


@_msg('reschema Solr', 'finished reschema Solr')
def reschema_solr():
    version = env.solr_version
    with cd(django_dir):
        run('workon bboard && python manage.py build_solr_schema > %s/apache-solr-%s/example/solr/conf/schema.xml' % (
            project_dir, 
            version,
        ))


@_msg('reindexing Solr', 'finished reindexing Solr')
def reindex_solr():
    version = env.solr_version
    with cd(django_dir):
        run('workon bboard && python manage.py rebuild_index --noinput')


def run_solr():
    version = env.solr_version
    with cd("%s/apache-solr-%s/example" % (project_dir, version)):
        run('java -jar start.jar')
