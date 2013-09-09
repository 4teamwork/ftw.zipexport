from ftw.zipexport.interfaces import IZipRepresentation
from Products.CMFCore.interfaces import IFolderish
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from Products.ATContentTypes.interfaces.file import IFileContent


class NullZipRepresentation(object):
    """
    defualt zip export implementation
    """
    implements(IZipRepresentation)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_files(self, path_prefix="", recursive=True, toplevel=True):
        return StopIteration


class FolderZipRepresentation(NullZipRepresentation):
    implements(IZipRepresentation)
    adapts(IFolderish, Interface)

    def get_files(self, path_prefix="", recursive=True, toplevel=True):
        if not recursive:
            return

        brains = self.context.getFolderContents()
        content = [brain.getObject() for brain in brains]
        if not toplevel:
            path_prefix += "/" + self.context.title

        for obj in content:
            adapt = getMultiAdapter((obj, self.request),
                                 interface=IZipRepresentation)

            for item in adapt.get_files(path_prefix=path_prefix,
                                    recursive=recursive,
                                    toplevel=False):

                yield item


class FileZipRepresentation(NullZipRepresentation):
    implements(IZipRepresentation)
    adapts(IFileContent, Interface)

    def get_files(self, path_prefix="", recursive=True, toplevel=True):
        yield (path_prefix + "/" + self.context.getFile().getFilename(),
                self.context.getFile().getBlob().open())
