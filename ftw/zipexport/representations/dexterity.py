from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.general import NullZipRepresentation
from plone.namedfile.interfaces import INamedBlobFileField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.dexterity.interfaces import IDexterityItem
from zope.component import adapts
from zope.component import getAdapter
from zope.interface import implements
from zope.interface import Interface


class DexterityItemZipRepresentation(NullZipRepresentation):
    implements(IZipRepresentation)
    adapts(IDexterityItem, Interface)

    def get_files(self, path_prefix="", recursive=True, toplevel=True):
        try:
            primary_adapter = getAdapter(self.context,
                                         interface=IPrimaryFieldInfo)
        except TypeError:
            # if no primary field is available PrimaryFieldInfo Adapter throws TypeError
            return

        if INamedBlobFileField.providedBy(primary_adapter.field):
            if primary_adapter.value:
                namedblob = primary_adapter.value
                yield (path_prefix + "/" + namedblob.filename, namedblob.open())
