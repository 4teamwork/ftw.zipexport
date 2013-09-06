from ftw.zipexport.zipfilestream import ZipFile
from StringIO import StringIO
from tempfile import NamedTemporaryFile
from unittest2 import TestCase


class TestZipFileStream(TestCase):

    def test_write_normal_file(self):
        with NamedTemporaryFile(prefix="plone_zipexport_") as tmp_test_file:
            test_file = open(tmp_test_file.name, "w")
            test_file.write("Testdata.")
            with NamedTemporaryFile(prefix="plone_zipexport_") as tmp_zip_file:
                with ZipFile(tmp_zip_file.name, "w") as zip_file:
                    zip_file.writefile(test_file, "testfile.txt")

                    self.assertEquals(['testfile.txt'], zip_file.namelist())

    def test_write_file_stream(self):
        with NamedTemporaryFile(prefix="plone_zipexport_") as tmp_zip_file:
            with ZipFile(tmp_zip_file.name, "w") as zip_file:
                sio = StringIO("test")
                zip_file.writefile(sio, "teststream.txt")

                self.assertEquals(['teststream.txt'], zip_file.namelist())
