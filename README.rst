Overview
========

``ftw.zipexport`` provides a generic solution to export data from plone
in a zip archive.

A user can export data with the "Export as Zip" action in document listings.

Install
=======


Compatibility
-------------

For zipping files with a total size of over 4Gb python 2.7.4 is required.

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

In a first step we have to collect all data to zip.
Use the IZipRepresentation interface for this task.

The get_files function returns a list of tuples. The tuples consist of two values.
First a relative path under which the file should show up in the zip.
Second the data as eather a file or a stream.

.. code:: python

	class IZipRepresentation(Interface):

	    def get_files(path_prefix='', recursive=True, toplevel=True):

By default we support basic data-types like folder and files.
More complex data-types require an own adapter for IZipRepresentation.

Feel free to extend one of the predefined adapters:
`Predefined representations <https://github.com/4teamwork/ftw.zipexport/tree/master/ftw/zipexport/representations>`_

The data generated by our IZipRepresentation then gets delivered to the ZipGeneration helper class.

.. code:: python

	class ZipGenerator(object):
		def add_file(file_path, file_pointer):
			Zipps the file and adds it to the archive.
			If large or many files are selected this function might take some time to execute.

		def generate():
			returns a temp file holding the generated zip

Here is the sample code of the described steps:

.. code:: python

	from zope.component import getMultiAdapter
	from ftw.zipexport.generation import ZipGenerator
	from ftw.zipexport.interfaces import IZipRepresentation

	ziprepresentation = getMultiAdapter((self.folder, self.request), interface=IZipRepresentation)
	with ZipGenerator() as zipgenerator:
		for file_path, file_pointer in ziprepresentation.get_files():
			zipgenerator.add_file(file_path, file_pointer)
		generated_zip_pointer = zipgenerator.generate()


The download is handled in a standard BrowserView which plainly reads from the temp file.
For details check out the code:
`zipexportview.py <https://github.com/4teamwork/ftw.zipexport/blob/master/ftw/zipexport/zipexportview.py>`_.

Current supported data-types
----------------------------

* IFolderish
* IFileContent
* IDexterityItem with IPrimaryFieldInfo

Path Normalization
------------------

Paths are automatically using Plone's ``IFileNameNormalizer``.
If you want to use a custom normalization, you  can pass it to the ``ZipGenerator``:

.. code:: python

    from ftw.zipexport.generation import ZipGenerator
    from Products.CMFPlone.utils import safe_unicode
    import re

    def normalize_path(path):
        path = safe_unicode(path).replace(u'\\', u'/')
        return re.sub(ur'[^\w\-.\/]', u'', path)

    with ZipGenerator(path_normalizer=normalize_path) as zipgenerator:
        ...

Pass ``None`` to disable normalization completely:

.. code:: python

    from ftw.zipexport.generation import ZipGenerator

    with ZipGenerator(path_normalizer=None) as zipgenerator:
        ...




Nice to have
============

* Multithreading

Links
=====

- Github: https://github.com/4teamwork/ftw.zipexport
- Issues: https://github.com/4teamwork/ftw.zipexport/issues
- Continuous integration: https://jenkins.4teamwork.ch/view/All/search/?q=ftw.zipexport

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.zipexport`` is licensed under GNU General Public License, version 2.
