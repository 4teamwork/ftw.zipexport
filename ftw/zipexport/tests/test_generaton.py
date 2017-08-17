from ftw.builder import Builder, create
from ftw.zipexport.generation import ZipGenerator
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import getMultiAdapter
import os


class TestZipGeneration(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = portal.REQUEST

    def test_zip_is_not_empty(self):
        file = create(Builder("file")
                        .titled("File")
                        .attach_file_containing("Testdata file in subfolder",
                                                 u"subtest.txt"))

        ziprepresentation = getMultiAdapter((file, self.request),
                                            interface=IZipRepresentation)
        with ZipGenerator() as zipgenerator:
            self.assertTrue(zipgenerator.is_empty)

            for file_path, file_pointer in ziprepresentation.get_files():
                zipgenerator.add_file(file_path, file_pointer)

            self.assertFalse(zipgenerator.is_empty)

            generated_zip_pointer = zipgenerator.generate()
            if (not hasattr(generated_zip_pointer, "name")
            or (os.stat(generated_zip_pointer.name).st_size == 0)):
                raise AssertionError()

    def test_add_folder_will_create_a_new_folder(self):
        with ZipGenerator() as zipgenerator:
            zipgenerator.add_folder('Documents')

            self.assertEqual(['Documents/'], zipgenerator.zip_file.namelist())

    def test_generator_raises_exception_when_not_used_as_generator(self):
        zipgenerator = ZipGenerator()
        self.assertRaises(StandardError, zipgenerator.generate)

    def test_generator_raises_exception_when_files_added_after_generate(self):
        file = create(Builder("file")
                        .titled("File")
                        .attach_file_containing("Testdata file in subfolder",
                                                 u"subtest.txt"))
        ziprepresentation = getMultiAdapter((file, self.request),
                                            interface=IZipRepresentation)

        file_rep = ziprepresentation.get_files().next()

        with ZipGenerator() as zipgenerator:
            zipgenerator.add_file(file_rep[0], file_rep[1])

            zipgenerator.generate()

            self.assertRaises(StandardError, zipgenerator.add_file, file_rep)

    def test_generator_creates_unique_file_names(self):
        folder = create(Builder('folder').titled("folder"))
        create(Builder("file")
                        .within(folder)
                        .attach_file_containing("File1", u"file.txt"))
        create(Builder("file")
                        .within(folder)
                        .attach_file_containing("File2", u"file.txt"))
        create(Builder("file")
                        .within(folder)
                        .attach_file_containing("File3", u"file.txt"))

        ziprepresentation = getMultiAdapter((folder, self.request),
                                            interface=IZipRepresentation)

        with ZipGenerator() as zipgenerator:
            for path, pointer in ziprepresentation.get_files():
                zipgenerator.add_file(path, pointer)

            in_zip_file_list = zipgenerator.zip_file.namelist()

            self.assertEquals(
                [u'file.txt', u'file (2).txt', u'file (3).txt'],
                in_zip_file_list)

    def test_filenames_are_normalized(self):
        with ZipGenerator() as zipgenerator:
            zipgenerator.add_file('F\xc3\xbc\xc3\xb6 B\xc3\xa4r.tar.gz', StringIO())
            self.assertItemsEqual(
                [u'Fuo Bar.tar.gz'],
                zipgenerator.zip_file.namelist())

    def test_normalization_can_be_disabled(self):
        with ZipGenerator() as zipgenerator:
            zipgenerator.add_file('(B\xc3\xa4r).txt', StringIO())
            self.assertItemsEqual([u'Bar.txt'], zipgenerator.zip_file.namelist())

        with ZipGenerator(path_normalizer=None) as zipgenerator:
            zipgenerator.add_file('(B\xc3\xa4r).txt', StringIO())
            self.assertItemsEqual([u'(B\xe4r).txt'], zipgenerator.zip_file.namelist())
