from ftw.builder import Builder
from ftw.builder import create
from ftw.builder import registry
from ftw.builder.dexterity import DexterityBuilder
from ftw.zipexport.events import ContainerZippedEvent
from ftw.zipexport.events import ItemZippedEvent
from ftw.zipexport.interfaces import IContainerZippedEvent
from ftw.zipexport.interfaces import IItemZippedEvent
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.testing import FTW_ZIPEXPORT_FUNCTIONAL_TESTING
from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from ftw.zipexport.tests import dottedname
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.fti import register
from plone.dexterity.interfaces import IDexterityItem
from plone.directives import form
from plone.namedfile import field
from plone.namedfile.file import NamedBlobFile
from plone.rfc822.interfaces import IPrimaryField
from plone.testing.z2 import Browser
from Products.CMFPlone.utils import getFSVersionTuple
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.component import provideHandler
from zope.interface import alsoProvides
import transaction


class TestArchetypeEvents(TestCase):
    layer = FTW_ZIPEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])
        self.browser = Browser(self.layer['app'])

        self.superfolder = create(
            Builder("folder")
            .titled("Superfolder")
            )

        self.folder = create(
            Builder("folder")
            .titled("Folder")
            .within(self.superfolder)
            )

        self.folderfile = create(
            Builder("file")
            .titled("File")
            .attach_file_containing(
                "Testdata for the sake of test the data (and not my grammar).",
                "testdata.txt")
            .within(self.folder)
            )

        transaction.commit()

        class MockEvent(object):
            # History: [[interface, context], ]
            event_history = []

            def mock_handler(self, event):
                self.event_history.append(event, )

            def last_event(self):
                return self.event_history[-1]

        self.mock_event = MockEvent()

    def test_archetype_item_event(self):
        provideHandler(
            factory=self.mock_event.mock_handler,
            adapts=[IItemZippedEvent, ], )

        self.browser.open("%s/zip_export" % self.folderfile.absolute_url())

        self.assertEquals(1, len(self.mock_event.event_history))

        self.assertIsInstance(self.mock_event.event_history[0],
                              ItemZippedEvent)

        self.assertEquals('file', self.mock_event.event_history[0].object.id)

    # This also tests the code path for dexterity containers as this action
    # is always fired from a container and that is what gets caught
    def test_container_event(self):
        provideHandler(
            factory=self.mock_event.mock_handler,
            adapts=[IContainerZippedEvent, ], )

        provideHandler(
            factory=self.mock_event.mock_handler,
            adapts=[IItemZippedEvent, ], )

        self.browser.open("%s/zip_export" % self.superfolder.absolute_url())

        self.assertEqual(2, len(self.mock_event.event_history))

        self.assertIsInstance(self.mock_event.event_history[0],
                              ItemZippedEvent)

        self.assertEquals('file', self.mock_event.event_history[0].object.id)

        self.assertIsInstance(self.mock_event.event_history[1],
                              ContainerZippedEvent)

        self.assertEquals('superfolder',
                          self.mock_event.event_history[1].object.id)


class INoteSchemaPrimary(form.Schema):
    form.primary('blob')
    blob = field.NamedBlobFile(
        title=u'blobfile',
        required=False,
        )


alsoProvides(INoteSchemaPrimary, IDexterityItem)


if getFSVersionTuple() < (4, 3):
    # Marshalling was not triggered in Plone 4.2 without grokking.
    alsoProvides(INoteSchemaPrimary['blob'], IPrimaryField)


class EventNoteBuilder(DexterityBuilder):
    portal_type = 'event_note'


registry.builder_registry.register('event_note', EventNoteBuilder)


class TestDexterityEvents(TestCase):

    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.request = self.portal.REQUEST

        # fti
        self.fti_note = DexterityFTI('event_note')
        self.fti_note.schema = dottedname(INoteSchemaPrimary)
        self.portal.portal_types._setObject('event_note', self.fti_note)

        # register
        register(self.fti_note)

        class MockEvent(object):
            # History: [[interface, context], ]
            event_history = []

            def mock_handler(self, event):
                self.event_history.append(event, )

            def last_event(self):
                return self.event_history[-1]

        self.mock_event = MockEvent()

    def test_dexterity_item_event(self):
        provideHandler(
            factory=self.mock_event.mock_handler,
            adapts=[IItemZippedEvent, ], )

        note = create(
            Builder("event_note")
            .having(blob=NamedBlobFile(data='NoteNoteNote',
                                       filename=u'note.txt')
                    )
            )

        # Force the generator to fire, the events live there
        list(getMultiAdapter((note, self.request),
                             interface=IZipRepresentation).get_files())

        self.assertEquals(1, len(self.mock_event.event_history))

        self.assertIsInstance(self.mock_event.event_history[0],
                              ItemZippedEvent)

        self.assertEquals('event_note',
                          self.mock_event.event_history[0].object.id)
