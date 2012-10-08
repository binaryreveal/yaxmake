#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'yaxmake',
    version = '0.1.2',
    description = 'Yet another cross make tool',
    author = 'jIeZHaNG',
    author_email = 'binaryreveal@gmail.com',
    url = 'http://code.google.com/p/yaxmake',
    license = 'BSD',
    packages = find_packages(),
    scripts = ['yaxmake.py',
               'yaxlib/__init__.py',
               'yaxlib/ybuilder.py',
               'yaxlib/ycl.py',
               'yaxlib/yenv.py',
               'yaxlib/ylang.py',
               'yaxlib/ymessage.py',
               'yaxlib/ynode.py',
               'yaxlib/ytarget.py',
               'yaxlib/ytk.py',
               'yaxlib/yver.py']
)


