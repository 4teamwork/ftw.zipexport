from ftw.zipexport import _
from ftw.zipexport.generation import ZipGenerator
from ftw.zipexport.interfaces import IZipRepresentation
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from ZPublisher.Iterators import filestream_iterator
import os


class ZipSelectedExportView(BrowserView):

    def __init__(self, *args, **kwargs):
        super(ZipSelectedExportView, self).__init__(*args, **kwargs)

    def __call__(self):
        portal = getSite()
        paths = self.request.get('paths', [])
        objects = [portal.restrictedTraverse(path) for path in paths]

        return self.zip_selected(objects)

    def zip_selected(self, objects):
        response = self.request.response

        with ZipGenerator() as generator:

            for obj in objects:
                repre = getMultiAdapter((obj, self.request),
                                        interface=IZipRepresentation)

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
                                 'inline; filename="%s"' % filename.encode('utf-8'))
            response.setHeader("Content-type", "application/zip")
            response.setHeader("Content-Length", os.stat(zip_file.name).st_size)

            return filestream_iterator(zip_file.name, 'rb')


class ZipExportView(ZipSelectedExportView):

    def __init__(self, *args, **kwargs):
        super(ZipExportView, self).__init__(*args, **kwargs)

    def __call__(self):
        return self.zip_selected([self.context])
