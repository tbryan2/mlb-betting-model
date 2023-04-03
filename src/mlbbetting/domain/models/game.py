from __future__ import annotations
from typing import Optional, Union
from dataclasses import dataclass
import datetime
from .mlbteam import MlbTeam

strint = Optional[Union[str, int]]


@dataclass
class MlbGameApiStruct:
    game_id               : Optional[int]               = None
    game_datetime         : Optional[datetime.datetime] = None
    game_date             : Optional[datetime.date]     = None
    game_type             : Optional[str]               = None
    status                : Optional[str]               = None
    away_id               : Optional[int]               = None
    home_id               : Optional[int]               = None
    doubleheader          : Optional[str]               = None
    game_num              : Optional[int]               = None
    home_probable_pitcher : Optional[str]               = None
    away_probable_pitcher : Optional[str]               = None
    home_pitcher_note     : Optional[str]               = None
    away_pitcher_note     : Optional[str]               = None
    away_score            : strint                      = None
    home_score            : strint                      = None
    current_inning        : strint                      = None
    inning_state          : Optional[str]               = None
    venue_id              : Optional[int]               = None
    venue_name            : Optional[str]               = None
    summary               : Optional[str]               = None

@dataclass
class MlbGame(MlbGameApiStruct):
    home_team: Optional[MlbTeam] = None
    away_team: Optional[MlbTeam] = None


    


