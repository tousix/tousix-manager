#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TouSIX-Manager is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='TouSIX-Manager',
    version='0.7',
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPL v3',
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='http://touix.net/',
    author='Rémy Lapeyrade',
    author_email='rlapeyra@laas.fr',
    install_requires=[
        'django >= 1.9, < 1.10',
        'django-bootstrap3==6.2.2',
        'django-debug-toolbar==1.4',
        'django-formtools',
        'django-fsm',
        'django-localflavor',
        'django-sb-admin',
        'django-fsm-admin==1.2.2',
        'django-registration-redux >= 1.3',
        'django-reversion',
        'mysqlclient',
        'influxdb',
        'pygments',
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)