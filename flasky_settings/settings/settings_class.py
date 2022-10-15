import os
import codecs
import json

from ..error import PropertyPermissionError
from .settings_element import SettingsElement
from .. import codec_string, logger

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

    def get_value_formattet(self, key):
        se = self.elements.get(key, None)
        v = self.__getattribute__(key)
        v = se.format_value(v)
        return v
    
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

