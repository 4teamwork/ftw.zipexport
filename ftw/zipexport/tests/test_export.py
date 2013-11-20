from ftw.builder import Builder
from ftw.builder import create
from ftw.zipexport.testing import FTW_ZIPEXPORT_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
from ZPublisher.Iterators import filestream_iterator


class TestExport(TestCase):

    layer = FTW_ZIPEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])

    def test_export_files_with_umlauts_in_title(self):
        folder = create(Builder('folder'))
        subfolder = create(Builder('folder')
                           .titled('f\xc3\xb6lder')
                           .within(folder))

        create(Builder('file')
               .titled('hall\xc3\xb6chen')
               .attach_file_containing('Testdata', 'hall\xc3\xb6chen.pdf')
               .within(subfolder))

        view = folder.restrictedTraverse('zip_export')
        self.assertEquals(filestream_iterator, type(view()))
