#!/usr/bin/env python
'''
    Copyright (c) 2016, 2017 Tim Savannah All Rights Reserved.
    This software is licensed under the terms of the Lesser GNU General Public License Version 2.1 (LGPLv2.1)

    You should have received a copy of this with the source distribution as LICENSE,
    otherwise the most up to date license can be found at
    https://github.com/kata198/func_timeout/LICENSE

'''

import os
import sys
from setuptools import setup


if __name__ == '__main__':

    dirName = os.path.dirname(__file__)
    if dirName and os.getcwd() != dirName:
        os.chdir(dirName)

    summary = 'Fork of [func_timeout]. Fixes some Exception issues and creates a new decorator for when you always want to specify a timeout value.'

    try:
        with open('README.rst', 'rt') as f:
            long_description = f.read()
    except Exception as e:
        sys.stderr.write('Error reading from README.rst: %s\n' %(str(e),))
        log_description = summary

    setup(name='func_timeouts',
            version='1.0',
            packages=['func_timeouts'],
            author='Brian Houle',
            author_email='grimzecho@gmail.com',
            maintainer='Brian Houle',
            url='https://github.com/BrianHVB/func_timeouts.git',
            maintainer_email='grimzecho@gmail.com',
            description=summary,
            long_description=long_description,
            license='LGPLv2',
            keywords=['timeout'],
            classifiers=['Development Status :: 5 - Production/Stable',
                         'Programming Language :: Python',
                         'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
                         'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3.4',
                          'Programming Language :: Python :: 3.5',
                          'Programming Language :: Python :: 3.6',
                          'Programming Language :: Python :: 3.7',
                          'Topic :: Software Development :: Libraries :: Python Modules'
            ]
    )



