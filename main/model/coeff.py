__author__ = 'mivanov'

class Coeff:

    def __init__(self, id, game, date, coeff1, coeff2, team1, team2, type, tournament, parentid, map, result):
        self._id = id
	self._game = game
        self._date = date
        self._coeff1 = coeff1
        self._coeff2 = coeff2
        self._team1 = team1
        self._team2 = team2
        self._type = type
        self._tournament = tournament
        self._map = map
        self._parentid = parentid
        self._result = result
