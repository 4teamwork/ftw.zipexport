from ftw.builder.content import register_dx_content_builders
from ftw.builder.testing import BUILDER_LAYER
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from zope.configuration import xmlconfig
import pkg_resources


IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


class FtwZipexportLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.zipexport:default')

        if IS_PLONE_5:
            applyProfile(portal, 'plone.app.contenttypes:default')
            register_dx_content_builders(force=True)


FTW_ZIPEXPORT_FIXTURE = FtwZipexportLayer()
FTW_ZIPEXPORT_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(FTW_ZIPEXPORT_FIXTURE, ),
        name="FtwZipexport:Functional")

FTW_ZIPEXPORT_INTEGRATION_TESTING = IntegrationTesting(
        bases=(FTW_ZIPEXPORT_FIXTURE, ),
        name="FtwZipexport:Integration")
