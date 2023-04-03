
from . import routines
import datetime

if __name__ == "__main__":
    print("Today's games: \n")

    games = routines.get_games_on_date(datetime.date.today())
    
    for game in games:
        message = f'{game.away_team.name} @ {game.home_team.name}'
        message += f"\n{game.away_probable_pitcher} vs {game.home_probable_pitcher}\n"
        print(message)




