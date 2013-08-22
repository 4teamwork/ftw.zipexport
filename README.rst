Overview
========

``ftw.zipexport`` provides a generic solution to export data from plone
in a zip archive.

A user can export data with the "Export as Zip" action in document listings.

Install
=======


Compatibility
-------------

Requires python 2.7.4 or higher.

Step-by-Step
------------

- Add ``ftw.zipexport`` to your buildout configuration

::

    [instance]
    eggs =
        ftw.zipexport

- Run buildout

- Install ``ftw.zipexport`` in portal_setup

Implementation
==============

How the file collector and the zip generator work is documented in [interfaces.py](ftw/zipexport/interfaces.py).

The download is placed in [zipexportview.py](ftw/zipexport/zipexportview.py).


TODO
====

* Dexterity support (ZipRepresentation)
* ev. Thread

Links
=====

- Package repository: https://github.com/4teamwork/ftw.zipexport
- Issue tracker: https://github.com/4teamwork/ftw.zipexport/issues

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.zipexport`` is licensed under GNU General Public License, version 2.

.. image:: https://cruel-carlota.pagodabox.com/8b048ecd61dba82375e5662b30e6f0d6
   :alt: githalytics.com
   :target: http://githalytics.com/4teamwork/ftw.zipexport
