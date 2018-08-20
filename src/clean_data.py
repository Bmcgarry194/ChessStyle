import pandas as pd
import pymongo
import time
from collections import Counter

def games_in_a_month(df, player, month):
    return len(df['games'][player][month][0]['games'])

def is_in_fist_30_days(df, player, month, game):
    '''returns True if game was played within the first 30 days of signing up'''
    seconds_in_a_month = 2629743
    month_from_date_joined = df['joined'][player] + seconds_in_a_month
    time_of_game = df['games'][player][month][0]['games'][game]['end_time']
    
    return month_from_date_joined > time_of_game

def is_in_fourth_month(df, player, month, game):
    '''returns the count of games played in the in the 4th month since sign up'''
    seconds_in_a_month = 2629743
    three_months_from_date_joined = df['joined'][player] + (3 * seconds_in_a_month)
    four_months_from_date_joined = df['joined'][player] + (3.5 * seconds_in_a_month)
    time_of_game = df['games'][player][month][0]['games'][game]['end_time']
    
    return (time_of_game > three_months_from_date_joined) and (time_of_game < four_months_from_date_joined)

def games_in_first_month(df, player, month, game):
    '''returns a count of how many games were played by a user in the first 30 days since signing up'''
    games = 0
    if is_in_fist_30_days(df, player, month, game):
        games += 1
    return games

def rated_games(df, player, month, game):
    '''returns True if game was rated and it was played within the first 30 days of signing up'''
    if is_in_fist_30_days(df, player, month, game):
        return str(df['games'][player][month][0]['games'][game]['rated'])
    else:
        return 'invalid'
    
def time_class_games(df, player, month, game):
    '''returns type of time control if the game was played within the first 30 days'''
    if is_in_fist_30_days(df, player, month, game):
        return df['games'][player][month][0]['games'][game]['time_class']
    else:
        return 'invalid'
    
def rules_games(df, player, month, game):
    '''returns chess variation if the game was played within the first 30 days'''
    if is_in_fist_30_days(df, player, month, game):
        return df['games'][player][month][0]['games'][game]['rules']
    else:
        return 'invalid'
    
def eco_games(df, player, month, game):
    '''returns the eco code for opening played if the game was played in the first 30 days'''
    if is_in_fist_30_days(df, player, month, game):
        return df['games'][player][month][0]['games'][game]['eco'][31:].split('-')[0]
    else:
        return 'invalid'

def results_games(df, player, month, game):
    '''returns the result of the each game played'''
    result_for_white = df['games'][player][month][0]['games'][game]['white']['result']
    result_for_black = df['games'][player][month][0]['games'][game]['black']['result']
    
    if is_in_fist_30_days(df, player, month, game):
        if df['games'][player][month][0]['games'][game]['white']['username'] == df['username'][0]:
            return result_for_white
        else:
            return result_for_black
    else:
        return 'invalid'

def rating_games(df, player, month, game):
    '''returns the result of the each game played'''
    rating_for_white = df['games'][player][month][0]['games'][game]['white']['rating']
    rating_for_black = df['games'][player][month][0]['games'][game]['black']['rating']
    
    if is_in_fist_30_days(df, player, month, game):
        if df['games'][player][month][0]['games'][game]['white']['username'] == df['username'][0]:
            return int(rating_for_white)
        else:
            return int(rating_for_black)
    else:
        return 0

def make_columns(features, df, index):
    '''Counts the appearances of each type of outcome then creates a column in the dataframe corresponding to
    that outcome and filling in the number of occurrences for each player
    Params:
        features: List of each outcome ex: [c, a, a, d, d, a, d, c, j]
        df: pandas dataframe
        index: index to located each player
    '''
    counters = Counter()
    for feature in features:
        counters[feature] += 1

    for counter in counters:
        df.loc[index, counter] = counters[counter]


def parse_games(df):
    '''Pull out stats from the column containing games and add columns to the datafram inplace for the stats
    Params:
        df: pandas dataframe
    '''
    player_idxes = range(df.shape[0])
    for player in player_idxes:
        rated = []
        time_class = []
        rules = []
