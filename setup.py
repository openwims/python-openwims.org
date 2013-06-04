#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'A simple module designed to produce Weak Inferred Meanings (WIMs).',
    'author': 'Benjamin Bengfort, Jesse English',
    'url': 'https://github.com/bbengfort/wim',
    'author_email': 'benjamin@bengfort.com',
    'version': '1.0',
    'install_requires': ['nose', 'nltk'],
    'packages:': ['wim'],
    'scripts': ['bin/wimify.py', ],
    'name': 'WIM Analyzer'
}

setup(**config)
