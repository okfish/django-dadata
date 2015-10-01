#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import dadata

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = dadata.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-dadata',
    version=version,
    description="""Some django batteries for dadata.ru services""",
    long_description=readme + '\n\n' + history,
    author='Oleg Rybkin aka Fish',
    author_email='okfish@yandex.ru',
    url='https://github.com/okfish/django-dadata',
    packages=[
        'dadata',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-dadata',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
