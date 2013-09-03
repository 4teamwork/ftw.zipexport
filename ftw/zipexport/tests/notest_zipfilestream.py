from ftw.zipexport.zipfilestream import ZipFile
from StringIO import StringIO
from tempfile import NamedTemporaryFile


with NamedTemporaryFile(prefix="zipfilestream_") as tmp_file:
    with ZipFile(tmp_file.name, "w") as zip_file:
        sio = StringIO("test")
        zip_file.writefile(sio, "test.txt")
        print "Wrote StringIO into test.txt"
        f = open("notest_zipfilestream.py", "r")
        zip_file.writefile(f, "file.py")
        print "Wrote file test_zipfilestream.py into file.py"
        zip_file.printdir()
