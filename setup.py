#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='gitcoach',
    version='0.2.2',
    description='Help you find out what files you should be changing.',
    long_description=readme + '\n\n' + history,
    author='Mike Hoye',
    author_email='mhoye@mozilla.com',
    url='https://github.com/mhoye/gitcoach',
    packages=[
        'gitcoach',
    ],
    package_dir={'gitcoach': 'gitcoach'},
    entry_points={'console_scripts': ['gitlearn = gitcoach.commands:learn', 'gitcoach = gitcoach.commands:coach']},
    include_package_data=True,
    install_requires=[
        'git2json',
        'clint',
    ],
    license="BSD",
    zip_safe=False,
    keywords='gitcoach',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
