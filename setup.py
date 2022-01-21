#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (3, 0):
    sys.exit("Python 2.x is not supported; Python 3.x is required.")

setup(
    name='yahoo_quote_download',
    version='0.1',
    description='Yahoo Quote Downloader',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daniel Lenski',
    author_email='dlenski@gmail.com',
    packages=['yahoo_quote_download'],
    install_requires=open('requirements.txt').readlines(),
    entry_points = {
    	'console_scripts': [ 'yqd=yahoo_quote_download.__main__:main' ],
    },
    license="Simplified BSD License",
)
