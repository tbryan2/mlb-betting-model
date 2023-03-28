# Dependencies
import os
import pandas as pd
from sqlalchemy import create_engine

# Create engine
engine = create_engine('postgresql://postgres:1789@localhost:5433/baseball')

# Query the database
final_score_query = '''
SELECT * FROM final_scores
'''

batter_query = '''
SELECT * FROM batter_statistics
'''

pitcher_query = '''
SELECT * FROM pitchers
'''

# Create dataframes from the queries
final_scores_df = pd.read_sql(final_score_query, engine)
batter_df = pd.read_sql(batter_query, engine)
pitcher_df = pd.read_sql(pitcher_query, engine)

# Drop duplicates from all DataFrames
final_scores_df = final_scores_df.drop_duplicates()
batter_df = batter_df.drop_duplicates()
pitcher_df = pitcher_df.drop_duplicates()

# Redefine the inning column in pitcher_df as a string
pitcher_df['inning'] = pitcher_df['inning'].astype(str)

# Create a copy of the batter_df DataFrame to merge on the pitcher_df DataFrame
batter_df_copy = batter_df.copy()

# Keep only the necessary columns from the batter_df_copy DataFrame
batter_df_copy = batter_df_copy[['game_id', 'home_team', 'away_team', 'inning', 'batter_player_id', 'outcome']]

# Merge the pitcher_df DataFrame with the batter_df_copy DataFrame
pitcher_df = pitcher_df.merge(
    batter_df_copy, on=['game_id', 'inning', 'batter_player_id'])

# Define the outcomes for the pitcher and whether they were a starter or relief pitcher
outcomes = ['out_in_play', 'strikeout', 'single', 'walk',
            'double', 'home_run', 'stolen_base', 'triple']

for outcome in outcomes:
    # Create a starting_pitcher column for each outcome
    pitcher_df[f'starting_pitcher_{outcome}'] = pitcher_df.apply(
        lambda row: 1 if row['outcome'] == outcome and row['starter'] == 1 else 0, axis=1)

    # Create a relief_pitcher column for each outcome
    pitcher_df[f'relief_pitcher_{outcome}'] = pitcher_df.apply(
        lambda row: 1 if row['outcome'] == outcome and row['starter'] == 0 else 0, axis=1)
    
# Define the outcomes for the batter

# out in play
batter_df['batter_out_in_play'] = batter_df['outcome'].apply(
    lambda x: 1 if x == 'out in play' else 0)

# strikeout
batter_df['batter_strikeout'] = batter_df['outcome'].apply(lambda x: 1 if x == 'strikeout' else 0)

# single
batter_df['batter_single'] = batter_df['outcome'].apply(lambda x: 1 if x == 'single' else 0)

# walk and intentional_walk
batter_df['batter_walk'] = batter_df['outcome'].apply(
    lambda x: 1 if x == 'walk' or x == 'intentional_walk' else 0)

# double
batter_df['batter_double'] = batter_df['outcome'].apply(lambda x: 1 if x == 'double' else 0)

# home_run
batter_df['batter_home_run'] = batter_df['outcome'].apply(lambda x: 1 if x == 'home_run' else 0)

# stolen_base
batter_df['batter_stolen_base'] = batter_df['outcome'].apply(
    lambda x: 1 if x == 'stolen_base' else 0)

# triple
batter_df['batter_triple'] = batter_df['outcome'].apply(lambda x: 1 if x == 'triple' else 0)

# drop the unnecessary columns in pitcher_df
pitcher_df = pitcher_df.drop(['outcome'], axis=1)

# Merge the batter_df DataFrame with the pitcher_df DataFrame
df = batter_df.merge(pitcher_df, on=['game_id', 'inning', 'batter_player_id', 'home_team', 'away_team'])

# Merge the final_scores_df DataFrame with the df DataFrame
df = df.merge(final_scores_df, on=['game_id', 'away_team', 'home_team'])

# Create a column for whether or not the home team won
df['home_team_won'] = df.apply(lambda row: 1 if row['home_team_score'] > row['away_team_score'] else 0, axis=1)

# Load the DataFrame into a PostgreSQL database
df.to_sql('prod', engine, index=False)