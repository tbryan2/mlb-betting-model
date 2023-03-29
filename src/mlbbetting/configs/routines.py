from __future__ import annotations
from .iconfig import IConfig
from .configs import ConfigDevelopment, ConfigProduction

def get_config(is_development) -> IConfig:
    """Get the current config"""
    
    if is_development:
        return ConfigDevelopment

    return ConfigProduction