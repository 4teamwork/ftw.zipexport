from tempfile import NamedTemporaryFile
from ftw.zipexport.zipfilestream import ZipFile


class ZipGenerator(object):
    """
    Generates the zip. Acts as context manager to ensure that all temporary
    files are deleted after usage.
    """

    def __init__(self):
        self.file_tuples = []

    def __enter__(self):
        self.tmp_zip_file = NamedTemporaryFile(prefix="plone_zipexport_")
        self.tmp_zip_file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.tmp_zip_file.__exit__(exc_type, exc_value, traceback)

    def add_file(self, file_path, file_pointer):
        self.file_tuples.append((file_path, file_pointer))

    @property
    def is_empty(self):
        return not self.file_tuples

    def generate(self):
        if self.tmp_zip_file is None:
            raise("Please use ZipGenerator as a context manager.")
        with ZipFile(self.tmp_zip_file.name, "w", allowZip64=True) as zip_container:
            for file_path, file_pointer in self.file_tuples:
                zip_container.writefile(file_pointer, file_path)

        return self.tmp_zip_file
