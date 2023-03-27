import os
import pandas as pd
from sqlalchemy import create_engine


def extract_starting_pitchers(file_path):
    '''
    Extract starting pitchers from the event file
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    starting_pitchers = []
    game_id = ""

    for line in lines:
        tokens = line.strip().split(',')

        if tokens[0] == "id":
            game_id = tokens[1]

        if tokens[0] == "start":
            if tokens[-1] == "1":
                starting_pitchers.append({
                    "game_id": game_id,
                    "team": tokens[3],
                    "player_id": tokens[1],
                    "player_name": tokens[2].strip('"')
                })

    return starting_pitchers


data_dir = 'data/'

starting_pitchers_list = []

years = range(2012, 2022 + 1)

for year in years:
    year_dir = os.path.join(data_dir, str(year) + 'eve')
    event_files = [os.path.join(year_dir, f) for f in os.listdir(
        year_dir) if f.endswith('.EVA') or f.endswith('.EVN')]
    for event_file in event_files:
        starting_pitchers_list.extend(extract_starting_pitchers(event_file))

starting_pitchers_df = pd.DataFrame(starting_pitchers_list)

# Database connection parameters
db_user = "postgres"
db_password = "1789"
db_name = "baseball"
db_host = "localhost"
db_port = "5433"

# Connect to the PostgreSQL database
engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Append the data to the local PostgreSQL database
starting_pitchers_df.to_sql('starting_pitchers', engine, if_exists='append', index=False)
