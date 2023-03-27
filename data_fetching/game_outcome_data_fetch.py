# Dependencies
import os
import pandas as pd
from sqlalchemy import create_engine


def extract_final_scores(file_path):
    # Define the columns you want to extract
    cols_to_extract = ["date", "away_team", "home_team",
                       "away_team_score", "home_team_score"]

    # Read the CSV file and extract the final scores
    df = pd.read_csv(file_path, usecols=[
                     0, 3, 6, 9, 10], header=None, names=cols_to_extract)

    # Convert the date column to a datetime object
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

    # Add a game_id column
    df['game_id'] = df['home_team'] + df['date'].dt.strftime('%Y%m%d') + '0'

    # Drop the date column
    df.drop('date', axis=1, inplace=True)

    return df

# Loop through the years and extract the final scores
final_scores_list = []

years = range(2012, 2022 + 1)

game_logs_folder = 'data/game_logs'

for year in years:
    game_logs_file = os.path.join(game_logs_folder, 'gl' + str(year) + '.txt')
    if os.path.isfile(game_logs_file):
        final_scores_list.append(extract_final_scores(game_logs_file))

# Concatenate the list of dataframes into a single dataframe
final_scores_df = pd.concat(final_scores_list)

# Database connection parameters
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
final_scores_df.to_sql(
    'final_scores', engine, if_exists='append', index=False)
