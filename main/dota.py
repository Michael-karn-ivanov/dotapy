from coeffprovider import CoeffProvider
from consts import DEFAULT_RATING, ELO_K_FACTOR, ELO_BETA
from dao import Dao
import time, threading
from elo.elo import Elo
from precalculation import PreCalculation

__author__ = 'mivanov'
import sys

def grab(interval):
    coeffprovider = CoeffProvider()
    dao = Dao()
    coeffs = coeffprovider.get_coeff_list()
    dao.save_new_data(coeffs)
    print(time.ctime())
    threading.Timer(interval, grab, [interval]).start()

def calculate():
    dao = Dao()
    elo = Elo(k_factor=ELO_K_FACTOR, rating_class=float, initial=DEFAULT_RATING, beta=ELO_BETA)
    calculator = PreCalculation(DEFAULT_RATING, elo)
    dataframe = dao.get_past()
    dataframe = calculator.prepare_subtype(dataframe)
    rating = calculator.replay_elo(dataframe)
    print rating

if len(sys.argv) == 1:
    print "Usage: dota grab <interval in seconds> OR dota calc"
else:
    if sys.argv[1] == "grab":
        grab(int(sys.argv[2]))
    elif sys.argv[1] == "calc":
        calculate()