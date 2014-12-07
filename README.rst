=============
django-report
=============

Django report, Open Mining Server Interface

Django Report provides modular report for Django. It features a unified, familiar API that allows you to plug in different search backends (such as _OpenMining) without having to modify your code.

.. _OpenMining: https://github.com/avelino/mining


Installation
============

Use your favorite Python package manager to install the app from PyPI, e.g.

Example::

    pip install django-report


Configuration
=============

Add django-report To ``INSTALLED_APPS``
---------------------------------------

As with most Django applications, you should add **report** to the
``INSTALLED_APPS`` within your settings file (usually ``settings.py``).

Example::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',

        # Added.
        'report',

        # Then your usual apps...
        'myapp.note',
    ]


Modify Your ``settings.py``
---------------------------

Within your ``settings.py``, you'll need to add a setting to indicate where your
site configuration file will live and which backend to use, as well as other
settings for that backend.

Open Mining
~~~~~~~~~~~

Example::

    REPORT_URL = 'http://127.0.0.1:8888'


Handling Data
=============

Creating ``ReportClass``
------------------------

``ReportClass`` objects are the way django-report determines what data should be
placed in the handles the flow of data in.

This code generally goes in a ``reports.py`` file within the app
it applies to, though that is not required.::

    # -*- coding: utf-8 -*-
    from report.backends.mining import Mining
    from myapp.models import Note
    
    
    class NoteMining(Mining):
        model = Note
    
        def get_queryset(self):
            """Used when the entire index for model is updated."""
            return self.model.objects.all


Build
-----

The final step, now that you have everything setup, is to put your data in
from your database into the report system. django-report ships with a management
command to make this process easy.

Simply run ``./manage.py update_report``. You'll get some totals of how many
models were processed and placed in the report systeam.
