from ftw.builder import Builder, create
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
from zope.component import getMultiAdapter


class TestArchetypeZipRepresentation(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = portal.REQUEST

        self.folder = create(Builder("folder")
                            .titled(u"Folder\xe3\x82\xb9"))

        self.folderfile = create(Builder("file")
                            .titled(u"File")
                            .attach_file_containing("Testdata file in folder",
                                                    u"test.txt")
                            .within(self.folder))

        subfolder = create(Builder("folder")
                            .titled(u"SubF\xc3\xb6lder")
                            .within(self.folder))

        self.subfolderfile = create(Builder("file")
                                    .titled(u"SubF\xc3\xb6lderFile")
                                    .attach_file_containing("Testdata file in subfolder",
                                                            u"s\xc3\xb6btest.txt")
                                    .within(subfolder))

        self.prefixfolder = create(Builder('folder').titled(u'Folder\xe3\x82\xb9'))
        self.prefixsubfolder = create(Builder('folder').titled(u'Folder\xe3\x82\xb9').within(self.prefixfolder))
        self.prefixsubfolder.zipexport_title = u'Prefix Folder\xe3\x82\xb9'

    def test_folder_representation_non_recursive_is_empty(self):
        self.assertEquals([], list(getMultiAdapter((self.folder, self.request),
                                             interface=IZipRepresentation)
                                             .get_files(recursive=False)))

    def test_folder_contains_files_in_recursive(self):
        ziprepresentation = getMultiAdapter((self.folder, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files(recursive=True))
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([(u"/test.txt", "Testdata file in folder"),
                            (u"/SubF\xc3\xb6lder/s\xc3\xb6btest.txt", "Testdata file in subfolder")],
                            files_converted)

    def test_file_represents_itself(self):
        ziprepresentation = getMultiAdapter((self.folderfile, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([(u"/test.txt", "Testdata file in folder")],
                            files_converted)

    def test_folder_prefixes(self):
        ziprepresentation = getMultiAdapter((self.prefixfolder, self.request), interface=IZipRepresentation)
        paths = [path_file[0] for path_file in ziprepresentation.get_files()]
        expected_paths = [u'/Prefix Folder\xe3\x82\xb9']
        self.assertEqual(paths, expected_paths)
