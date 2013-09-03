from Products.Five.browser import BrowserView
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.generation import ZipGenerator
from zope.component import getMultiAdapter
import os
from ZPublisher.Iterators import filestream_iterator
from Products.statusmessages.interfaces import IStatusMessage
from ftw.zipexport import _


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

            # check if zip has files
            if generator.is_empty:
                messages = IStatusMessage(self.request)
                messages.add(_("statmsg_content_not_supported",
                    default=u"Zip export is not supported on the selected content."),
                    type=u"error")
                self.request.response.redirect(self.context.absolute_url())
                return

            zip_file = generator.generate()
            filename = '%s.zip' % self.context.title
            response.setHeader("Content-Disposition",
                                 'inline; filename="%s"' % filename)
            response.setHeader("Content-type", "application/zip")
            response.setHeader("Content-Length", os.stat(zip_file.name).st_size)

            return filestream_iterator(zip_file.name, 'rb')
