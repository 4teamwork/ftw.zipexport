from zope import schema
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface


class IZipExportSettings(Interface):
    enabled_dotted_names = schema.List(
        title=u"Interface dotted-names on which zipexport is enabled.",
        default=[u"Products.CMFCore.interfaces._content.IContentish"],
        value_type=schema.TextLine())

    include_empty_folders = schema.Bool(
        title=u"Include empty folders in zipexport.",
        description=u"Defines if empty folders should be included in the export or not",
        default=True)


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


class IContainerZippedEvent(IObjectEvent):
    pass


class IItemZippedEvent(IObjectEvent):
    pass
