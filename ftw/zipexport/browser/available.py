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
        reg_proxy = registry.forInterface(IZipExportSettings)
        try:
            interface_class = resolve(reg_proxy.enabled_dotted_name)
        except ImportError:
            return False

        return interface_class and interface_class.providedBy(self.context)
