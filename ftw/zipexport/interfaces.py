from zope import schema
from zope.interface import Interface

class IZipExportSettings(Interface):
    enabled_dotted_name = schema.TextLine(
        title=u"Interface dotted-name on which zipexport is enabled.",
        default=u"Products.CMFCore.interfaces._content.IContentish")


class IZipRepresentation(Interface):
    """ Represents list of files to zip. """

    def get_files(path_prefix='', recursive=True, toplevel=True):
        """
        Returns the files for the zip archive.
        The returned data is a list of tuples. One tuple for every file entry.
        The tuples consist of two values. First a relative path under which the
        file should show up in the zip. Second the data as eather a file or
        a stream.
        """
