#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup


setup(
    name='django-report',
    version='0.1',
    description='Pluggable model report for Django.',
    author='Thiago Avelino',
    author_email='thiago@avelino.xxx',
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/mining/django-report/',
    packages=[
        'report',
        'report.backends',
        'report.management',
        'report.management.commands'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'],
    zip_safe=False,
    install_requires=['Django'],
)
