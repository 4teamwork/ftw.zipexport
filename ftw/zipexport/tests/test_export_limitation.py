from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from ftw.builder import Builder, create
from ftw.zipexport.testing import FTW_ZIPEXPORT_FUNCTIONAL_TESTING
from unittest2 import TestCase
from plone.registry.interfaces import IRegistry
from ftw.zipexport.interfaces import IZipExportSettings
from zope.component import getUtility
from plone.testing.z2 import Browser


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
        export = self.file.restrictedTraverse("@@zipexport-enabled")
        self.assertTrue(export.zipexport_enabled())

    def test_export_is_disabled_when_non_existent_interface_is_configured(self):
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(IZipExportSettings)
        reg_proxy.enabled_dotted_name = u"some.other.interface"

        export = self.file.restrictedTraverse("@@zipexport-enabled")

        self.assertFalse(export.zipexport_enabled())

    def test_export_is_disabled_when_unprovided_interface_is_configured(self):
        registry = getUtility(IRegistry)
        reg_proxy = registry.forInterface(IZipExportSettings)
        reg_proxy.enabled_dotted_name = u"OFS.interfaces.IFolder"

        export = self.file.restrictedTraverse("@@zipexport-enabled")

        self.assertFalse(export.zipexport_enabled())
