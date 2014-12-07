#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import json
import inspect
import importlib
import warnings
import requests
from django.core.management.base import BaseCommand
from django.utils.module_loading import module_has_submodule
from django.utils.text import slugify
from django.conf import settings


class Command(BaseCommand):

    help = "Completely rebuilds the report by removing the old data and then updating."

    def collect_report(self):
        indexes = []

        for app in settings.INSTALLED_APPS:
            try:
                mod = importlib.import_module(app)
            except ImportError:
                warnings.warn('Installed app %s is not an importable Python module and will be ignored' % app)
                continue

            try:
                report_module = importlib.import_module("%s.reports" % app)
            except ImportError:
                if module_has_submodule(mod, 'reports'):
                    raise
                continue

            for item_name, item in inspect.getmembers(report_module,
                                                      inspect.isclass):
                if getattr(item, 'get_queryset', None) and item_name != "Mining":
                    indexes.append(item().get_queryset())
                elif getattr(item, 'model', None) and item_name != "Mining":
                    indexes.append(item().model.objects.all())

        return indexes

    def mining_save(self, url, _data, name):
        slug = slugify(name.replace(".", "-").replace(" ", "-").replace("/", "-").replace("@", "-").replace(":", "-"))
        _data["slug"] = slug
        data = json.dumps(_data)
        headers = {'content-type': 'application/json'}

        requests.post(url, data=data, headers=headers)
        requests.put("{0}/{1}".format(url, slug, data=data,
                                      headers=headers))

        return slug

    def handle(self, *args, **options):
        """REPORT_URL = http://127.0.0.1:8888"""
        db = settings.DATABASES['default']
        db_engine = db['ENGINE'].split(".")[-1]
        db['ENGINE'] = db_engine

        if db.get('PASSWORD'):
            db["PASSWORD"] = ":{0}".format(db.get('PASSWORD'))

        if db_engine == "postgresql_psycopg2":
            db['ENGINE'] = "postgresql"
            db['PORT'] = db.get('PORT') or 5432
        elif db_engine == "mysql":
            db['PORT'] = db.get('PORT') or 3306
        elif db_engine == "sqlite3":
            db['ENGINE'] = "sqlite"

        conn_string = u"{0}://{1}{2}@{3}:{4}/{5}".format(
            db['ENGINE'], db['USER'], db['PASSWORD'], db['HOST'], db['PORT'],
            db['NAME'])

        conn_name = u"Django default {0}".format(conn_string)

        conn_slug = self.mining_save(
            "{0}/api/connection".format(settings.REPORT_URL),
            {"name": conn_name, "connection": conn_string},
            conn_name)

        for m in self.collect_report():
            name = u"{0}.{1}".format(m.model.__module__, m.model.__name__)
            data = {"connection": conn_slug,
                    "name": name,
                    "scheduler_status": False,
                    "sql": m.query.__str__(),
                    "type": "relational"}
            print self.mining_save("{0}/api/cube".format(settings.REPORT_URL),
                                   data, name)
