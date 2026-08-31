import yaml
import os
from types import SimpleNamespace

def _dict_to_namespace(d):
    if isinstance(d, dict):
        return SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [_dict_to_namespace(i) for i in d]
    else:
        return d

def load_settings():
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.yaml')
    with open(settings_path, 'r') as f:
        settings_dict = yaml.safe_load(f)
    return _dict_to_namespace(settings_dict)

settings = load_settings()