#         eco = []
        results = []
        ratings = [0,]
        fourth_month_games = 0
        first_month_games = 0
        for month in range(5):
            try:
                for game in range(games_in_a_month(df, player, month)):
                    if is_in_fourth_month(df, player, month, game):
                        fourth_month_games += 1
                    if is_in_fist_30_days(df, player, month, game):
                        first_month_games += 1
                        try:
                            rated.append(rated_games(df, player, month, game))
                        except KeyError:
                            continue
                        try:
                            rules.append(rules_games(df, player, month, game))
                        except KeyError:
                            continue
    #                     try:
    #                         eco.append(eco_games(df, player, month, game))
    #                     except KeyError:
    #                         continue
                        try:
                            results.append(results_games(df, player, month, game))
                        except KeyError:
                            continue
                        try:
                            ratings.append(rating_games(df, player, month, game))
                        except KeyError:
                            continue
                        try:
                            first_month_games += games_in_first_month(df, player, month, game)
                        except KeyError:
                            continue
            except (KeyError, IndexError):
                continue

        df.loc[player, 'fourth_month_games'] = fourth_month_games
        df.loc[player, 'first_month_games'] = first_month_games
        df.loc[player, 'highest_rating'] = max(ratings)
        df.loc[player, 'lowest_rating'] = min(ratings)
#         df.loc[player, 'minimum_rating'] = min([rating for rating in ratings if rating > 0])
        
        make_columns(rated, df, player)
        make_columns(rules, df, player)
#         make_columns(eco, df, player)
        make_columns(results, df, player)
            
        
def add_features(df):
    '''make all feature columns and target column
    Params:
        df: pandas datafram
    Returns:
        df: dataframe with all feature columns and target column
    '''
    #parse games column
    parse_games(df)
    
    #rename True and False columns to rated and unrated
    df.rename(columns={'True': 'rated', 'False': 'unrated'}, inplace=True)

    #create inactive column (1 = inactive, 0 = active) inactive if they have not played a game in the fourth month since signup
    df['inactive'] = df['fourth_month_games'].apply(lambda x: 1 if x == 0 else 0)

    #create columns has_name, has_location, has_avatar
    df['has_name'] = df['name'].apply(lambda x: 0 if x != x else 1)
    df['has_location'] = df['location'].apply(lambda x: 0 if x != x else 1)
    df['has_avatar'] = df['avatar'].apply(lambda x: 0 if x != x else 1)

    #make a basic account type column
    df['is_basic'] = df['status'].apply(lambda x: 1 if x == 'basic' else 0)

    #make a premium account type column
    df['is_premium'] = df['status'].apply(lambda x:  1 if x == 'premium' else 0)
    
    #win percentage
#     df['win_percentage'] = df['win'] / df['first_month_games']
    
#     #rated percentage
#     df['rated_percentage'] = df['rated'] / df['first_month_games']
    return df.fillna(0)
    
    
def make_X_y(df):
    '''returns:
            X: all important feature columns
            y: target column, 1 (inactive: less than 2 games played during the last month) or 0 (active)'''
    #assign X and y variables
    y = df['inactive']
    
    X = df[['first_month_games', 'chess', 'resigned', 'checkmated', 'timeout',
       'abandoned', 'timevsinsufficient', 'stalemate', 'insufficient',
       'unrated', 'repetition', 'agreed', 'bughouse', 'crazyhouse',
       'kingofthehill', 'chess960', 'threecheck', 'has_name', 'has_location', 'has_avatar',
       'is_basic', 'is_premium', 'highest_rating']]
    
    return (X, y)

def create_df_from_mongo():
    mc = pymongo.MongoClient()  # Connect to the MongoDB server using default settings
    db = mc['chess_predictions']  # Use (or create) a database called 'chess_predictions'

    print('import data from mongoDB to pandas dataframe')
    
    #get data from mongoDB and put into dataframe
    df = pd.DataFrame(list(db['players'].find()))

    #remove duplicate users by player_id
    df.drop_duplicates(subset='player_id', inplace=True)

    # #reset the index
    df.reset_index(drop=True, inplace=True)
    
    return df
