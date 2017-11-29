from ftw.zipexport import _
from ftw.zipexport.events import ContainerZippedEvent
from ftw.zipexport.generation import NotEnoughSpaceOnDiskException
from ftw.zipexport.generation import ZipGenerator
from ftw.zipexport.interfaces import IZipExportSettings
from ftw.zipexport.interfaces import IZipRepresentation
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from rfc6266 import build_header
from zExceptions import NotFound
from zipfile import LargeZipFile
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.event import notify
from ZPublisher.Iterators import filestream_iterator
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
        except NotEnoughSpaceOnDiskException:
            messages = IStatusMessage(self.request)
            messages.add(_("statmsg_not_enough_space_on_disk",
                           default=u"There is not enough free space on the "
                           "disk to create the zip-file."),
                         type=u"error")
            return self.request.response.redirect(self.context.absolute_url())

    def zip_selected(self, objects):
        response = self.request.response
        settings = getUtility(IRegistry).forInterface(IZipExportSettings)

        with ZipGenerator() as generator:

            for obj in objects:
                repre = getMultiAdapter((obj, self.request),
                                        interface=IZipRepresentation)

                for path, pointer in repre.get_files():
                    if not pointer:
                        if settings.include_empty_folders:
                            generator.add_folder(path)
                        continue

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

            # Trigger the per container event
            notify(ContainerZippedEvent(self.context))

            # Generate response file
            filename = u'%s.zip' % self.context.title
            response.setHeader(
                "Content-Disposition",
                build_header(filename, disposition='attachment'))
            response.setHeader("Content-type", "application/zip")
            response.setHeader("Content-Length",
                               os.stat(zip_file.name).st_size)

            return filestream_iterator(zip_file.name, 'rb')


class ZipExportView(ZipSelectedExportView):

    def __call__(self):
        # check if zipexport is allowed on this context
        enabled_view = getMultiAdapter((self.context, self.request),
                                       name=u'zipexport-enabled')

        if not enabled_view.zipexport_enabled():
            raise NotFound()

        try:
            return self.zip_selected([self.context])
        except NoExportableContent:
            messages = IStatusMessage(self.request)
            messages.add(_("statmsg_no_exportable_content_found",
                           default=u"No zip-exportable content "
                           "has been found."),
                         type=u"error")
            return self.request.response.redirect(self.context.absolute_url())
        except NotEnoughSpaceOnDiskException:
            messages = IStatusMessage(self.request)
            messages.add(_("statmsg_not_enough_space_on_disk",
                           default=u"There is not enough free space on the "
                           "disk to create the zip-file."),
                         type=u"error")
            return self.request.response.redirect(self.context.absolute_url())
