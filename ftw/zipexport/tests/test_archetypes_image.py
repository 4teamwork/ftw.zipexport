from ftw.builder import Builder
from ftw.builder import create
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from unittest2 import TestCase
from zope.component import getMultiAdapter


class TestArchetypesImageRepresentation(TestCase):
    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        login(self.layer['portal'], TEST_USER_NAME)

    def test_images_have_file_representation(self):
        image = create(Builder('image')
                       .attach_file_containing('The Image', 'img.png'))
        repr = getMultiAdapter((image, self.layer['request']),
                               interface=IZipRepresentation)

        files = [(path, stream.read()) for path, stream in repr.get_files()]
        self.assertEquals([(u'/img.png', 'The Image')], files)
