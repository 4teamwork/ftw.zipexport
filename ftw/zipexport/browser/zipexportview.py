from ftw.zipexport import _
from ftw.zipexport.generation import ZipGenerator
from ftw.zipexport.interfaces import IZipRepresentation
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from ZPublisher.Iterators import filestream_iterator
from zipfile import LargeZipFile
import os


class NoExportableContent(Exception):
    """Raised when no zip exportable content is requested.
    """


class ZipSelectedExportView(BrowserView):

    def __call__(self):
        portal = getSite()
        paths = self.request.get('paths', [])
        objects = [portal.restrictedTraverse(path) for path in paths]

        try:
            return self.zip_selected(objects)
        except NoExportableContent:
            messages = IStatusMessage(self.request)
            messages.add(_("statmsg_no_exportable_content_selected",
                           default=u"No zip-exportable content selected."),
                         type=u"error")
            return self.request.response.redirect(self.context.absolute_url())

    def zip_selected(self, objects):
        response = self.request.response

        # check if zipexport is allowed on this context
        enabled_view = getMultiAdapter((self.context, self.request),
                                       name=u'zipexport-enabled')

        if not enabled_view.zipexport_enabled():
            raise NotFound()

        with ZipGenerator() as generator:

            for obj in objects:
                repre = getMultiAdapter((obj, self.request),
                                        interface=IZipRepresentation)

                for path, pointer in repre.get_files():
                    try:
                        generator.add_file(path, pointer)
                    except LargeZipFile:
                        messages = IStatusMessage(self.request)
                        messages.add(_("statmsg_zip_file_too_big",
                                       default=u"Content is too big "
                                       "to export"),
                                     type=u"error")
                        return self.request.response.redirect(
                            self.context.absolute_url())

            # check if zip has files
            if generator.is_empty:
                raise NoExportableContent()

            zip_file = generator.generate()
            filename = '%s.zip' % self.context.title
            response.setHeader(
                "Content-Disposition",
                'inline; filename="%s"' % filename.encode('utf-8'))
            response.setHeader("Content-type", "application/zip")
            response.setHeader(
                "Content-Length",
                os.stat(zip_file.name).st_size)

            return filestream_iterator(zip_file.name, 'rb')


class ZipExportView(ZipSelectedExportView):

    def __call__(self):
        try:
            return self.zip_selected([self.context])
        except NoExportableContent:
            messages = IStatusMessage(self.request)
            messages.add(_("statmsg_no_exportable_content_found",
                           default=u"No zip-exportable content "
                           "has been found."),
                         type=u"error")
            return self.request.response.redirect(self.context.absolute_url())
