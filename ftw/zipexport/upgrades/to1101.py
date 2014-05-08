from ftw.upgrade import UpgradeStep
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from ftw.zipexport.interfaces import IZipExportSettings


class UpgradeRegistry(UpgradeStep):

    def __call__(self):
        self.setup_install_profile('profile-ftw.zipexport.upgrades:1101')

        registry = getUtility(IRegistry)

        DOTTED_NAME_KEY = 'ftw.zipexport.interfaces.IZipExportSettings.enabled_dotted_name'

        try:
            old_value = registry[DOTTED_NAME_KEY]
        except KeyError:
            # registy has already been changed
            pass
        else:
            zip_settings = registry.forInterface(IZipExportSettings)
            zip_settings.enabled_dotted_names = [old_value]

            #Unregister the old dotted name setting
            del registry.records[DOTTED_NAME_KEY]
