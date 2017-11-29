from ftw.builder import Builder, create
from ftw.zipexport.interfaces import IZipExportSettings
from ftw.zipexport.testing import FTW_ZIPEXPORT_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from unittest2 import TestCase
from zExceptions import NotFound
from zope.component import getUtility
from ZPublisher.Iterators import filestream_iterator


class TestExportView(TestCase):
    layer = FTW_ZIPEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Reviewer', 'Manager'])

        self.browser = Browser(self.layer['app'])

        self.file = create(Builder("file")
                           .titled("File")
                           .attach_file_containing(
                               "Testdata.",
                               "testdata.txt"))

    def test_export_is_enabled_by_default(self):
        enabled_view = self.file.restrictedTraverse("@@zipexport-enabled")
        self.assertTrue(enabled_view.zipexport_enabled())

        export_view = self.file.restrictedTraverse("zip_export")
        self.assertIsInstance(export_view(),
                              filestream_iterator)

    def test_export_is_disabled_when_non_existent_interface_is_configured(self):
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(IZipExportSettings)
        reg_proxy.enabled_dotted_names = [u"some.non.existent.interface"]

        enabled_view = self.file.restrictedTraverse("@@zipexport-enabled")

        self.assertFalse(enabled_view.zipexport_enabled())

    def test_export_is_disabled_when_unprovided_interface_is_configured(self):
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(IZipExportSettings)
        reg_proxy.enabled_dotted_names = [u"OFS.interfaces.IFolder"]

        enabled_view = self.file.restrictedTraverse("@@zipexport-enabled")
        self.assertFalse(enabled_view.zipexport_enabled())

        export_view = self.file.restrictedTraverse("zip_export")
        self.assertRaises(NotFound, export_view)

        # selected view does not check if the zip export is enabled on
        # current context
        zip_selected_view = self.file.restrictedTraverse("zip_selected")
        zip_selected_view()

    def test_export_with_multiple_configured_interfaces(self):
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(IZipExportSettings)
        reg_proxy.enabled_dotted_names = [
            u"OFS.interfaces.IFolder",
            u"Products.ATContentTypes.interfaces.file.IATFile"]

        export = self.file.restrictedTraverse("@@zipexport-enabled")

        self.assertTrue(export.zipexport_enabled())

    def test_export_with_multiple_and_nonexistent_interfaces(self):
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(IZipExportSettings)
        reg_proxy.enabled_dotted_names = [
            u"some.non.existent.interface",
            u"Products.ATContentTypes.interfaces.file.IATFile"]

        export = self.file.restrictedTraverse("@@zipexport-enabled")

        self.assertTrue(export.zipexport_enabled())
