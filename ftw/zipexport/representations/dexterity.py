from ftw.zipexport.events import ItemZippedEvent
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.general import NullZipRepresentation
from plone.dexterity.interfaces import IDexterityItem
from plone.namedfile.interfaces import INamedFileField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from Products.CMFPlone.utils import safe_unicode
from StringIO import StringIO
from zope.component import adapts
from zope.component import getAdapter
from zope.event import notify
from zope.interface import implements
from zope.interface import Interface

from plone.namedfile.interfaces import HAVE_BLOBS
if HAVE_BLOBS:
    from plone.namedfile.interfaces import INamedBlobFile


class DexterityItemZipRepresentation(NullZipRepresentation):
    implements(IZipRepresentation)
    adapts(IDexterityItem, Interface)

    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):
        try:
            primary_adapter = getAdapter(self.context,
                                         interface=IPrimaryFieldInfo)
        except TypeError:
            # if no primary field is available PrimaryFieldInfo
            # Adapter throws TypeError
            return

        if INamedFileField.providedBy(primary_adapter.field):
            named_file = primary_adapter.value
            if primary_adapter.value:
                notify(ItemZippedEvent(self.context))
                yield self.get_file_tuple(named_file, path_prefix)

    def get_file_tuple(self, named_file, path_prefix):
        path = u'{0}/{1}'.format(safe_unicode(path_prefix),
                                 safe_unicode(named_file.filename))
        if HAVE_BLOBS and INamedBlobFile.providedBy(named_file):
            return (path, named_file.open())
        else:
            stream_data = StringIO(named_file.data)
            return (path, stream_data)
