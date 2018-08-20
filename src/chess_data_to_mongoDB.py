import json
from sys import argv
import random
import datetime
import requests
import time
import pandas as pd
import pymongo
from collections import Counter

def get_player_ids_by_country(country):
    '''use the country's 2-character ISO 3166 code (capitalized) to specify which country you want data
       for example: United States = US'''

    url = f'https://api.chess.com/pub/country/{country}/players'
    response = requests.get(url)

    #check if the request worked
    assert response.status_code == 200

    #convert from bytes to utf-8, then to json then pull the names from the dict
    return json.loads(response.content.decode('utf-8'))['players']

def date_joined(username, datetype='epoch'):
    '''returns the date the user joined in epoch time by default, human readable date is returned if datetype=readable'''

    try:
        response = requests.get(f'https://api.chess.com/pub/player/{username}')
        profile = json.loads(response.content.decode('utf-8'))
        if datetype == 'epoch':
            return profile['joined']
        elif datetype == 'readable':
            return datetime.datetime.fromtimestamp(profile['joined']).strftime('%c')
    except:
        return -1

def list_of_players(country, start, end, num_of_players):
    '''use the country's 2-character ISO 3166 code (capitalized) to specify which country you want data from
    Params:
         country: country from which players will be selected ex: US (use the country's 2-character ISO 3166 code (capitalized))
         start: select players who signed up after this date in epoch time ex: 1514764800 (jan 1st, 2018)
         end: select players who signed up before this date in epoch time ex: 1517443200 (feb 1st, 2018)
         num_of_players: amount of players to analyze
    '''

    #random pick from list of usernames
    player_list = random.shuffle(get_player_ids_by_country(country))

    players = []

    for player in player_list:
        # player_count = 0
        joined = date_joined(player)
        if player_count == num_of_players:
            break
        elif (joined > start) and joined < end:
            player_count += 1
            players.append(player)
            # yield player
    return players

def get_player_profile(username):
    try:
        response = requests.get(f'https://api.chess.com/pub/player/{username}')
        return json.loads(response.content.decode('utf-8'))
    except:
        return []

def get_player_stats(username):
    try:
        response = requests.get(f'https://api.chess.com/pub/player/{username}/stats')
        return json.loads(response.content.decode('utf-8'))
    except:
        return []

def get_player_games(username, year='2018'):
    '''return a list of lists where each list contains the games played each month of January through May 2018'''

    months = ['01', '02', '03', '04', '05']
    month_games = []
    for month in months:
        try:
            response = requests.get(f'https://api.chess.com/pub/player/{username}/games/{year}/{month}')
            month_games.append([json.loads(response.content.decode('utf-8'))])
        except KeyError:
            continue
    return month_games

def player_data_to_mongoDB(username, mongoDB_connection, database, collection):

    mc = mongoDB_connection

    #use/create a database
    db = mc[database]

    #use/create a collection
    collection = db[collection]

    #query Chess.com api for data
    profile = get_player_profile(username)
    stats = get_player_stats(username)
    games = get_player_games(username)

    #insert player data into database
    collection.insert_one({**profile,
                           **stats,
                           'games': games
                            })

def all_player_data_to_mongoDB(players, mongoDB_connection, database, collection, verbose=True):
    '''insert all player data into a mongoDB
       Params:
          players: list of player names
          mongoDB_connection: open connection to database ex. pymongo.MongoClient()
          database: name of database
          collection: name of collection
       Keyword Args:
          verbose: if True print player name after each insert, default is False
    '''
    # print(f'importing to {database} database and {collection} collection)
    for player in players:
        player_data_to_mongoDB(player, mongoDB_connection, database, collection)
        if verbose:
            print(player)
    print('All player data inserted into database')

if __name__ == "__main__":
    all_player_data_to_mongoDB(list_of_players('US', 1514764800, 1517443200, 10), pymongo.MongoClient(), 'chess_predictions', 'test')
