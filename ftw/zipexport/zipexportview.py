from Products.Five.browser import BrowserView
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.generation import ZipGenerator
from zope.component import getMultiAdapter
import os
from ZPublisher.Iterators import filestream_iterator


class ZipExportView(BrowserView):

    def __init__(self, *args, **kwargs):
        super(ZipExportView, self).__init__(*args, **kwargs)

    def __call__(self):
        response = self.request.response
        repre = getMultiAdapter((self.context, self.request),
                                interface=IZipRepresentation)
        
        with ZipGenerator() as generator:
            for path, pointer in repre.get_files():
                generator.add_file(path, pointer)

            zip_file = generator.generate()
            filename = '%s.zip' % self.context.title
            response.setHeader("Content-Disposition",
                                 'inline; filename="%s"' % filename)
            response.setHeader("Content-type", "application/zip")
            response.setHeader("Content-Length", os.stat(zip_file.name).st_size)

            return filestream_iterator(zip_file.name, 'rb')
