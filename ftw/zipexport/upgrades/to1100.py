from ftw.upgrade import UpgradeStep


class ExportRestriction(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.zipexport.upgrades:1100')
