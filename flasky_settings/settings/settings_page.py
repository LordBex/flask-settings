

class SettingsPage:
    pages = {}

    def __init__(self, key, title):
        self.setting_groups = []
        self.title = title
        self.key = key

        SettingsPage.pages[key] = self

    @classmethod
    def get_page(cls, page_key, default=None):
        return cls.pages.get(page_key, default)

    def add_settings_groups(self, *settings_groups):
        for s in settings_groups:
            self.setting_groups.append(s)

    def loop_groups(self):
        for sg in self.setting_groups:
            yield sg
