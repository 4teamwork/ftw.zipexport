from ftw.upgrade import UpgradeStep


class IncludeEmptyFoldersInExport(UpgradeStep):
    """Include empty folders in export.
    """

    def __call__(self):
        self.install_upgrade_profile()
