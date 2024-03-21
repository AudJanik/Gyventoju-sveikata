import pandas as pd
import os


class Duomenys:
    def __init__(self, metai):
        self.metai = metai
        self.csv_duomenys = os.path.join('duomenys', str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv')
        self.csv_aprašymai = os.path.join('duomenys', str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv')
        self.kintamieji = []
        self.df = pd.DataFrame()

        self.csv2pd()  # nuskaitymas
        # self.kintamojo_paaišknimas() # pridėti kintamųjų paaiškinimus
        print(f'{metai} m. gyventojų sveikatos duomenys įkelti į vidinę strukūrą.')

    def csv2pd(self, kintamųjų_sąrašas=[]):
        # nuskaityti csv
        self.df = pd.read_csv(self.csv_duomenys)
        # artinkti norimus kintamuosius - Audrius

    def kintamojo_paaišknimas(self):
        # nebūtina, galima rankiniu būdu - Mindaugas?
        pass

    def valymas(self):
        # tuščių reikšmių, išskirčių atmetimas - Mindaugas
        self.df = self.df.dropna()
        print(' - atmestos tuščios eilutės')


    def gauti_sutvarkytus_duomenis(self):
        self.valymas() # valymas
        return self.df


def main():
    duomenys2019 = Duomenys(2019)
    print(duomenys2019.gauti_sutvarkytus_duomenis())


if __name__ == '__main__':
    main()