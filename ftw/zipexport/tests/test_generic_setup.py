from Products.CMFCore.utils import getToolByName
from ftw.zipexport.testing import FTW_ZIPEXPORT_FUNCTIONAL_TESTING
from plone.app.testing import applyProfile
from unittest2 import TestCase


class TestDefaultInstallation(TestCase):

    layer = FTW_ZIPEXPORT_FUNCTIONAL_TESTING

    def test_default_profile_installed(self):
        portal = self.layer['portal']
        portal_setup = getToolByName(portal, 'portal_setup')

        version = portal_setup.getLastVersionForProfile(
            'ftw.zipexport:default')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')

    def test_documentaction_profile_installation(self):
        portal = self.layer['portal']
        portal_setup = getToolByName(portal, 'portal_setup')

        applyProfile(portal, 'ftw.zipexport:documentaction')

        version = portal_setup.getLastVersionForProfile(
            'ftw.zipexport:documentaction')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')
