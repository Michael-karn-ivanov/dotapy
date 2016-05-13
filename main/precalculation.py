from elo.elo import Rating
from elo.elo import Elo
__author__ = 'mivanov'

import pandas
import numpy as np
import os
import datetime

class PreCalculation:
    WIN_BET = 'win'
    CUMULATIVE_BET = 'cumulative'

    def __init__(self, default_rating, elo):
        self._default_rating = default_rating
        self._subtype_map = dict()
        self._elo = elo

    def prepare_subtype(self, dataframe):
        dataframe.subtype = dataframe.subtype.fillna('total')
        self._subtype_map['total'] = self.WIN_BET
        self.__prepate_win_subtype(dataframe, 'Map1', 'map')
        return dataframe


    def __prepate_win_subtype(self, dataframe, value, replacement):
        dataframe.ix[dataframe.subtype == value, 'subtype_map'] = replacement
        self._subtype_map[replacement] = self.WIN_BET

    def __prepate_cumulative_subtype(self, dataframe, value, replacement):
        dataframe.ix[dataframe.subtype == value, 'subtype_map'] = replacement
        self._subtype_map[replacement] = self.CUMULATIVE_BET

    def replay_elo(self, dataframe):
        t1 = dataframe[['team1', 'game', 'subtype_map']]
        t2 = dataframe[['team2', 'game', 'subtype_map']]
        t1.columns = ['team', 'game', 'subtype_map']
        t2.columns = ['team', 'game', 'subtype_map']
        teams = pandas.concat((t1, t2), axis=0, ignore_index=True)
        teams.drop_duplicates(keep='last', inplace=True)
        teams['rating'] = teams['team'].map(lambda x: Rating(self._default_rating))
        for index, row in dataframe.iterrows():
            if self._subtype_map[row['subtype_map']] == self.WIN_BET:
                if row['result'] == 'win1':
                    winner = row['team1']
                    loser = row['team2']
                elif row['result'] == 'win2':
                    winner = row['team2']
                    loser = row['team1']
                else:
                    raise ValueError('Undefined type of result: ', row['result'])
                winner_index = teams[(teams.team == winner) & (teams.game == row['game']) & (teams.subtype_map == row['subtype_map'])].index
                loser_index = teams[(teams.team == loser) & (teams.game == row['game']) & (teams.subtype_map == row['subtype_map'])].index
                winner_rating_s = teams.loc[winner_index].rating
                loser_rating_s = teams.loc[loser_index].rating
                if len(winner_rating_s) != 1:
                    raise ValueError('Unexpected winner')
                if len(loser_rating_s) != 1:
                    raise ValueError('Unexpected winner')
                winner_rating = winner_rating_s.iloc[0]
                loser_rating = loser_rating_s.iloc[0]
                result = self._elo.rate_1vs1(winner_rating, loser_rating)
                teams.set_value(winner_index, 'rating', Rating(result[0]))
                teams.set_value(loser_index, 'rating', Rating(result[1]))
        return teams
