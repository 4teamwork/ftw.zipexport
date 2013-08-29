from plone.namedfile import field
from plone.namedfile.file import NamedBlobFile
from plone.directives import form
from zope.interface import alsoProvides
from plone.dexterity.interfaces import IDexterityItem
from ftw.builder import Builder, create
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from ftw.zipexport.interfaces import IZipRepresentation
from unittest2 import TestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from ftw.builder.dexterity import DexterityBuilder
from plone.dexterity.fti import DexterityFTI
from ftw.builder import registry
from plone.dexterity.fti import register


class INoteSchemaPrimary(form.Schema):
    form.primary('blob')
    blob = field.NamedBlobFile(
        title=u'afile',
        required=True,
        )

alsoProvides(INoteSchemaPrimary, IDexterityItem)


class INoteSchemaNonPrimary(form.Schema):
    blob = field.NamedBlobFile(
        title=u'afile',
        required=True,
        )

alsoProvides(INoteSchemaNonPrimary, IDexterityItem)


class NoteBuilder(DexterityBuilder):
    portal_type = 'note'

registry.builder_registry.register('note', NoteBuilder)


class TestDexterityZipRepresentation(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = self.portal.REQUEST

        # fti
        self.fti = DexterityFTI('note')
        self.fti.schema = 'ftw.zipexport.tests.test_representation.INoteSchemaNonPrimary'
        self.portal.portal_types._setObject('note', self.fti)

        # register
        register(self.fti)

    def test_dexterity_item_gets_omittet_if_no_primary_field_set(self):

        # create objects
        self.note = create(Builder("note")
                            .with_constraints()
                            .having(blob=NamedBlobFile(data='NoteNoteNote',
                                                        filename=u'note.txt')))

        ziprepresentation = getMultiAdapter((self.note, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([], files_converted)

    def test_dexterity_item_gets_added_in_representation(self):
        self.portal.portal_types.get('note').schema = 'ftw.zipexport.tests.test_representation.INoteSchemaPrimary'

        # create objects
        self.note = create(Builder("note")
                            .with_constraints()
                            .having(blob=NamedBlobFile(data='NoteNoteNote',
                                                        filename=u'note.txt')))

        ziprepresentation = getMultiAdapter((self.note, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([("/note.txt", "NoteNoteNote")], files_converted)
