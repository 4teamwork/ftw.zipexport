from tempfile import NamedTemporaryFile
import os
import zipfile


class ZipFile(zipfile.ZipFile):
    """
    Extends the ZipFile library with the option to write file-like objects
    to a zip.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def writefile(self, fileobj, arctype=None, compress_type=None):
        # check if fileobj has the attribute name,
        # the file exists and is readable
        if hasattr(fileobj, 'name') and os.access(fileobj.name, os.R_OK):
            self.write(fileobj.name, arctype, compress_type)
            return

        # file-like objects without an underlying physical file like
        # streams are written to a temporary file an then passed to
        # the zipfile library.
        else:
            with NamedTemporaryFile(prefix="zipfile_") as tmp_file:
                tmp_file.write(fileobj.read())
                tmp_file.flush()
                self.write(tmp_file.name, arctype, compress_type)
