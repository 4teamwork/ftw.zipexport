from zope.component import adapts
from zope.interface import implements
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.interfaces import IZipGenerator
from tempfile import NamedTemporaryFile
from zipfilestream import ZipFile


class ZipGenerator(object):
    """
    Generates the zip. Acts as context manager to ensure that all temporary
    files are deleted after usage.
    """
    implements(IZipGenerator)
    adapts(IZipRepresentation)

    def __init__(self, context):
        self.context = context

    def __enter__(self):
        self.tmp_zip_file = NamedTemporaryFile(prefix="plone_zipexport_")
        self.tmp_zip_file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.tmp_zip_file.__exit__(exc_type, exc_value, traceback)

    def get_zip(self):
        if self.tmp_zip_file is None:
            raise("Please use ZipGenerator as a context manager.")
        with ZipFile(self.tmp_zip_file.name, "w", allowZip64=True) as zip_container:
            for file_path, file_pointer in self.context.get_files():
                zip_container.writefile(file_pointer, file_path )

        return self.tmp_zip_file
