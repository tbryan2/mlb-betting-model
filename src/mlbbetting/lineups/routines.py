from __future__ import annotations
import statsapi
from mlbbetting.domain.models import MlbGame
from mlbbetting.domain.models import MlbTeam
from mlbbetting.common import mapper
import datetime

def get_teams_dict() -> dict[int, MlbTeam]:
    """Get a dictionary of all the teams (TeamID, Team)"""

    result = dict()

    for team in get_all_teams():
        result[team.id] = team
    
    return result


def get_all_teams() -> list[MlbTeam]:
    """Get a list of all the teams"""

    # fetch the data from the api
    data = statsapi.get('teams',{'sportIds':1,'activeStatus':'Yes'}).get('teams')

    # map the dictionaries into MlbTeam objects
    teams = mapper.to_models(data, MlbTeam)
    
    return teams


def get_games_on_date(day: datetime.date) -> list[MlbGame]:
    """Get all the games for the specified date"""

    api_data: list[dict] = statsapi.schedule(date=day)
    teams = get_teams_dict()

    games = [_map_game(teams, game) for game in api_data]

    return games



def _map_game(teams_dict: dict[int, MlbTeam], game_dict: dict) -> MlbGame:
    """Map the api response into a domain model"""

    result = mapper.to_model(game_dict, MlbGame)
    result.home_team = teams_dict.get(result.home_id)
    result.away_team = teams_dict.get(result.away_id)

    return result