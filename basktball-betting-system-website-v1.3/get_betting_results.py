from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import plaidml.keras
plaidml.keras.install_backend()
# import os
# os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import tensorflow as tf
import keras
from keras import backend as k
import numpy as np
# tf.random.set_seed(1)
from tensorflow.python.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor


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

        else:

            return "No data found"


    except:
        return "No data found"


def preprocessed_data_for_neural_network(games):
    try:
        processed_data = games
        processed_data.drop(labels=['TEAM_ID','TEAM_ABBREVIATION','TEAM_NAME','TEAM_NAME','GAME_ID','GAME_DATE','MATCHUP','WL'],axis=1,inplace=True)
        processed_data.dropna(axis=0,inplace=True)
        return processed_data
    except:
        return "No data found"


def train_nerual_network(games_home, games_away):
    try:
        final_df = pd.concat([games_home, games_away], axis=0, ignore_index=True)
        
        final_df = final_df.sample(frac=1,).reset_index(drop=True)
        target = final_df[['PTS']]
        final_df.drop(labels=['SEASON_ID', 'PTS', 'MIN', 'PLUS_MINUS'], axis=1, inplace=True)
        features = final_df
        X_train, X_val, y_train, y_val = train_test_split(features, target, test_size=0.20)
        y_train = np.reshape(y_train, (-1, 1))
        y_val = np.reshape(y_val, (-1, 1))

        model = Sequential()
        model.add(Dense(17, input_dim=17, kernel_initializer='normal', activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.summary()
        model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
        history = model.fit(X_train, y_train, epochs=1000, batch_size=500, verbose=1, validation_split=0.2)
        predictions = model.predict(X_val)

        accuracy = mean_squared_error(y_val, predictions)
        print("MSE ", accuracy)
        return model

    except Exception as e:
        print(e)
        return "No data found"




def train_nerual_network_for_score(last_season_home, last_season_away):

    try:
        last_season_home.drop(labels=['SEASON_ID', 'MIN', 'PLUS_MINUS'],axis=1,inplace=True)
        last_season_away.drop(labels=['SEASON_ID', 'MIN', 'PLUS_MINUS'],axis=1,inplace=True)

        last_season_home.columns = ['PTS_home', 'FGM_home', 'FGA_home', 'FG_PCT_home', 'FG3M_home', 'FG3A_home', 'FG3_PCT_home', 'FTM_home', 'FTA_home',
        'FT_PCT_home', 'OREB_home', 'DREB_home', 'REB_home', 'AST_home', 'STL_home', 'BLK_home', 'TOV_home', 'PF_home']

        last_season_away.columns = ['PTS_away', 'FGM_away', 'FGA_away', 'FG_PCT_away', 'FG3M_away', 'FG3A_away', 'FG3_PCT_away', 'FTM_away', 'FTA_away',
        'FT_PCT_away', 'OREB_away', 'DREB_away', 'REB_away', 'AST_away', 'STL_away', 'BLK_away', 'TOV_away', 'PF_away']


        final_df = pd.concat([last_season_home,last_season_away], axis=1, ignore_index=True)
        final_df.columns = ['PTS_home', 'FGM_home', 'FGA_home', 'FG_PCT_home', 'FG3M_home', 'FG3A_home', 'FG3_PCT_home', 'FTM_home', 'FTA_home',
            'FT_PCT_home', 'OREB_home', 'DREB_home', 'REB_home', 'AST_home', 'STL_home', 'BLK_home', 'TOV_home', 'PF_home','PTS_away', 'FGM_away', 'FGA_away', 'FG_PCT_away', 'FG3M_away', 'FG3A_away', 'FG3_PCT_away', 'FTM_away', 'FTA_away',
            'FT_PCT_away', 'OREB_away', 'DREB_away', 'REB_away', 'AST_away', 'STL_away', 'BLK_away', 'TOV_away', 'PF_away']
    
        final_df.dropna(axis=0,inplace=True)

        final_df_home_features = final_df.drop(labels=['PTS_home'],axis=1)
        final_df_home_target = final_df[['PTS_home']]


        final_df_away_features = final_df.drop(labels=['PTS_away'],axis=1)
        final_df_away_target = final_df[['PTS_away']]
        #**********************************************************#
        X_train, X_val, y_train, y_val = train_test_split(final_df_home_features, final_df_home_target, test_size=0.20)
        y_train = np.reshape(y_train, (-1, 1))
        y_val = np.reshape(y_val, (-1, 1))
        model = Sequential()
        model.add(Dense(35, input_dim=35, kernel_initializer='normal', activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.summary()
        model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
        history = model.fit(X_train, y_train, epochs=1000, batch_size=500, verbose=1, validation_split=0.2)
        predictions = model.predict(X_val)

        # accuracy = mean_squared_error(y_val, predictions)
        # print("MSE ", accuracy)

        
        home_score_model = model

        #**********************************************************************#

        X_train, X_val, y_train, y_val = train_test_split(final_df_away_features, final_df_away_target, test_size=0.20)
        y_train = np.reshape(y_train, (-1, 1))
        y_val = np.reshape(y_val, (-1, 1))
        model = Sequential()
        model.add(Dense(35, input_dim=35, kernel_initializer='normal', activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.summary()
        model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
        history = model.fit(X_train, y_train, epochs=1000, batch_size=500, verbose=1, validation_split=0.2)
        predictions = model.predict(X_val)

        # accuracy = mean_squared_error(y_val, predictions)
        # print("MSE ", accuracy)


        away_score_model = model

        #***********************************************************************#
        # Working of dataframes


        home_score_data = final_df.head(5)
        home_score_df = pd.DataFrame()
        home_score_df['FGM_home'] = [round(home_score_data['FGM_home'].mean(), 0)]
        home_score_df['FGA_home'] = [round(home_score_data['FGA_home'].mean(), 0)]
        home_score_df['FG_PCT_home'] = [home_score_data['FG_PCT_home'].mean()]
        home_score_df['FG3M_home'] = [round(home_score_data['FG3M_home'].mean(), 0)]
        home_score_df['FG3A_home'] = [round(home_score_data['FG3A_home'].mean(), 0)]
        home_score_df['FG3_PCT_home'] = [home_score_data['FG3_PCT_home'].mean()]
        home_score_df['FTM_home'] = [round(home_score_data['FTM_home'].mean(), 0)]
        home_score_df['FTA_home'] = [round(home_score_data['FTA_home'].mean(), 0)]
        home_score_df['FT_PCT_home'] = [home_score_data['FT_PCT_home'].mean()]
        home_score_df['OREB_home'] = [round(home_score_data['OREB_home'].mean(), 0)]
        home_score_df['DREB_home'] = [round(home_score_data['DREB_home'].mean(), 0)]
        home_score_df['REB_home'] = [round(home_score_data['REB_home'].mean(), 0)]
        home_score_df['AST_home'] = [round(home_score_data['AST_home'].mean(), 0)]
        home_score_df['STL_home'] = [round(home_score_data['STL_home'].mean(), 0)]
        home_score_df['BLK_home'] = [round(home_score_data['BLK_home'].mean(), 0)]
        home_score_df['TOV_home'] = [round(home_score_data['TOV_home'].mean(), 0)]
        home_score_df['PF_home'] = [round(home_score_data['PF_home'].mean(), 0)]
        home_score_df['PTS_away'] = [round(home_score_data['PTS_away'].mean(), 0)]
        home_score_df['FGM_away'] = [round(home_score_data['FGM_away'].mean(), 0)]
        home_score_df['FGA_away'] = [round(home_score_data['FGA_away'].mean(), 0)]
        home_score_df['FG_PCT_away'] = [home_score_data['FG_PCT_away'].mean()]
        home_score_df['FG3M_away'] = [round(home_score_data['FG3M_away'].mean(), 0)]
        home_score_df['FG3A_away'] = [round(home_score_data['FG3A_away'].mean(), 0)]
        home_score_df['FG3_PCT_away'] = [home_score_data['FG3_PCT_away'].mean()]
        home_score_df['FTM_away'] = [round(home_score_data['FTM_away'].mean(), 0)]
        home_score_df['FTA_away'] = [round(home_score_data['FTA_away'].mean(), 0)]
        home_score_df['FT_PCT_away'] = [home_score_data['FT_PCT_away'].mean()]
        home_score_df['OREB_away'] = [round(home_score_data['OREB_away'].mean(), 0)]
        home_score_df['DREB_away'] = [round(home_score_data['DREB_away'].mean(), 0)]
        home_score_df['REB_away'] = [round(home_score_data['REB_away'].mean(), 0)]
        home_score_df['AST_away'] = [round(home_score_data['AST_away'].mean(), 0)]
        home_score_df['STL_away'] = [round(home_score_data['STL_away'].mean(), 0)]
        home_score_df['BLK_away'] = [round(home_score_data['BLK_away'].mean(), 0)]
        home_score_df['TOV_away'] = [round(home_score_data['TOV_away'].mean(), 0)]
        home_score_df['PF_away'] = [round(home_score_data['PF_away'].mean(), 0)]

        
        away_score_data = final_df.head(5)
        away_score_df = pd.DataFrame()
        away_score_df['PTS_home'] = [round(away_score_data['PTS_home'].mean(), 0)]
        away_score_df['FGM_home'] = [round(away_score_data['FGM_home'].mean(), 0)]
        away_score_df['FGA_home'] = [round(away_score_data['FGA_home'].mean(), 0)]
        away_score_df['FG_PCT_home'] = [away_score_data['FG_PCT_home'].mean()]
        away_score_df['FG3M_home'] = [round(away_score_data['FG3M_home'].mean(), 0)]
        away_score_df['FG3A_home'] = [round(away_score_data['FG3A_home'].mean(), 0)]
        away_score_df['FG3_PCT_home'] = [away_score_data['FG3_PCT_home'].mean()]
        away_score_df['FTM_home'] = [round(away_score_data['FTM_home'].mean(), 0)]
        away_score_df['FTA_home'] = [round(away_score_data['FTA_home'].mean(), 0)]
        away_score_df['FT_PCT_home'] = [away_score_data['FT_PCT_home'].mean()]
        away_score_df['OREB_home'] = [round(away_score_data['OREB_home'].mean(), 0)]
        away_score_df['DREB_home'] = [round(away_score_data['DREB_home'].mean(), 0)]
        away_score_df['REB_home'] = [round(away_score_data['REB_home'].mean(), 0)]
        away_score_df['AST_home'] = [round(away_score_data['AST_home'].mean(), 0)]
        away_score_df['STL_home'] = [round(away_score_data['STL_home'].mean(), 0)]
        away_score_df['BLK_home'] = [round(away_score_data['BLK_home'].mean(), 0)]
        away_score_df['TOV_home'] = [round(away_score_data['TOV_home'].mean(), 0)]
        away_score_df['PF_home'] = [round(away_score_data['PF_home'].mean(), 0)]
        away_score_df['FGM_away'] = [round(away_score_data['FGM_away'].mean(), 0)]
        away_score_df['FGA_away'] = [round(away_score_data['FGA_away'].mean(), 0)]
        away_score_df['FG_PCT_away'] = [away_score_data['FG_PCT_away'].mean()]
        away_score_df['FG3M_away'] = [round(away_score_data['FG3M_away'].mean(), 0)]
        away_score_df['FG3A_away'] = [round(away_score_data['FG3A_away'].mean(), 0)]
        away_score_df['FG3_PCT_away'] = [away_score_data['FG3_PCT_away'].mean()]
        away_score_df['FTM_away'] = [round(away_score_data['FTM_away'].mean(), 0)]
        away_score_df['FTA_away'] = [round(away_score_data['FTA_away'].mean(), 0)]
        away_score_df['FT_PCT_away'] = [away_score_data['FT_PCT_away'].mean()]
        away_score_df['OREB_away'] = [round(away_score_data['OREB_away'].mean(), 0)]
        away_score_df['DREB_away'] = [round(away_score_data['DREB_away'].mean(), 0)]
        away_score_df['REB_away'] = [round(away_score_data['REB_away'].mean(), 0)]
        away_score_df['AST_away'] = [round(away_score_data['AST_away'].mean(), 0)]
        away_score_df['STL_away'] = [round(away_score_data['STL_away'].mean(), 0)]
        away_score_df['BLK_away'] = [round(away_score_data['BLK_away'].mean(), 0)]
        away_score_df['TOV_away'] = [round(away_score_data['TOV_away'].mean(), 0)]
        away_score_df['PF_away'] = [round(away_score_data['PF_away'].mean(), 0)]
        
        home_score_points = home_score_model.predict(home_score_df)
        away_score_points = away_score_model.predict(away_score_df)
        return home_score_points,away_score_points

    except Exception as e:
        print(e)
        return "No data found" , "No data found"

    

def accumulate_n_season_stats_for_betting(games_home, games_away, number_of_considered_seasons_home,
                                          number_of_considered_seasons_away, model):
    try:
        number_of_considered_seasons = 0
        if (number_of_considered_seasons_away == number_of_considered_seasons_home):

            number_of_considered_seasons = number_of_considered_seasons_home
            s1_home, s2_home, s3_home, s4_home, s5_home = preprocess_data_for_betting(games_home,
                                                                                      number_of_considered_seasons)
            s1_away, s2_away, s3_away, s4_away, s5_away = preprocess_data_for_betting(games_away,
                                                                                      number_of_considered_seasons)

            last_2_seasons_home = pd.concat([s1_home, s2_home], axis=0, ignore_index=True)
            last_2_seasons_avg_home = pd.DataFrame()
            last_2_seasons_avg_home['FGM'] = [round(last_2_seasons_home['FGM'].mean(), 0)]
            last_2_seasons_avg_home['FGA'] = [round(last_2_seasons_home['FGA'].mean(), 0)]
            last_2_seasons_avg_home['FG_PCT'] = [last_2_seasons_home['FG_PCT'].mean()]
            last_2_seasons_avg_home['FG3M'] = [round(last_2_seasons_home['FG3M'].mean(), 0)]
            last_2_seasons_avg_home['FG3A'] = [round(last_2_seasons_home['FG3A'].mean(), 0)]
            last_2_seasons_avg_home['FG3_PCT'] = [last_2_seasons_home['FG3_PCT'].mean()]
            last_2_seasons_avg_home['FTM'] = [round(last_2_seasons_home['FTM'].mean(), 0)]
            last_2_seasons_avg_home['FTA'] = [round(last_2_seasons_home['FTA'].mean(), 0)]
            last_2_seasons_avg_home['FT_PCT'] = [last_2_seasons_home['FT_PCT'].mean()]
            last_2_seasons_avg_home['OREB'] = [round(last_2_seasons_home['OREB'].mean(), 0)]
            last_2_seasons_avg_home['DREB'] = [round(last_2_seasons_home['DREB'].mean(), 0)]
            last_2_seasons_avg_home['REB'] = [round(last_2_seasons_home['REB'].mean(), 0)]
            last_2_seasons_avg_home['AST'] = [round(last_2_seasons_home['AST'].mean(), 0)]
            last_2_seasons_avg_home['STL'] = [round(last_2_seasons_home['STL'].mean(), 0)]
            last_2_seasons_avg_home['BLK'] = [round(last_2_seasons_home['BLK'].mean(), 0)]
            last_2_seasons_avg_home['TOV'] = [round(last_2_seasons_home['TOV'].mean(), 0)]
            last_2_seasons_avg_home['PF'] = [round(last_2_seasons_home['PF'].mean(), 0)]

            last_2_seasons_away = pd.concat([s1_away, s2_away], axis=0, ignore_index=True)
            last_2_seasons_avg_away = pd.DataFrame()
            last_2_seasons_avg_away['FGM'] = [round(last_2_seasons_away['FGM'].mean(), 0)]
            last_2_seasons_avg_away['FGA'] = [round(last_2_seasons_away['FGA'].mean(), 0)]
            last_2_seasons_avg_away['FG_PCT'] = [last_2_seasons_away['FG_PCT'].mean()]
            last_2_seasons_avg_away['FG3M'] = [round(last_2_seasons_away['FG3M'].mean(), 0)]
            last_2_seasons_avg_away['FG3A'] = [round(last_2_seasons_away['FG3A'].mean(), 0)]
            last_2_seasons_avg_away['FG3_PCT'] = [last_2_seasons_away['FG3_PCT'].mean()]
            last_2_seasons_avg_away['FTM'] = [round(last_2_seasons_away['FTM'].mean(), 0)]
            last_2_seasons_avg_away['FTA'] = [round(last_2_seasons_away['FTA'].mean(), 0)]
            last_2_seasons_avg_away['FT_PCT'] = [last_2_seasons_away['FT_PCT'].mean()]
            last_2_seasons_avg_away['OREB'] = [round(last_2_seasons_away['OREB'].mean(), 0)]
            last_2_seasons_avg_away['DREB'] = [round(last_2_seasons_away['DREB'].mean(), 0)]
            last_2_seasons_avg_away['REB'] = [round(last_2_seasons_away['REB'].mean(), 0)]
            last_2_seasons_avg_away['AST'] = [round(last_2_seasons_away['AST'].mean(), 0)]
            last_2_seasons_avg_away['STL'] = [round(last_2_seasons_away['STL'].mean(), 0)]
            last_2_seasons_avg_away['BLK'] = [round(last_2_seasons_away['BLK'].mean(), 0)]
            last_2_seasons_avg_away['TOV'] = [round(last_2_seasons_away['TOV'].mean(), 0)]
            last_2_seasons_avg_away['PF'] = [round(last_2_seasons_away['PF'].mean(), 0)]

            last_3_matches_of_last_season_home = s1_home.head(3)
            last_3_matches_of_last_season_avg_home = pd.DataFrame()
            last_3_matches_of_last_season_avg_home['FGM'] = [round(last_3_matches_of_last_season_home['FGM'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['FGA'] = [round(last_3_matches_of_last_season_home['FGA'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['FG_PCT'] = [last_3_matches_of_last_season_home['FG_PCT'].mean()]
            last_3_matches_of_last_season_avg_home['FG3M'] = [
                round(last_3_matches_of_last_season_home['FG3M'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['FG3A'] = [
                round(last_3_matches_of_last_season_home['FG3A'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['FG3_PCT'] = [last_3_matches_of_last_season_home['FG3_PCT'].mean()]
            last_3_matches_of_last_season_avg_home['FTM'] = [round(last_3_matches_of_last_season_home['FTM'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['FTA'] = [round(last_3_matches_of_last_season_home['FTA'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['FT_PCT'] = [last_3_matches_of_last_season_home['FT_PCT'].mean()]
            last_3_matches_of_last_season_avg_home['OREB'] = [
                round(last_3_matches_of_last_season_home['OREB'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['DREB'] = [
                round(last_3_matches_of_last_season_home['DREB'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['REB'] = [round(last_3_matches_of_last_season_home['REB'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['AST'] = [round(last_3_matches_of_last_season_home['AST'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['STL'] = [round(last_3_matches_of_last_season_home['STL'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['BLK'] = [round(last_3_matches_of_last_season_home['BLK'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['TOV'] = [round(last_3_matches_of_last_season_home['TOV'].mean(), 0)]
            last_3_matches_of_last_season_avg_home['PF'] = [round(last_3_matches_of_last_season_home['PF'].mean(), 0)]

            last_3_matches_of_last_season_away = s1_away.head(3)
            last_3_matches_of_last_season_avg_away = pd.DataFrame()
            last_3_matches_of_last_season_avg_away['FGM'] = [round(last_3_matches_of_last_season_away['FGM'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['FGA'] = [round(last_3_matches_of_last_season_away['FGA'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['FG_PCT'] = [last_3_matches_of_last_season_away['FG_PCT'].mean()]
            last_3_matches_of_last_season_avg_away['FG3M'] = [
                round(last_3_matches_of_last_season_away['FG3M'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['FG3A'] = [
                round(last_3_matches_of_last_season_away['FG3A'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['FG3_PCT'] = [last_3_matches_of_last_season_away['FG3_PCT'].mean()]
            last_3_matches_of_last_season_avg_away['FTM'] = [round(last_3_matches_of_last_season_away['FTM'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['FTA'] = [round(last_3_matches_of_last_season_away['FTA'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['FT_PCT'] = [last_3_matches_of_last_season_away['FT_PCT'].mean()]
            last_3_matches_of_last_season_avg_away['OREB'] = [
                round(last_3_matches_of_last_season_away['OREB'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['DREB'] = [
                round(last_3_matches_of_last_season_away['DREB'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['REB'] = [round(last_3_matches_of_last_season_away['REB'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['AST'] = [round(last_3_matches_of_last_season_away['AST'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['STL'] = [round(last_3_matches_of_last_season_away['STL'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['BLK'] = [round(last_3_matches_of_last_season_away['BLK'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['TOV'] = [round(last_3_matches_of_last_season_away['TOV'].mean(), 0)]
            last_3_matches_of_last_season_avg_away['PF'] = [round(last_3_matches_of_last_season_away['PF'].mean(), 0)]

            last_2_matches_of_last_season_home = s1_home.head(5)
            last_2_matches_of_last_season_avg_home = pd.DataFrame()
            last_2_matches_of_last_season_avg_home['FGM'] = [round(last_2_matches_of_last_season_home['FGM'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['FGA'] = [round(last_2_matches_of_last_season_home['FGA'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['FG_PCT'] = [last_2_matches_of_last_season_home['FG_PCT'].mean()]
            last_2_matches_of_last_season_avg_home['FG3M'] = [
                round(last_2_matches_of_last_season_home['FG3M'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['FG3A'] = [
                round(last_2_matches_of_last_season_home['FG3A'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['FG3_PCT'] = [last_2_matches_of_last_season_home['FG3_PCT'].mean()]
            last_2_matches_of_last_season_avg_home['FTM'] = [round(last_2_matches_of_last_season_home['FTM'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['FTA'] = [round(last_2_matches_of_last_season_home['FTA'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['FT_PCT'] = [last_2_matches_of_last_season_home['FT_PCT'].mean()]
            last_2_matches_of_last_season_avg_home['OREB'] = [
                round(last_2_matches_of_last_season_home['OREB'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['DREB'] = [
                round(last_2_matches_of_last_season_home['DREB'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['REB'] = [round(last_2_matches_of_last_season_home['REB'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['AST'] = [round(last_2_matches_of_last_season_home['AST'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['STL'] = [round(last_2_matches_of_last_season_home['STL'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['BLK'] = [round(last_2_matches_of_last_season_home['BLK'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['TOV'] = [round(last_2_matches_of_last_season_home['TOV'].mean(), 0)]
            last_2_matches_of_last_season_avg_home['PF'] = [round(last_2_matches_of_last_season_home['PF'].mean(), 0)]

            last_2_matches_of_last_season_away = s1_away.head(5)
            last_2_matches_of_last_season_avg_away = pd.DataFrame()
            last_2_matches_of_last_season_avg_away['FGM'] = [round(last_2_matches_of_last_season_away['FGM'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['FGA'] = [round(last_2_matches_of_last_season_away['FGA'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['FG_PCT'] = [last_2_matches_of_last_season_away['FG_PCT'].mean()]
            last_2_matches_of_last_season_avg_away['FG3M'] = [
                round(last_2_matches_of_last_season_away['FG3M'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['FG3A'] = [
                round(last_2_matches_of_last_season_away['FG3A'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['FG3_PCT'] = [last_2_matches_of_last_season_away['FG3_PCT'].mean()]
            last_2_matches_of_last_season_avg_away['FTM'] = [round(last_2_matches_of_last_season_away['FTM'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['FTA'] = [round(last_2_matches_of_last_season_away['FTA'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['FT_PCT'] = [last_2_matches_of_last_season_away['FT_PCT'].mean()]
            last_2_matches_of_last_season_avg_away['OREB'] = [
                round(last_2_matches_of_last_season_away['OREB'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['DREB'] = [
                round(last_2_matches_of_last_season_home['DREB'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['REB'] = [round(last_2_matches_of_last_season_away['REB'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['AST'] = [round(last_2_matches_of_last_season_away['AST'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['STL'] = [round(last_2_matches_of_last_season_away['STL'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['BLK'] = [round(last_2_matches_of_last_season_away['BLK'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['TOV'] = [round(last_2_matches_of_last_season_away['TOV'].mean(), 0)]
            last_2_matches_of_last_season_avg_away['PF'] = [round(last_2_matches_of_last_season_away['PF'].mean(), 0)]

            s1_home_pred = model.predict(s1_home)
            s2_home_pred = model.predict(s2_home)
            s3_home_pred = model.predict(s3_home)
            s4_home_pred = model.predict(s4_home)
            s5_home_pred = model.predict(s5_home)

            s1_away_pred = model.predict(s1_away)
            s2_away_pred = model.predict(s2_away)
            s3_away_pred = model.predict(s3_away)
            s4_away_pred = model.predict(s4_away)
            s5_away_pred = model.predict(s5_away)

            last_2_season_home_pred = model.predict(last_2_seasons_avg_home)
            last_2_season_away_pred = model.predict(last_2_seasons_avg_away)

            last_3_matches_of_last_season_home_pred = model.predict(last_3_matches_of_last_season_avg_home)
            last_3_matches_of_last_season_away_pred = model.predict(last_3_matches_of_last_season_avg_away)

            last_2_matches_of_last_season_home_pred = model.predict(last_2_matches_of_last_season_avg_home)
            last_2_matches_of_last_season_away_pred = model.predict(last_2_matches_of_last_season_avg_away)


            s1_winner = 0
            s2_winner = 0
            s3_winner = 0
            s4_winner = 0
            s5_winner = 0
            last_2_season_winner = 0
            last_3_matches_of_last_season_winner = 0

            if (s1_home_pred[0][0] > s1_away_pred[0][0]):
                s1_winner = 1

            if (s2_home_pred[0][0] > s2_away_pred[0][0]):
                s2_winner = 1

            if (s3_home_pred[0][0] > s3_away_pred[0][0]):
                s3_winner = 1

            if (s4_home_pred[0][0] > s4_away_pred[0][0]):
                s4_winner = 1

            if (s5_home_pred[0][0] > s5_away_pred[0][0]):
                s5_winner = 1

            if (last_2_season_home_pred[0][0] > last_2_season_away_pred[0][0]):
                last_2_season_winner = 1

            if (last_3_matches_of_last_season_home_pred[0][0] > last_3_matches_of_last_season_away_pred[0][0]):
                last_3_matches_of_last_season_winner = 1


            return [s1_winner, s2_winner, s3_winner, s4_winner, s5_winner, last_2_season_winner,
                    last_3_matches_of_last_season_winner],last_2_matches_of_last_season_home_pred[0][0],last_2_matches_of_last_season_away_pred[0][0]

        else:

            

            return "No data found"


    except Exception as e:
        print(e)
        return "No data found"


def get_average_of_x_season(games, season_id):
    try:

        # getting average of particulr "x" season
        season = pd.DataFrame()
        season['FGM'] = [round(games[games['SEASON_ID'] == season_id]['FGM'].mean(), 0)]
        season['FGA'] = [round(games[games['SEASON_ID'] == season_id]['FGA'].mean(), 0)]
        season['FG_PCT'] = [games[games['SEASON_ID'] == season_id]['FG_PCT'].mean()]
        season['FG3M'] = [round(games[games['SEASON_ID'] == season_id]['FG3M'].mean(), 0)]
        season['FG3A'] = [round(games[games['SEASON_ID'] == season_id]['FG3A'].mean(), 0)]
        season['FG3_PCT'] = [games[games['SEASON_ID'] == season_id]['FG3_PCT'].mean()]
        season['FTM'] = [round(games[games['SEASON_ID'] == season_id]['FTM'].mean(), 0)]
        season['FTA'] = [round(games[games['SEASON_ID'] == season_id]['FTA'].mean(), 0)]
        season['FT_PCT'] = [games[games['SEASON_ID'] == season_id]['FT_PCT'].mean()]
        season['OREB'] = [round(games[games['SEASON_ID'] == season_id]['OREB'].mean(), 0)]
        season['DREB'] = [round(games[games['SEASON_ID'] == season_id]['DREB'].mean(), 0)]
        season['REB'] = [round(games[games['SEASON_ID'] == season_id]['REB'].mean(), 0)]
        season['AST'] = [round(games[games['SEASON_ID'] == season_id]['AST'].mean(), 0)]
        season['STL'] = [round(games[games['SEASON_ID'] == season_id]['STL'].mean(), 0)]
        season['BLK'] = [round(games[games['SEASON_ID'] == season_id]['BLK'].mean(), 0)]
        season['TOV'] = [round(games[games['SEASON_ID'] == season_id]['TOV'].mean(), 0)]
        season['PF'] = [round(games[games['SEASON_ID'] == season_id]['PF'].mean(), 0)]

        return season

    except:

        return "No data found"


def preprocess_data_for_betting(games, number_of_considered_seasons):
    try:

        unique_seasons = games['SEASON_ID'].unique()
        unique_seasons = unique_seasons[0:number_of_considered_seasons]

        # getting average of particulr "x" season
        if (len(unique_seasons) == 5):

            last_season_avg = get_average_of_x_season(games, unique_seasons[0])
            second_last_season_avg = get_average_of_x_season(games, unique_seasons[1])
            third_last_season_avg = get_average_of_x_season(games, unique_seasons[2])
            fourth_last_season_avg = get_average_of_x_season(games, unique_seasons[3])
            fifth_last_season_avg = get_average_of_x_season(games, unique_seasons[4])

            return last_season_avg, second_last_season_avg, third_last_season_avg, fourth_last_season_avg, fifth_last_season_avg

        else:

             return "No data found"

    except:

        return "No data found"



def get_betting_results(home_team_name,away_team_name):

    try:
        team_id_home = get_team_id(home_team_name)
        if(team_id_home=="No data found"):

            return "No data found"

        games_home = get_team_all_games(team_id_home)
        games_home = convert_season_id_for_games(games_home)

        if(type(games_home)==str):

            return "No data found"
        
        games_home, number_of_considered_seasons_home = get_last_n_seasons_of_team(games_home)

        if(type(games_home)==str):

            return "No data found"

        processed_data_home = preprocessed_data_for_neural_network(games_home)

        if(type(processed_data_home)==str):

            return "No data found"

        team_id_away = get_team_id(away_team_name)

        if(team_id_away=="No data found"):

            return "No data found"

        games_away = get_team_all_games(team_id_away)
        games_away = convert_season_id_for_games(games_away)

        if(type(games_away)==str):

            return "No data found"

        games_away, number_of_considered_seasons_away = get_last_n_seasons_of_team(games_away)

        if(type(games_away)==str):

            return "No data found"

        processed_data_away = preprocessed_data_for_neural_network(games_away)

        if(type(processed_data_away)==str):

            return "No data found"
        
        # points_home , points_away = train_nerual_network_for_score(processed_data_home,processed_data_away)
       
        # if(type(points_home)==str):
        #     return "No data found"
    
        # points_home = points_home.tolist()
        # points_away = points_away.tolist()

        home_data_for_score = processed_data_home.copy(deep=True)
        away_data_for_score = processed_data_away.copy(deep=True)

        model_1 = train_nerual_network(processed_data_home, processed_data_away)
        model_2 = train_nerual_network(processed_data_home, processed_data_away)
        model_3 = train_nerual_network(processed_data_home, processed_data_away)
        model_4 = train_nerual_network(processed_data_home, processed_data_away)
        model_5 = train_nerual_network(processed_data_home, processed_data_away)

        points_home , points_away = train_nerual_network_for_score(home_data_for_score,away_data_for_score)
       
        if(type(points_home)==str):
            return "No data found"

        print("\n\n\n\n\n Done \n\n\n\n\n")

        result_1,h1_score,a1_score = accumulate_n_season_stats_for_betting(games_home, games_away, number_of_considered_seasons_home,
                                                         number_of_considered_seasons_away, model_1)
        result_2,h2_score,a2_score = accumulate_n_season_stats_for_betting(games_home, games_away, number_of_considered_seasons_home,
                                                         number_of_considered_seasons_away, model_2)
        result_3,h3_score,a3_score = accumulate_n_season_stats_for_betting(games_home, games_away, number_of_considered_seasons_home,
                                                         number_of_considered_seasons_away, model_3)
        result_4,h4_score,a4_score = accumulate_n_season_stats_for_betting(games_home, games_away, number_of_considered_seasons_home,
                                                         number_of_considered_seasons_away, model_4)
        result_5,h5_score,a5_score = accumulate_n_season_stats_for_betting(games_home, games_away, number_of_considered_seasons_home,
                                                         number_of_considered_seasons_away, model_5)

        result_stack = []

        limit = len(result_1)
        if(limit==7):
            r_1_home_count = result_1.count(1)
            r_1_away_count = result_1.count(0)

            r_2_home_count = result_2.count(1)
            r_2_away_count = result_2.count(0)


            r_3_home_count = result_3.count(1)
            r_3_away_count = result_3.count(0)

            r_4_home_count = result_4.count(1)
            r_4_away_count = result_4.count(0)

            r_5_home_count = result_5.count(1)
            r_5_away_count = result_5.count(0)


            if(r_1_home_count>r_1_away_count):
                result_stack.append(1)
            else:
                result_stack.append(0)

            if (r_2_home_count > r_2_away_count):
                result_stack.append(1)
            else:
                result_stack.append(0)

            if (r_3_home_count > r_3_away_count):
                result_stack.append(1)
            else:
                result_stack.append(0)

            if (r_4_home_count > r_4_away_count):
                result_stack.append(1)
            else:
                result_stack.append(0)

            if (r_5_home_count > r_5_away_count):
                result_stack.append(1)
            else:
                result_stack.append(0)

            h_c = result_stack.count(1)
            a_c = result_stack.count(0)

            home_team_winning_chances = (h_c/5)*100
            away_team_winning_chances = (a_c/5)*100

      

            home_team_score_points_est = round((h1_score+h2_score+h3_score+h4_score+h5_score)/5,0)
            away_team_score_points_est = round((a1_score+a2_score+a3_score+a4_score+a5_score)/5,0)

          

            if(home_team_winning_chances>away_team_winning_chances):
                model_1_h_points = result_1.count(1)
                model_2_h_points = result_2.count(1)
                model_3_h_points = result_3.count(1)
                model_4_h_points = result_4.count(1)
                model_5_h_points = result_5.count(1)

                model_1_h_points_percentage = round((model_1_h_points/7)*100,0)
                model_2_h_points_percentage = round((model_2_h_points/7)*100,0)
                model_3_h_points_percentage = round((model_3_h_points/7)*100,0)
                model_4_h_points_percentage = round((model_4_h_points/7)*100,0)
                model_5_h_points_percentage = round((model_5_h_points/7)*100,0)

                avg_home_chance = round((model_1_h_points_percentage + model_2_h_points_percentage + model_3_h_points_percentage + model_4_h_points_percentage + model_5_h_points_percentage)/5,0)
                avg_away_chance = 100 - avg_home_chance

              

                if(points_home>points_away):
                    
                    return [int(avg_home_chance),int(avg_away_chance),int(round(points_home[0][0],0)),int(round(points_away[0][0],0))]
                else:
                
                    return [int(avg_home_chance),int(avg_away_chance),int(round(points_away[0][0],0)),int(round(points_home[0][0],0))]

            else:

                model_1_a_points = result_1.count(0)
                model_2_a_points = result_2.count(0)
                model_3_a_points = result_3.count(0)
                model_4_a_points = result_4.count(0)
                model_5_a_points = result_5.count(0)

                model_1_a_points_percentage = round((model_5_a_points/7)*100,0)
                model_2_a_points_percentage = round((model_5_a_points/7)*100,0)
                model_3_a_points_percentage = round((model_5_a_points/7)*100,0)
                model_4_a_points_percentage = round((model_5_a_points/7)*100,0)
                model_5_a_points_percentage = round((model_5_a_points/7)*100,0)


                avg_away_chance = round((model_1_a_points_percentage + model_2_a_points_percentage + model_3_a_points_percentage + model_4_a_points_percentage + model_5_a_points_percentage)/5,0)
                avg_home_chance = 100 - avg_away_chance

                

                if(points_away>points_home):
                   
                    return [int(avg_home_chance),int(avg_away_chance),int(round(points_home[0][0],0)),int(round(points_away[0][0],0))]
                else:
                    
                    return [int(avg_home_chance),int(avg_away_chance),int(round(points_away[0][0],0)),int(round(points_home[0][0],0))]
        
        else:
            return "No data found"
        # '''
    except:
        return "No data found"

