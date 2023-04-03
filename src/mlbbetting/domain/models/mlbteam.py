from __future__ import annotations
from typing import Optional
from dataclasses import dataclass


@dataclass
class MlbTeamVenue:
    id  : Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


@dataclass
class MlbTeamLeague:
    id  : Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


@dataclass
class MlbTeamDivision:
    id  : Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None


@dataclass
class MlbTeam:
    allStarStatus   : Optional[str]             = None
    id              : Optional[int]             = None
    name            : Optional[str]             = None
    link            : Optional[str]             = None
    season          : Optional[int]             = None
    teamCode        : Optional[str]             = None
    fileCode        : Optional[str]             = None
    abbreviation    : Optional[str]             = None
    teamName        : Optional[str]             = None
    locationName    : Optional[str]             = None
    firstYearOfPlay : Optional[str]             = None
    shortName       : Optional[str]             = None
    franchiseName   : Optional[str]             = None
    clubName        : Optional[str]             = None
    active          : Optional[bool]            = None
    venue           : Optional[MlbTeamVenue]    = None
    league          : Optional[MlbTeamLeague]   = None
    division        : Optional[MlbTeamDivision] = None
