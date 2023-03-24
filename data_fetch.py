# Dependencies
import time
import pandas as pd
import tqdm
from pybaseball import batting_stats_range
from sqlalchemy import create_engine

# Initialize an empty dataframe
df = pd.DataFrame()

# Define sleep time in seconds (for example, 2 seconds)
sleep_time = 2

# PostgreSQL connection string
db_name = 'postgres'
user = 'postgres'
password = '1789'
host = 'localhost'
port = '5433'
conn_str = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

# Function to store data in PostgreSQL
def store_data_in_postgresql(df, table_name, conn_str):
    engine = create_engine(conn_str)
    df.to_sql(table_name, engine, if_exists='append', index=False)


# Loop through each year 2015-2022 as a string and for each year March 15 through November 15; use tqdm to monitor progress
for year in range(2015, 2022):
    for date in tqdm.tqdm(pd.date_range(f"{year}-03-15", f"{year}-11-15").strftime("%Y-%m-%d")):
        try:
            # Retrieve the batting stats for that day
            data = batting_stats_range(date, date)
            # Append the data to the dataframe
            df = pd.concat([df, data])
        except IndexError:
            # If there is no data for that day, skip it
            pass

        # Check if it's the last day of the month
        current_date = pd.Timestamp(date)
        last_day_of_month = current_date + pd.offsets.MonthEnd(0)
        if current_date == last_day_of_month:
            # Output the data to a local PostgreSQL server
            table_name = f"baseball_stats_{year}_{current_date.month}"
            store_data_in_postgresql(df, mlb_dailystats, conn_str)

            # Print a warning if the month is empty
            if df.empty:
                print(
                    f"Warning: Data for {current_date.strftime('%Y-%m')} is empty.")

            # Reset the dataframe for the next month
            df = pd.DataFrame()

        # Sleep for specified duration before making the next request
        time.sleep(sleep_time)
