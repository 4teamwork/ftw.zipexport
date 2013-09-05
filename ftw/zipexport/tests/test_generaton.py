from ftw.builder import Builder, create
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
from zope.component import getMultiAdapter
from ftw.zipexport.generation import ZipGenerator
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
                                                     "subtest.txt"))

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

    def test_generator_raises_exception_when_not_used_as_generator(self):
        zipgenerator = ZipGenerator()
        self.assertRaises(StandardError, zipgenerator.generate)

    def test_generator_raises_exception_when_files_added_after_generate(self):
        file = create(Builder("file")
                            .titled("File")
                            .attach_file_containing("Testdata file in subfolder",
                                                     "subtest.txt"))
        ziprepresentation = getMultiAdapter((file, self.request),
                                            interface=IZipRepresentation)

        file_rep = ziprepresentation.get_files().next()

        with ZipGenerator() as zipgenerator:
            zipgenerator.add_file(file_rep[0], file_rep[1])

            zipgenerator.generate()

            self.assertRaises(StandardError, zipgenerator.add_file, file_rep)
