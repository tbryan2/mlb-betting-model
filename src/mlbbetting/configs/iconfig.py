from __future__ import annotations
from dataclasses import dataclass
import typing

@dataclass
class IConfig:
    db_user         : str = None
    db_password     : str = None
    db_name         : str = None
    db_host         : str = None
    db_port         : str = None

    weather_api_key : str = None

    is_development : bool = None




