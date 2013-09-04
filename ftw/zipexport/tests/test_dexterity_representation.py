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
        required=False,
        )

alsoProvides(INoteSchemaPrimary, IDexterityItem)


class IInvitationSchemaNonPrimary(form.Schema):
    pass

alsoProvides(IInvitationSchemaNonPrimary, IDexterityItem)


class NoteBuilder(DexterityBuilder):
    portal_type = 'note'

registry.builder_registry.register('note', NoteBuilder)


class InvitationBuilder(DexterityBuilder):
    portal_type = 'invitation'

registry.builder_registry.register('invitation', InvitationBuilder)


class TestDexterityZipRepresentation(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = self.portal.REQUEST

        # fti
        self.fti_note = DexterityFTI('note')
        self.fti_note.schema = 'ftw.zipexport.tests.test_representation.INoteSchemaPrimary'
        self.portal.portal_types._setObject('note', self.fti_note)

        self.fti_invi = DexterityFTI('invitation')
        self.fti_invi.schema = 'fti.zipexport.tests.test_representation.IInvitationSchemaNonPrimary'
        self.portal.portal_types._setObject('invitation', self.fti_invi)

        # register
        register(self.fti_note)
        register(self.fti_invi)

        # create objects
        self.note = create(Builder("note")
                            .having(blob=NamedBlobFile(data='NoteNoteNote',
                                                        filename=u'note.txt')))

        self.note_without_blob = create(Builder("note"))

        self.invitation = create(Builder("invitation")
                            .with_constraints())

    def test_dexterity_item_gets_omittet_if_no_primary_field_set(self):
        ziprepresentation = getMultiAdapter((self.invitation, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([], files_converted)

    def test_dexterity_item_gets_added_in_representation(self):
        ziprepresentation = getMultiAdapter((self.note, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([("/note.txt", "NoteNoteNote")], files_converted)

    def test_item_gets_omittet_if_no_underlying_file_found(self):
        ziprepresentation = getMultiAdapter((self.note_without_blob, self.request),
                                            interface=IZipRepresentation)
        files = list(ziprepresentation.get_files())
        files_converted = [(path, stream.read()) for path, stream in files]
        self.assertEquals([], files_converted)
