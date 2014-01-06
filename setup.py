#!/usr/bin/env python

from distutils.core import setup
import os

scriptdir = 'src/bin'

setup(
    name='iona',
    version='0.1',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    url='http://abagofapples.com/',
    package_dir={'': 'src'},
    packages=['iona'],
    scripts=[os.path.join(scriptdir, x) for x in os.listdir(scriptdir)],
)
