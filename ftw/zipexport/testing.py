from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig
from ftw.builder.testing import BUILDER_LAYER


class FtwZipexportLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import ftw.zipexport
        xmlconfig.file('configure.zcml',
                        ftw.zipexport,
                        context=configurationContext)

        import plone.dexterity
        xmlconfig.file('configure.zcml', plone.dexterity,
            context=configurationContext)

        import plone.namedfile
        xmlconfig.file('configure.zcml', plone.namedfile,
            context=configurationContext)


FTW_ZIPEXPORT_FIXTURE = FtwZipexportLayer()
FTW_ZIPEXPORT_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(FTW_ZIPEXPORT_FIXTURE, ),
        name="FtwZipexport:Functional")

FTW_ZIPEXPORT_INTEGRATION_TESTING = IntegrationTesting(
        bases=(FTW_ZIPEXPORT_FIXTURE, ),
        name="FtwZipexport:Integration")
