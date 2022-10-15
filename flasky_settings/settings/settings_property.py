from .settings_class import SettingClass
from .settings_page import SettingsPage
from .settings_element import SettingsElement

class SettingProperty:

    def __init__(self, setting_class, *args, **kwargs):
        """ Attributes of 'SettingProperty' """
        self.setting_class = setting_class
        self.args = args
        self.kwargs = kwargs
        self.se: SettingsElement | None = None

    def __set_name__(self, owner, name):
        self.kwargs['key'] = name
        self.public_name = name
        self.private_name = '_' + name
        owner: SettingClass
        self.se: SettingsElement = self.setting_class(*self.args, **self.kwargs)

        if 'elements' in owner.__dict__:
            owner.elements[name] = self.se
        else:
            owner.elements = {name: self.se}

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name, self.se.default)

    def __set__(self, obj, value):
        value = self.se._parse_value(value)
        self.se.to_validation(value)
        setattr(obj, self.private_name, value)
