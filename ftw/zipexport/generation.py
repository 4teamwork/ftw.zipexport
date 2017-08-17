from exceptions import IOError
from ftw.zipexport.utils import normalize_path
from ftw.zipexport.zipfilestream import ZipFile
from Products.CMFPlone.utils import safe_unicode
from tempfile import NamedTemporaryFile
import os
import sys
import zipfile


class NotEnoughSpaceOnDiskException(IOError):
    """ Thrown when there is not enough space on disk to create the zip file.
    """


class ZipGenerator(object):
    """
    Generates the zip. Acts as context manager to ensure that all temporary
    files are deleted after usage.
    """

    def __init__(self, path_normalizer=normalize_path):
        self.empty = True
        self.path_normalizer = path_normalizer

    def __enter__(self):
        self.tmp_file = NamedTemporaryFile(prefix="plone_zipexport_")
        self.tmp_file.__enter__()
        self.zip_file = ZipFile(self.tmp_file.name, "w", allowZip64=True)
        self.zip_file.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zip_file.__exit__(exc_type, exc_value, traceback)
        self.tmp_file.__exit__(exc_type, exc_value, traceback)

    def add_folder(self, folder_path):
        folder_path = safe_unicode(folder_path)

        # Always add a slash at the end of the path
        folder_path = u'{}/'.format(folder_path.strip('/'))

        # Creates a new empty folder
        self.zip_file.writestr(zipfile.ZipInfo(folder_path), '')

        self.empty = False

    def add_file(self, file_path, file_pointer):
        if self.path_normalizer is not None:
            file_path = self.path_normalizer(file_path)
        else:
            file_path = safe_unicode(file_path)

        # paths in zipfile do not have a / at the root
        file_path = file_path.strip('/')

        file_path = self.generate_unique_filepath(file_path)

        if not self.check_disk_has_space_for_file(file_pointer):
            raise NotEnoughSpaceOnDiskException()

        try:
            self.zip_file.writefile(file_pointer, file_path)
        except RuntimeError:
            raise StandardError("ZipFile already generated/closed. "
                                "Please add all files before generating.")
        self.empty = False

    def generate_unique_filepath(self, file_path):
        if file_path not in self.zip_file.namelist():
            return file_path

        path, name = os.path.split(file_path)
        name, ext = os.path.splitext(name)

        for i in xrange(2, sys.maxint):
            new_filename = os.path.join(path, '%s (%d)%s' % (name, i, ext))
            if new_filename not in self.zip_file.namelist():
                return new_filename

    def check_disk_has_space_for_file(self, file_d):
        disk_stat = os.statvfs(self.tmp_file.name)
        bytes_free = disk_stat.f_frsize * disk_stat.f_bavail
        position = file_d.tell()
        file_d.seek(0, os.SEEK_END)
        file_size = file_d.tell() - position
        file_d.seek(position)
        return file_size < bytes_free

    @property
    def is_empty(self):
        return self.empty

    def generate(self):
        if self.tmp_file is None:
            raise StandardError(
                "Please use ZipGenerator as a context manager.")
        self.zip_file.close()
        return self.tmp_file
