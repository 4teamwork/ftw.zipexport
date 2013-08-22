from Products.Five.browser import BrowserView
from ftw.zipexport.interfaces import IZipRepresentation
from zope.component import getAdapter, getMultiAdapter
import os
from ZPublisher.Iterators import filestream_iterator


class ZipExportView(BrowserView):

    def __init__(self, *args, **kwargs):
        super(ZipExportView, self).__init__(*args, **kwargs)

    def __call__(self):
        response = self.request.response
        repre = getMultiAdapter((self.context, self.request),
                                interface=IZipRepresentation)
        with getAdapter(repre) as generator:
            zip = generator.get_zip()
            filename = '%s.zip' % self.context.title
            response.setHeader("Content-Disposition",
                                 'inline; filename="%s"' % filename)
            response.setHeader("Content-type", "application/zip")
            response.setHeader("Content-Length", os.stat(zip.name).st_size)

            return filestream_iterator(zip.name, 'rb')
