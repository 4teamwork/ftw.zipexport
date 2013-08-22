import os
from setuptools import setup, find_packages

version = '1.0.0'

maintainer = 'Lukas Knoepfel'

tests_require = [
    'ftw.builder',
    'plone.app.testing'
    ]
    
extras_require = {
    'tests': tests_require,
    }

import sys
if sys.version_info < (2, 7, 4):
    raise Exception("Zipexport requires at least python 2.7.4.")

setup(name='ftw.zipexport',
      version=version,
      description="Zip export for Plone",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      keywords='ftw zip export',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.zipexport',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Plone',
        'setuptools',
        # -*- Extra requirements: -*-
        ],
      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
