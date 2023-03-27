import pandas as pd
import os

def extract_game_outcome(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    game_outcome = {}
    game_id = ""
    visteam = ""
    hometeam = ""
    home_score = 0
    vis_score = 0

    for line in lines:
        tokens = line.strip().split(',')

        if tokens[0] == "id":
            game_id = tokens[1]

        if tokens[0] == "info":
            if tokens[1] == "visteam":
                visteam = tokens[2].strip('"')
            elif tokens[1] == "hometeam":
                hometeam = tokens[2].strip('"')
            elif tokens[1] == "home_score":
                home_score = int(tokens[2])
            elif tokens[1] == "vis_score":
                vis_score = int(tokens[2])

    winner = hometeam if home_score > vis_score else visteam
    game_outcome = {
        "game_id": game_id,
        "visteam": visteam,
        "hometeam": hometeam,
        "home_score": home_score,
        "vis_score": vis_score,
        "winner": winner
    }

    return game_outcome


game_outcomes_list = []
years = range(2012, 2022 + 1)

data_dir = 'data/'

for year in years:
    year_dir = os.path.join(data_dir, str(year) + 'eve')
    event_files = [os.path.join(year_dir, f) for f in os.listdir(
        year_dir) if f.endswith('.EVA') or f.endswith('.EVN')]

    for event_file in event_files:
        game_outcomes_list.append(extract_game_outcome(event_file))

game_outcomes_df = pd.DataFrame(game_outcomes_list)

print(game_outcomes_df.head())