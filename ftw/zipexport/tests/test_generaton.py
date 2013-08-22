from ftw.builder import Builder, create
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
from zope.component import getAdapter, getMultiAdapter


class TestZipGeneration(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = portal.REQUEST

        self.folder = create(Builder("folder")
                            .titled("Folder 1"))

        self.folderfile = create(Builder("file")
                            .titled("File")
                            .attach_file_containing("Testdata file in folder",
                                                     "test.txt")
                            .within(self.folder))

        subfolder = create(Builder("folder")
                            .titled("SubFolder")
                            .within(self.folder))

        self.subfolderfile = create(Builder("file")
                                    .titled("SubFolderFile")
                                    .attach_file_containing("Testdata file in subfolder",
                                                             "subtest.txt")
                                    .within(subfolder))

    def test_zip_is_not_empty(self):
        #TODO
        ziprepresentation = getMultiAdapter((self.folder, self.request),
                                            interface=IZipRepresentation)
        with getAdapter(ziprepresentation) as zipgenerator:
            zipgenerator.get_zip()
