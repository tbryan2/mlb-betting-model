import os
import pandas as pd
from sqlalchemy import create_engine
from mlbbetting import configs


def extract_pitchers(file_path):
    '''
    Extract pitchers from the event file
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pitchers = []
    game_id = ""
    inning = 1
    home_team = ""
    away_team = ""
    batter_player_id = ""
    current_pitcher = {0: None, 1: None}

    for line in lines:
        tokens = line.strip().split(',')

        if tokens[0] == "id":
            game_id = tokens[1]

        if tokens[0] == "info":
            if tokens[1] == "hometeam":
                home_team = tokens[2]
            elif tokens[1] == "visteam":
                away_team = tokens[2]

        if tokens[0] == "start" or tokens[0] == "sub":
            if tokens[-1] == "1":
                home_away = 1 if tokens[3] == "0" else 0
                team = home_team if home_away == 0 else away_team
                starter = 1 if tokens[0] == "start" else 0
                current_pitcher[home_away] = {
                    "game_id": game_id,
                    "pitcher_home_away": home_away,
                    "team": team,
                    "pitcher_player_id": tokens[1],
                    "pitcher_player_name": tokens[2].strip('"'),
                    "starter": starter
                }

        if tokens[0] == "play":
            if tokens[-1].startswith("NP") or tokens[-1].startswith("BK"):
                continue
            inning = int(tokens[1])
            batter_player_id = tokens[3]
            home_away = 0 if tokens[2] == "0" else 1
            pitcher_details = current_pitcher[home_away].copy()
            pitcher_details["inning"] = inning
            pitcher_details["batter_player_id"] = batter_player_id
            pitchers.append(pitcher_details)

    return pitchers



# Main logic...
if __name__ == "__main__":

    data_dir = 'data/event_logs'

    starting_pitchers_list = []

    years = range(2012, 2022 + 1)

    for year in years:
        year_dir = os.path.join(data_dir, str(year) + 'eve')
        event_files = [os.path.join(year_dir, f) for f in os.listdir(
            year_dir) if f.endswith('.EVA') or f.endswith('.EVN')]
        for event_file in event_files:
            starting_pitchers_list.extend(extract_pitchers(event_file))

    starting_pitchers_df = pd.DataFrame(starting_pitchers_list)

    config = configs.get_config(True)

    # Connect to the PostgreSQL database
    engine = create_engine(
        f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}")

    # Append the data to the local PostgreSQL database
    starting_pitchers_df.to_sql('pitchers', engine, if_exists='append', index=False)



