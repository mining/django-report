#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import inspect
import importlib
import warnings
from django.core.management.base import BaseCommand
from django.utils.module_loading import module_has_submodule
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
                if getattr(item, 'get_queryset', None):
                    indexes.append(item().get_queryset())
                elif getattr(item, 'model', None):
                    indexes.append(item().model.objects.all())

        return indexes

    def handle(self, *args, **options):
        for m in self.collect_report():
            print m.query.__str__()
