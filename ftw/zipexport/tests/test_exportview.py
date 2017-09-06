from ftw.builder import Builder, create
from ftw.zipexport.interfaces import IZipExportSettings
from ftw.zipexport.testing import FTW_ZIPEXPORT_FUNCTIONAL_TESTING
from ftw.zipexport.zipfilestream import ZipFile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import getUtility
import transaction


class TestExportView(TestCase):
    layer = FTW_ZIPEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.browser = Browser(self.layer['app'])

        self.superfolder = create(Builder("folder")
                            .titled("Superfolder"))

        self.superfile = create(Builder("file")
                            .titled("File")
                            .attach_file_containing("SUPER TESTDATA!!!!",
                                                     "SUPERFILE")
                            .within(self.superfolder))

        self.folder = create(Builder("folder")
                            .titled("Folder")
                            .within(self.superfolder))

        self.folderfile = create(Builder("file")
                            .titled("File")
                            .attach_file_containing(
                                "Testdata for the sake of test the data (and not my grammar).",
                                "testdata.txt")
                            .within(self.folder))

        self.folderfile2 = create(Builder("file")
                            .titled("File")
                            .attach_file_containing(
                                "Some other testdata with testdata in it.",
                                "moretest.data")
                            .within(self.folder))

        self.emptyfolder = create(Builder("folder")
                                  .titled(u"Empty f\xf6lder")
                                  .within(self.superfolder))

        transaction.commit()

    def test_zip_single_file_download(self):
        self.browser.open("%s/zip_export" % self.folderfile.absolute_url())
        zipfile = ZipFile(StringIO(self.browser.contents), 'r')
        self.assertEquals(["testdata.txt"], zipfile.namelist())

    def test_content_disposition_for_non_ascii_characters(self):
        self.browser.open("%s/zip_export" % self.emptyfolder.absolute_url())
        self.assertEquals(
            "attachment; filename*=utf-8''Empty%20f%C3%B6lder.zip",
        self.browser.headers.get('Content-Disposition'))

    def test_zip_multiple_files_in_folder(self):
        self.browser.open("%s/zip_export" % self.folder.absolute_url())
        zipfile = ZipFile(StringIO(self.browser.contents), 'r')
        self.assertEquals(
            ['testdata.txt', 'moretest.data'],
            zipfile.namelist())

    def test_directory_tree_gets_builded_correctly_in_zip(self):
        self.browser.open("%s/zip_export" % self.superfolder.absolute_url())
        zipfile = ZipFile(StringIO(self.browser.contents), 'r')
        self.assertEquals(
            ['SUPERFILE', 'Folder/testdata.txt', 'Folder/moretest.data', u'Empty f\xf6lder/'],
            zipfile.namelist())

    def test_zip_selected_files(self):
        postdata = "zip_selected:method=1&paths:list=%s&paths:list=%s" % (
            '/'.join(self.folderfile.getPhysicalPath()),
            '/'.join(self.folderfile2.getPhysicalPath()))
        self.browser.open(self.superfolder.absolute_url(), postdata)
        zipfile = ZipFile(StringIO(self.browser.contents), 'r')
        self.assertEquals(
            ['testdata.txt', 'moretest.data'],
            zipfile.namelist())

    def test_exclude_empty_folders_if_setting_is_deactivated(self):
        registry = getUtility(IRegistry)
        registry.forInterface(IZipExportSettings).include_empty_folders = False

        transaction.commit()

        self.browser.open("%s/zip_export" % self.superfolder.absolute_url())
        zipfile = ZipFile(StringIO(self.browser.contents), 'r')
        self.assertEquals(
            ['SUPERFILE', 'Folder/testdata.txt', 'Folder/moretest.data'],
            zipfile.namelist())
