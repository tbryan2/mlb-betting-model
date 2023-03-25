# Dependencies
import pandas as pd
import tqdm

def preprocess_eva_file(file_path):
    '''
    Preprocess the EVA file to prepare for reading into a DataFrame
    '''
    with open(file_path, 'r') as file:
        content = file.readlines()

    clean_rows = []
    for line in content:
        if line.startswith('play') or line.startswith('id'):
            clean_rows.append(line.strip())

    return clean_rows

def read_eva_to_dataframe(file_path):
    '''
    Read the EVA file into a Pandas DataFrame
    '''
    clean_rows = preprocess_eva_file(file_path)
    data = []

    for row in clean_rows:
        split_row = row.split(',')
        if row.startswith('id'):
            game_id = split_row[1]
        elif row.startswith('play'):
            new_row = [game_id] + split_row
            data.append(new_row)

    headers = ['game_id', 'event_type', 'inning',
               'team', 'player_id', 'count', 'pitches', 'event']
    df = pd.DataFrame(data, columns=headers)

    return df

# Classify the outcome of the play
def classify_outcome(event):
    '''
    Classify the outcome of the play
    '''
    if event.startswith('S'):
        return 'single'
    elif event.startswith('D'):
        return 'double'
    elif event.startswith('T'):
        return 'triple'
    elif event.startswith('H'):
        return 'home_run'
    elif event.startswith('W'):
        return 'walk'
    else:
        return 'out'


def read_ros_to_dataframe(file_path):
    '''
    Read the ROS file into a Pandas DataFrame
    '''
    # Define the column headers for the roster DataFrame
    headers = ['player_id', 'last_name', 'first_name',
               'batting_hand', 'throwing_hand', 'team', 'position']

    # Read the ROS file into a pandas DataFrame
    df = pd.read_csv(file_path, header=None, names=headers)

    return df
