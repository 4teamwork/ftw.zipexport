from tempfile import NamedTemporaryFile
from ftw.zipexport.zipfilestream import ZipFile


class ZipGenerator(object):
    """
    Generates the zip. Acts as context manager to ensure that all temporary
    files are deleted after usage.
    """

    def __init__(self):
        self.empty = True

    def __enter__(self):
        self.tmp_file = NamedTemporaryFile(prefix="plone_zipexport_")
        self.tmp_file.__enter__()
        self.zip_file = ZipFile(self.tmp_file.name, "w", allowZip64=True)
        self.zip_file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zip_file.__exit__(exc_type, exc_value, traceback)
        self.tmp_file.__exit__(exc_type, exc_value, traceback)

    def add_file(self, file_path, file_pointer):
        self.empty = False
        self.zip_file.writefile(file_pointer, file_path)

    @property
    def is_empty(self):
        return self.empty

    def generate(self):
        if self.tmp_file is None:
            raise("Please use ZipGenerator as a context manager.")
        return self.tmp_file
