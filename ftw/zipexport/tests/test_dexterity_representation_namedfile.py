from ftw.builder import Builder, create
from ftw.builder import registry
from ftw.builder.dexterity import DexterityBuilder
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations import dexterity as ftwdexterity
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from ftw.zipexport.tests import dottedname
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.fti import register
from plone.dexterity.interfaces import IDexterityItem
from plone.directives import form
from plone.namedfile import field
from plone.namedfile.file import NamedFile
from plone.rfc822.interfaces import IPrimaryField
from Products.CMFPlone.utils import getFSVersionTuple
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class INamedFileSchema(form.Schema):
    form.primary('named_file')
    named_file = field.NamedFile(
        title=u'namedfile',
        required=False,
        )
alsoProvides(INamedFileSchema, IDexterityItem)


if getFSVersionTuple() < (4, 3):
    # Marshalling was not triggered in Plone 4.2 without grokking.
    alsoProvides(INamedFileSchema['named_file'], IPrimaryField)


class NamedFileBuilder(DexterityBuilder):
    portal_type = 'namedfile'
registry.builder_registry.register('namedfile', NamedFileBuilder)


class TestDexterityRepresentationNamedfile(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = self.portal.REQUEST

        # fti
        self.fti_namedfile = DexterityFTI('namedfile')
        self.fti_namedfile.schema = dottedname(INamedFileSchema)
        self.portal.portal_types._setObject('namedfile', self.fti_namedfile)
        register(self.fti_namedfile)

        self.store_have_blobs = ftwdexterity.HAVE_BLOBS

    def tearDown(self):
        ftwdexterity.HAVE_BLOBS = self.store_have_blobs

    def test_namedfile_is_handeled_correctly_even_when_blobs_are_enabled(self):
        ftwdexterity.HAVE_BLOBS = True

        namedfile = create(Builder("namedfile")
                           .having(named_file=NamedFile(data='NamedFile',
                                                filename=u'h\xc3\xb6lla.txt')))

        ziprepresentation = getMultiAdapter((namedfile, self.request),
                                              interface=IZipRepresentation)

        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([(u'/h\xc3\xb6lla.txt', "NamedFile")], files_converted)

    def test_dexterity_handles_non_blob_files_and_returns_tuple(self):
        ftwdexterity.HAVE_BLOBS = False

        namedfile = create(Builder("namedfile")
                           .having(named_file=NamedFile(data='NamedFile',
                                                filename=u'h\xc3\xb6lla.txt')))

        ziprepresentation = getMultiAdapter((namedfile, self.request),
                                            interface=IZipRepresentation)

        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([(u'/h\xc3\xb6lla.txt', "NamedFile")], files_converted)
