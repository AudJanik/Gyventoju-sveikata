import pandas as pd

class Duomenys:
    def __init__(self, metai):
        self.metai = metai
        self.kintamieji = []
        self.df = pd.DataFrame()


    def csv2pd(self, csv_rinkmena, kintamųjų_sąrašas):
        # nuskaityti csv
        df = pd.read_csv(csv_rinkmena)
        # artinkti norimus kintamuosius - Audrius

    def kintamojo_paaišknimas(self):
        # nebūtina, galima rankiniu būdu - Mindaugas?

    def valymas(self):
        # tuščių reikšmių, išskirčių atmetimas - Mindaugas

def main()
    metai = 2019