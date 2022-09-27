from flasky_settings.error import ValidationError, PropertyPermissionError
from flasky_settings import logger
import os
import codecs
import json

codec_string = 'utf-8'


class SettingsElement:
    template = '/flasky_settings/setting/default.html'
    settings_type = 'default'
    _none_allowed: bool = False
    _default = None

    def to_validation(self, v) -> (bool, str):
        if not self.none_allowed and v is None:
            raise ValidationError(message='"None" is not allowed !', obj=self)

    def parse_value(self, value):
        return value

    def __init__(self, key, title, description='', default=None, setting=None, none_allowed: bool | None = None,
                 col='12', **kwargs):
        self.key = key
        self.title = title
        self.description = description

        self.col = col
        self.default = default if default is not None else self._default
        self.setting = setting

        self.none_allowed = none_allowed if none_allowed is not None else self._none_allowed
        self.init(**kwargs)

    def init(self, **kwargs):
        pass


class SettingProperty:

    def __init__(self, setting_class, *args, **kwargs):
        """ Attributes of 'SettingProperty' """
        settings: SettingClass
        self.setting_class = setting_class
        self.args = args
        self.kwargs = kwargs
        self.se = None

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
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        value = self.se.parse_value(value)
        self.se.to_validation(value)
        setattr(obj, self.private_name, value)


class SettingClass:
    all_settings = {}
    elements: dict[str, SettingsElement] = {}
    settings_path = None

    def __init__(self, key, title):
        self.key = key
        self.title = title

        SettingClass.all_settings[key] = self
        self.load()

    def loop_elements(self):
        for v in self.elements.values():
            yield v

    def set_property(self, k, v):
        if k in self.elements.keys():
            setattr(self, k, v)
        else:
            raise PropertyPermissionError(property_name=k)

    def set_properties(self, d: dict):
        for k, v in d.items():
            self.set_property(k, v)

    def get_property(self, k, default=None) -> any:
        if k in self.elements.keys():
            return self.__getattribute__(k)
        return default

    def get_properties(self) -> dict:
        data = {e: self.get_property(e) for e in self.elements.keys()}
        return data

    def __getitem__(self, item):
        return self.__getattribute__(item)

    # save / loading - configuration

    def generate_file_name(self):
        return f"{self.__class__.__name__}-{self.key}.json"

    def generate_full_file_path(self, filename=None):
        if filename is None:
            filename = self.generate_file_name()
        full_path_filename = os.path.join(self.settings_path, filename)
        return full_path_filename

    def save(self):
        if self.settings_path is None:                      # TODO CHECK IF THIS IST BEST METHODE
            raise Exception("'settings_path' is None")
        # get settings data (for saving)
        data = self.get_properties()
        data_string = json.dumps(data, indent=2)
        # create/save File
        filename = self.generate_file_name()
        full_path_filename = self.generate_full_file_path(filename=filename)
        with codecs.open(full_path_filename, 'w', codec_string) as f:
            f.write(data_string)
            logger.info(f"[{self.__class__.__name__}] Saved Config to '{filename}'")

    def load_default_values(self):
        for e in self.elements.values():
            e: SettingsElement
            setattr(self, e.key, e.default)

    def load_from_file(self, file):
        with codecs.open(file, 'r', codec_string) as f:
            d = json.load(f)
            self.set_properties(d)

    def load(self):
        filename = self.generate_file_name()
        full_path_filename = self.generate_full_file_path(filename=filename)

        if os.path.exists(full_path_filename):
            self.load_from_file(full_path_filename)
            logger.info(f"[{self.__class__.__name__}] Loaded Config from File '{filename}'")
        else:
            logger.info(f"[{self.__class__.__name__}] Load Default Configuration")
            self.load_default_values()

    # class methods

    @classmethod
    def get_group(cls, key, default=None):
        return cls.all_settings.get(key, default)

    @classmethod
    def save_to_path(cls):
        for setting in cls.all_settings.values():
            setting.save()

    @classmethod
    def set_settings_path(cls, path):
        cls.settings_path = path


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
