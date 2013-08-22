from zope.interface import Interface


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


class IZipGenerator(Interface):
    """ Generates a zip based on the data received from IZipRepresentation. """

    def get_zip():
        """
        Returns a filepointer to the generated zip.
        Have to be used as a context manager as the enter and exit functions
        handle the temporary file.
        If large or many files are selected this function might take some time
        to execute.
        """
