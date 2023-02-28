
from ..settings import SettingsElement, SettingClass, SettingItemsList
from ..settings.settings_item import setting_item_tuple
from flasky_settings.error import ValidationError
from datetime import datetime


class SE_Bool(SettingsElement):
    template = '/flasky_settings/setting/bool.html'
    settings_type = 'bool'
    _none_allowed = True

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)

        if not isinstance(v, bool):
            raise ValidationError(message=f'ValueType is not correct (Type= {str(type(v))}). Must be Bool !')

    def _parse_value(self, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            v = v.lower()
            match v:
                case '':
                    return None
                case 'true' | 'on':
                    return True
                case 'false':
                    return False
                case _:
                    raise ValidationError()


class SE_String(SettingsElement):
    template = '/flasky_settings/setting/string.html'
    settings_type = 'string'
    input_type = 'text'
    _default = ''

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)
        if not isinstance(v, str):
            raise ValidationError(message=f'[StringElement] ValueType is not correct (Type= {str(type(v))}). Must be String ! ')

    def init(self, placeholder: str = '', **kwargs):            # Todo adding html validation function https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_input_placeholder PATTERN
        self.placeholder = placeholder


class SE_String_Split(SettingsElement):     # TODO Mach das mit einem HTML Template mit add und remove function
    template = '/flasky_settings/setting/string.html'
    settings_type = 'string'
    input_type = 'text'
    _default = []

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)
        if not isinstance(v, list):
            raise ValidationError(
                message=f'[StringElement] ValueType is not correct (Type= {str(type(v))}). Must be List ! '
            )

    def _parse_value(self, v: str | list):
        if isinstance(v, str):      # TODO better type checking
            l: list[str] = v.split(';')
            v = list(map(lambda s: s.strip(), l))
        return v

    def init(self, placeholder: str = '', **kwargs):            # Todo adding html validation function https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_input_placeholder PATTERN
        self.placeholder = placeholder


class SE_Text(SettingsElement):
    template = '/flasky_settings/setting/text.html'
    settings_type = 'text'

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)
        if not isinstance(v, str):
            raise ValidationError(message=f'[TextElement] ValueType is not correct (Type= {str(type(v))}). Must be String ! ')

    def init(self, rows: int = 3, **kwargs):
        self.rows = rows


class SE_MultiSelect(SettingsElement):
    template = '/flasky_settings/setting/multi_select_as_list.html'
    settings_type = 'multi-select'

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)
        if not isinstance(v, list):
            raise ValidationError(message=f'[MultiSelect] ValueType is not correct (Type= {str(type(v))}). Must be List !')

    def init(self, items: list = '', **kwargs):
        self.items = items

    def __loop_list(self, active_key):
        for i in self.items:
            active = (i in active_key)
            if isinstance(i, dict):
                item = i
            elif isinstance(i, tuple):
                k, t = i
                item = {
                    'key': str(k),
                    'title': str(t),
                }
            else:
                item = {
                    'key': str(i),
                    'title': str(i),
                }

            yield active, item

    def __loop_settings_items(self, active_keys):
        self.items: SettingItemsList
        for i in self.items.loop_items():
            active = (i.key in active_keys)
            yield active, i

    def loop_items(self, setting_group: SettingClass = None):
        active_keys = setting_group[self.key] if setting_group is not None else []
        if isinstance(self.items, list):
            yield from self.__loop_list(active_keys)
        elif isinstance(self.items, SettingItemsList):
            yield from self.__loop_settings_items(active_keys)
        else:
            yield from self.__loop_list(active_keys)


class SE_Select(SettingsElement):
    template = '/flasky_settings/setting/select.html'
    settings_type = 'select'

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)

    def init(self, items: list = '', **kwargs):
        self.items = items
        
    def __loop_list(self, active_key):
        for i in self.items:
            active = (i == active_key)
            if isinstance(i, dict):
                item = i
            elif isinstance(i, tuple):
                k, t = i
                item = {
                    'key': str(k),
                    'title': str(t),
                } 
            else:
                item = {
                'key': str(i),
                'title': str(i),
                } 
                
            yield active, item
            
    def __loop_settings_items(self, active_key):
        self.items: SettingItemsList
        for i in self.items.loop_items():
            active = (i.key == active_key)
            yield active, i

    def loop_items(self, setting_group: SettingClass = None):
        active_key = setting_group[self.key] if setting_group else None
        if isinstance(self.items, list):
            yield from self.__loop_list(active_key)
        elif isinstance(self.items, SettingItemsList):
            yield from self.__loop_settings_items(active_key)
        else:
            yield from self.__loop_list(active_key)
        # TODO raise Unknow Looping Item Type or something else xD
    
    def format_value(self, v):
        if isinstance(self.items, list):
            return v
        elif isinstance(self.items, SettingItemsList):
            return self.items.key_to_real_value(v)
            

class SE_DateTime(SettingsElement):
    template = '/flasky_settings/setting/datetime.html'
    settings_type = 'datetime'
    _default = ''

    def to_validation(self, v) -> tuple[bool, str]:
        super().to_validation(v)
        # TODO date-time parsing
        

class SE_Date(SE_DateTime):
    template = '/flasky_settings/setting/datetime.html'
    settings_type = 'date'
    _default = ''
