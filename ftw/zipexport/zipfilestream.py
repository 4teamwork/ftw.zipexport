import zipfile
from tempfile import NamedTemporaryFile


class ZipFile(zipfile.ZipFile):
    """
    Extends the ZipFile library with the option to write file-like objects
    to a zip.
    """

    def writefile(self, fileobj, arctype=None, compress_type=None):
        try:
            # check if fileobj has the attribute name,
            # the file exists and is readable
            with open(fileobj.name):
                pass
            self.write(fileobj.name, arctype, compress_type)
            return
        except (AttributeError, IOError):
            # file-like objects without an underlying physical file like
            # streams are written to a temporary file an then passed to
            # the zipfile library.
            with NamedTemporaryFile(prefix="zipfile_") as tmp_file:
                tmp_file.write(fileobj.read())
                tmp_file.flush()
                self.write(tmp_file.name, arctype, compress_type)
