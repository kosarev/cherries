#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='cherries',
    version='1.0a0',
    packages=[],
    scripts=['cherries/__init__.py',
             'cherries/range_set.py'],
    description='Library of Python utilities',
    author='Ivan Kosarev',
    author_email='ivan@kosarev.info',
    license='MIT',
    keywords='utilities rangeset range_set',
    url='https://github.com/kosarev/cherries',
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
