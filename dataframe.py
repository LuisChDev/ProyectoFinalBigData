import pandas as pd
from main import main as main_
from pickle import dump

PARTIDOS = [('cedemocratico', 'b', 'o'),
            ('partidodelaucol', 'r', '*'),
            ('PartidoLiberal', 'g', 'v'),
            ('PartidoVerdeCoL', 'c', '^'),
            ('PoloDemocratico', 'y', '<'),
            ('soyconservador', 'm', '>')]


def save():
    for p, c, s in PARTIDOS:
        frame = pd.DataFrame(main_(partido=p, filedir=p))
        with open('dataframes/' + p + '.pkl', 'wb') as archivo:
            dump(frame, archivo)
