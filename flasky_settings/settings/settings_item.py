from collections import namedtuple

setting_item_tuple = namedtuple(
    'setting_item',
    (
        'key',
        'title',
        'description',      # TODO use in tempate but where
        'real_value'
        )
    )

class SettingItemsList:
    setting_item = namedtuple('setting_item', ('key', 'title', 'description', 'real_value'))
    
    def __init__(self):
        self.items : dict[str:dict] = {}
    
    def get_keys(self):
        return self.items.keys()
    
    def add_item(self, key, title, description=None, real_value=None):
        self.items[key] = setting_item_tuple(key, title, description, real_value)
        
    def key_to_real_value(self, key):
        if key in self.items:
            r = self.items.get(key)
            if r is None:   # TODO to warning or something else
                return key
            return r.real_value
        else:
            raise ValueError(f"Key '{key}' is not settet. Item not exists !")
    
    def loop_items(self):
        for i in self.items.values():
            yield i