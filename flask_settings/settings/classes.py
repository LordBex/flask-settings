from flask_settings.settings import SettingsElement, SettingClass
from flask_settings.error import ValidationError, ParsingError


class SE_Bool(SettingsElement):
    template = '/flask_settings/setting/bool.html'
    settings_type = 'bool'
    _none_allowed = True

    def to_validation(self, v) -> (bool, str):
        super().to_validation(v)

        if not isinstance(v, bool):
            raise ValidationError(message=f'ValueType is not correct (Type= {str(type(v))}). Must be Bool !')

    def parse_value(self, v):
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
    template = '/flask_settings/setting/string.html'
    settings_type = 'string'
    input_type = 'text'
    _default = ''

    def to_validation(self, v) -> (bool, str):
        super().to_validation(v)
        if not isinstance(v, str):
            raise ValidationError(message=f'[StringElement] ValueType is not correct (Type= {str(type(v))}). Must be String ! ')

    def init(self, placeholder: str = '', **kwargs):            # Todo adding html validation function https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_input_placeholder PATTERN
        self.placeholder = placeholder


class SE_String_Split(SettingsElement):     # TODO Mach das mit einem HTML Template mit add und remove function
    template = '/flask_settings/setting/string.html'
    settings_type = 'string'
    input_type = 'text'
    _default = []

    def to_validation(self, v) -> (bool, str):
        super().to_validation(v)
        if not isinstance(v, list):
            raise ValidationError(
                message=f'[StringElement] ValueType is not correct (Type= {str(type(v))}). Must be List ! '
            )

    def parse_value(self, v: str | list):
        if isinstance(v, str):      # TODO better type checking
            l: list[str] = v.split(';')
            v = list(map(lambda s: s.strip(), l))
        return v

    def init(self, placeholder: str = '', **kwargs):            # Todo adding html validation function https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_input_placeholder PATTERN
        self.placeholder = placeholder


class SE_Text(SettingsElement):
    template = '/flask_settings/setting/text.html'
    settings_type = 'text'

    def to_validation(self, v) -> (bool, str):
        super().to_validation(v)
        if not isinstance(v, str):
            raise ValidationError(message=f'[TextElement] ValueType is not correct (Type= {str(type(v))}). Must be String ! ')

    def init(self, rows: int = 3, **kwargs):
        self.rows = rows


class SE_MultiSelect(SettingsElement):
    template = '/flask_settings/setting/multi_select_as_list.html'
    settings_type = 'multi-select'

    def to_validation(self, v) -> (bool, str):
        super().to_validation(v)
        if not isinstance(v, list):
            raise ValidationError(message=f'[MultiSelect] ValueType is not correct (Type= {str(type(v))}). Must be List !')

    def init(self, items: list = '', **kwargs):
        self.items = items

    def loop_items(self, setting_group: SettingClass):
        v = setting_group[self.key]
        for i in self.items:
            active = i in v
            yield {
                'name': str(i),
                'active': active
            }


class SE_Select(SettingsElement):
    template = '/flask_settings/setting/select.html'
    settings_type = 'select'

    def to_validation(self, v) -> (bool, str):
        super().to_validation(v)

    def init(self, items: list = '', **kwargs):
        self.items = items

    def loop_items(self, setting_group: SettingClass):
        v = setting_group[self.key]
        for i in self.items:
            active = (i == v)
            yield {
                'name': str(i),
                'active': active
            }