from ftw.zipexport.interfaces import IZipRepresentation
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class NullZipRepresentation(object):
    """
    defualt zip export implementation
    """
    implements(IZipRepresentation)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):
        return []
