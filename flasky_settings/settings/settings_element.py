from ..error import ValidationError


class SettingsElement:
    template = '/flasky_settings/setting/default.html'
    settings_type = 'default'
    _none_allowed: bool = False
    _default = None
    
    def format_value(self, value):
        return value

    def to_validation(self, v) -> tuple[bool, str]:
        if not self.none_allowed and v is None:
            raise ValidationError(message='"None" is not allowed !', obj=self)

    def _parse_value(self, value):
        return value

    def __init__(self, key, title='', description='', default=None, setting=None, none_allowed: bool | None = None,
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
