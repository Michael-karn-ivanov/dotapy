__author__ = 'mivanov'

import pandas
import numpy as np
import os
import datetime
from model.coeff import Coeff

class Dao:
    __root = "../data/"

    def __read_file(self, filename):
        result = pandas.read_csv(filename, sep=',', header=None, names = ['id', 'game', 'date', 'coeff1', 'coeff2', 'team1', 'team2',\
                                                                          'type', 'tourney', 'subtype', 'parent', 'result'], dtype=np.str, index_col=None)
        result.sort_values(by='date', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
        return result

    def __deduplicate(self):
        total = self.__read_file(self.__root + '!EGB.csv')
        for filename in os.listdir(self.__root + "."):
            if filename.startswith('coeffs') and filename.endswith('.csv'):
                coeff = self.__read_file(self.__root + filename)
                total = pandas.concat((total, coeff), axis=0, ignore_index=True)
                total.drop_duplicates(subset = 'id', keep='last', inplace=True)
        tt = total.sort_values('date')
        os.remove(self.__root + '!EGB.csv')
        total.to_csv(self.__root + '!EGB.csv', sep=',', header=None, index=False, encoding='utf-8')
        for filename in os.listdir(self.__root + "."):
            if filename.startswith('coeffs') and filename.endswith('.csv'):
                os.remove(self.__root + filename)

    def save_new_data(self, coeffs, fileName = None):
        if fileName is None:
            now = datetime.datetime.now()
            fileName = 'coeffs-{0}-{1}-{2}-{3}-{4}.csv'.format(now.year, now.month, \
                                                                       now.day if now.day > 10 else "0" + `now.day`, \
                                                                       now.hour if now.hour > 10 else "0" + `now.hour`, \
                                                                       now.minute if now.minute > 10 else "0" + `now.minute`,
                                                                       now.second if now.second > 10 else "0" + `now.second`)
        with open(self.__root + fileName, 'w') as coeff_file:
            for coeff in coeffs:
                coeff_file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(coeff._id, coeff._game, datetime.datetime.fromtimestamp(int(coeff._date)).strftime('%Y-%m-%d %H:%M:%S.%f'), coeff._coeff1, coeff._coeff2, coeff._team1, coeff._team2, coeff._type, coeff._tournament, coeff._map, coeff._parentid, coeff._result))
        self.__deduplicate()


    def get_past(self, filename = '!EGB.csv'):
        data = self.__read_file(self.__root + filename)
        return data[data.result != 'draw']

    def get_future(self):
        data = self.__read_file(self.__root + '!EGB.csv')
        return data[data.result == 'draw']
