from ftw.zipexport.interfaces import IZipExportSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.dottedname.resolve import resolve
from zope.publisher.browser import BrowserView


class ZipExportEnabled(BrowserView):

    def __call__(self):
        return str(self.zipexport_enabled())

    def zipexport_enabled(self):
        """ Checks if context is marked as zip exportable.
        """
        registry = getUtility(IRegistry)
        try:
            reg_proxy = registry.forInterface(IZipExportSettings)
        except KeyError:
            return False

        for dotted_name in reg_proxy.enabled_dotted_names:
            try:
                interface_class = resolve(dotted_name)
            except ImportError:
                continue

            if interface_class and interface_class.providedBy(self.context):
                return True

        return False
