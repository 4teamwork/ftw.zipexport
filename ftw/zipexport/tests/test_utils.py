# -*- coding: utf-8 -*-

from ftw.zipexport.testing import FTW_ZIPEXPORT_INTEGRATION_TESTING
from ftw.zipexport.utils import normalize_path
from unittest2 import TestCase


class TestNormalizePath(TestCase):
    layer = FTW_ZIPEXPORT_INTEGRATION_TESTING

    def test_alphanumeric_characters_are_allowed(self):
        self.assertEquals(u'Foo1/Bar2',
                          normalize_path(u'Foo1/Bar2'))

    def test_dots_hyphens_and_underscores_are_allowed(self):
        self.assertEquals(u'foo-bar_baz/foo.bar.baz',
                          normalize_path(u'foo-bar_baz/foo.bar.baz'))

    def test_spaces_are_allowed(self):
        self.assertEquals(u'Foo Bar',
                          normalize_path(u'Foo Bar'))

    def test_brackets_are_allowed(self):
        self.assertEquals(u'Foo',
                          normalize_path(u'(Foo)'))

    def test_umlauts_are_stripped(self):
        self.assertEquals(u'aou',
                          normalize_path(u'äöü'))

    def test_backslashes_are_converted_to_forward_slashes(self):
        self.assertEquals(u'foo/bar/baz',
                          normalize_path(u'foo/bar\\baz'))

    def test_blacklisted_characters_are_not_allowed(self):
        self.assertEquals(u'X-Y',
                          normalize_path('X"*:<>?|+,;=[]!@Y'))

    def test_path_normalization(self):
        self.assertEquals(u'bar', normalize_path('foo/../bar'))
        self.assertEquals(u'bar', normalize_path('./bar'))
