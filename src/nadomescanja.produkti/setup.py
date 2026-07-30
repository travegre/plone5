# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup


def read(*parts):
    with open(os.path.join(os.path.dirname(__file__), *parts), encoding='utf-8') as handle:
        return handle.read()


tests_require = ['zope.testing']


setup(
    name='nadomescanja.produkti',
    version='1.0',
    description='Plone 5 nadomescanja migration package',
    long_description=read('README.txt'),
    classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    keywords='',
    author='',
    author_email='',
    url='https://github.com/travegre/plone5',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['nadomescanja'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.api',
        'xlwt',
    ],
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    test_suite='nadomescanja.produkti.tests.test_doctest.test_suite',
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
