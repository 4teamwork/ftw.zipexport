from plone.i18n.normalizer.interfaces import IFileNameNormalizer
from Products.CMFPlone.utils import safe_unicode
from zope.component import getUtility
import os.path


def normalize_path(path):
    path = safe_unicode(path).replace(u'\\', u'/')
    path = os.path.normpath(path)
    normalizer = getUtility(IFileNameNormalizer)
    return '/'.join(map(normalizer.normalize, path.split('/')))
