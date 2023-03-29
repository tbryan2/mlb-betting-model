# Dependencies
import os
import pandas as pd
from sqlalchemy import create_engine
from mlbbetting import configs

if __name__ == "__main__":
    config = configs.get_config(True)
    
    # Bring in the data from the postgres database
    engine = create_engine(
        f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}")

    # Grab the pitcher and batter data from the database
    pitcher_df = pd.read_sql_table('pitchers', engine)

    batter_df = pd.read_sql_table('batter_statistics', engine)

    # Redefine the inning column in pitcher_df as a string
    pitcher_df['inning'] = pitcher_df['inning'].astype(str)

    # Keep only the necessary columns from the batter_df DataFrame
    batter_df = batter_df[[
        'game_id', 'home_team', 'away_team', 'inning', 'batter_player_id', 'outcome']]

    # Merge the pitcher_df DataFrame with the batter_df DataFrame
    pitcher_df = pitcher_df.merge(
        batter_df, on=['game_id', 'inning', 'batter_player_id'])
