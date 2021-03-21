from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)

def get_team_id(team_name_abb):
    try:
        nba_teams = teams.get_teams()
        team_ = [team for team in nba_teams if team['full_name'] == team_name_abb][0]
        team_id = team_['id']
        return team_id
    except:
        return "No data found"


def get_team_all_games(team_id):
    try:

        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
        games = gamefinder.get_data_frames()[0]
        print(games)
        if (len(games) == 0):
            return "No data found"
        return games

    except:
        return "No data found"


def convert_season_id_for_games(games):
    def convert_season_id(x):
        return x[-4:]

    try:

        games['SEASON_ID'] = games['SEASON_ID'].apply(lambda x: convert_season_id(x))
        return games

    except:

        return "No data found"


def get_last_n_seasons_of_team(games):
    try:
        season_records_df = games.groupby(games.SEASON_ID.str[-4:])[['GAME_ID']].count().loc[:]
        total_number_of_seasons = len(season_records_df.index)

        if (total_number_of_seasons >= 5):

            season_records_df = season_records_df.tail(5)

            seasons_record = season_records_df.index.tolist()

            games = games[(games['SEASON_ID'] == seasons_record[0]) | (games['SEASON_ID'] == seasons_record[1]) | (
                        games['SEASON_ID'] == seasons_record[2]) | (games['SEASON_ID'] == seasons_record[3]) | (
                                      games['SEASON_ID'] == seasons_record[4])]

            return games, 5

        elif (total_number_of_seasons >= 5):

            season_records_df = season_records_df.tail(3)

            seasons_record = season_records_df.index.tolist()

            games = games[(games['SEASON_ID'] == seasons_record[0]) | (games['SEASON_ID'] == seasons_record[1]) | (
                        games['SEASON_ID'] == seasons_record[2])]

            return games, 3

        else:

            return "No data found"


    except:
        return "No data found"


def preprocessed_data_for_neural_network(games):
    processed_data = games
    processed_data.drop(labels=['SEASON_ID','TEAM_ID','TEAM_ABBREVIATION','TEAM_NAME','TEAM_NAME','GAME_ID','GAME_DATE','MATCHUP','WL'],axis=1,inplace=True)
    processed_data.dropna(axis=0,inplace=True)
    return processed_data

# team_id = get_team_id("Los Angeles Lakers")
# games_home = get_team_all_games(team_id)
# games_home = convert_season_id_for_games(games_home)
# games_home,number_of_considered_seasons = get_last_n_seasons_of_team(games_home)
# processed_data_home = preprocessed_data_for_neural_network(games_home)
# processed_data_home

team_id = get_team_id("Golden State Warriors")
games_away = get_team_all_games(team_id)
print(games_away)
games_away = convert_season_id_for_games(games_away)
games_away,number_of_considered_seasons = get_last_n_seasons_of_team(games_away)
processed_data_away = preprocessed_data_for_neural_network(games_away)
print(processed_data_away)