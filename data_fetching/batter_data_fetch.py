# Dependencies
import pandas as pd
import numpy as np
import tqdm
import os
import re
from sqlalchemy import create_engine


def preprocess_eva_file(file_path):
    '''
    Preprocess the EVA file to prepare for reading into a DataFrame
    '''
    with open(file_path, 'r') as file:
        raw_data = file.readlines()

    processed_data = []
    current_game_id = None
    home_team = None
    away_team = None
    daynight = None
    temp = None
    winddirection = None
    windspeed = None
    precip = None
    sky = None

    for line in raw_data:
        if line.startswith('id'):
            current_game_id = line.strip().split(',')[1]
        elif line.startswith('info') and 'visteam' in line:
            away_team = line.strip().split(',')[2]
        elif line.startswith('info') and 'hometeam' in line:
            home_team = line.strip().split(',')[2]
        elif line.startswith('info') and 'daynight' in line:
            daynight = line.strip().split(',')[2]
        elif line.startswith('info') and 'temp' in line:
            temp = line.strip().split(',')[2]
        elif line.startswith('info') and 'winddir' in line:
            winddirection = line.strip().split(',')[2]
        elif line.startswith('info') and 'windspeed' in line:
            windspeed = line.strip().split(',')[2]
        elif line.startswith('info') and 'precip' in line:
            precip = line.strip().split(',')[2]
        elif line.startswith('info') and 'sky' in line:
            sky = line.strip().split(',')[2]
        elif line.startswith('play'):
            play_data = line.strip().split(',')
            play_data.insert(1, current_game_id)
            play_data.insert(2, home_team)
            play_data.insert(3, away_team)
            play_data.extend(
                [daynight, temp, winddirection, windspeed, precip, sky])
            processed_data.append(play_data)

    return processed_data


def read_eva_to_dataframe(file_path):
    '''
    Read the EVA file into a Pandas DataFrame
    '''
    processed_data = preprocess_eva_file(file_path)

    df = pd.DataFrame(processed_data, columns=['event', 'game_id', 'home_team', 'away_team',
                                               'inning', 'home_away', 'player_id', 'count',
                                               'pitches', 'event_description',
                                               'daynight', 'temp', 'winddirection', 'windspeed', 'precip', 'sky'])

    df['batting_team'] = df.apply(
        lambda row: row['home_team'] if row['home_away'] == '1' else row['away_team'], axis=1)

    df['date'] = df['game_id'].str[3:11]
    df['year'] = df['game_id'].str[3:7]

    df['year'] = df['year'].astype('int64')
    df['date'] = df['date'].astype('int64')

    df = df[~df['event_description'].str.startswith('WP')]
    df = df[~df['event_description'].str.startswith('NP')]
    df = df[~df['event_description'].str.startswith('DI')]
    df = df[~df['event_description'].str.startswith('E')]

    df = df.drop(columns=['event', 'count', 'pitches'])

    return df

def classify_outcome(play: str) -> str:
    '''
    Classify the outcome of the play
    '''
    if play.startswith("SB"):
        return "stolen_base"
    elif play.startswith("DI"):
        return "defensive_indifference"
    elif play.startswith("FC"):
        return "fielders_choice"
    elif play.startswith("E"):
        return "error"
    elif play.startswith("WP"):
        return "out in play"
    elif play.startswith("HP"):
        return "hit_by_pitch"
    elif play.startswith("IW"):
        return "intentional_walk"
    elif play.startswith("W"):
        return "walk"
    elif re.match(r"^K([1-9]|[A-Z])?", play):
        return "strikeout"
    elif play.startswith("HR"):
        return "home_run"
    elif play.startswith("H"):
        return "home_run"
    elif play.startswith("T"):
        return "triple"
    elif play.startswith("D"):
        return "double"
    elif play.startswith("S"):
        return "single"
    else:
        return "out in play"
    
def read_ros_to_dataframe(file_path):
    '''
    Read the ROS file into a Pandas DataFrame
    '''
    # Define the column headers for the roster DataFrame
    headers = ['player_id', 'last_name', 'first_name',
               'batting_hand', 'throwing_hand', 'batting_team', 'position']

    # Read the ROS file into a pandas DataFrame
    df = pd.read_csv(file_path, header=None, names=headers)

    # Combine the first and last names into a single column
    df['name'] = df['first_name'] + ' ' + df['last_name']

    # Drop the unnecessary columns
    df = df.drop(columns=['batting_hand', 'throwing_hand', 'first_name', 'last_name'])

    return df

# List the teams in the league
teams = ['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CHN', 'CHA', 'CIN', 'CLE', 'COL', 
         'DET', 'HOU', 'KCA', 'LAN', 'MIA', 'MIL', 'MIN', 'NYN', 'NYA', 'OAK', 'PHI', 
         'PIT', 'SDN', 'SFN', 'SEA', 'SLN', 'TBA', 'TEX', 'TOR', 'WAS']

# Create a single roster DataFrame for all teams
all_rosters = []

years = range(2012, 2022 + 1)

for year in years:
    for team in teams:
        try:
            file_path = f'data/event_logs/{year}eve/{team}{year}.ROS'
            roster = read_ros_to_dataframe(file_path)
            roster['year'] = year  # Add a 'year' column to the roster DataFrame
            all_rosters.append(roster)
        except FileNotFoundError:
            print(f"Roster file not found for team {team} in {year}")

# Combine all rosters into a single DataFrame
combined_rosters = pd.concat(all_rosters, ignore_index=True)

# Database connection parameters
db_user = "postgres"
db_password = "1789"
db_name = "baseball"
db_host = "localhost"
db_port = "5433"

# Connect to the PostgreSQL database
engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

for year in years:
    data = []

    for team in tqdm.tqdm(teams):
        try:
            # Read the EVA file into a DataFrame
            file_path = f'data/event_logs/{year}eve/{year}{team}.EVA'
            team_data = read_eva_to_dataframe(file_path)
        except FileNotFoundError:
            # Read the EVN file into a DataFrame
            file_path = f'data/event_logs/{year}eve/{year}{team}.EVN'
            team_data = read_eva_to_dataframe(file_path)

        # Apply the classification function to the 'event' column to create a new 'outcome' column
        team_data['outcome'] = team_data['event_description'].apply(
            classify_outcome)

        # Merge the all_team_rosters DataFrame with the team_data DataFrame using a left join
        team_data = pd.merge(team_data, combined_rosters, on=[
                             'player_id', 'batting_team', 'year'], how='left')

        # Concatenate each game's DataFrame to the data list
        data.append(team_data)

    # Combine all the DataFrames in the data list into a single DataFrame
    df = pd.concat(data, ignore_index=True)

    # Drop duplicate records
    df = df.drop_duplicates()

    # Append the data to the local PostgreSQL database
    df.to_sql('test_batter_statistics', engine, if_exists='append', index=False)
