import pandas as pd
import os


class Duomenys:
    def __init__(self, metai):
        self.metai = metai
        self.csv_duomenys = os.path.join('duomenys', str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv')
        self.csv_aprašymai = os.path.join('duomenys', str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv')
        self.kintamieji = ['pid', 'sex', 'age', 'citizen', 'ap', 'm_k', 'hs1', 'hs2', 'cd2', 'pn1', 'pa1', 'pe6',
                            'sk1', 'al1']
        self.atitikmenys = {'pid': 'ID', 'sex': 'Lytis', 'age': 'Amzius', 'citizen': 'Pilietybe',
            'ap': 'Apskritis', 'm_k': 'Miestas/Kaimas', 'hs1': 'Bendra sveikatos bukle', 'cd2': 'Bendra dantu bukle',
            'hs2': 'Letines ligos', 'pn1': 'Kuno skausmas', 'pa1': 'Skiepai', 'pe6': 'Sportas', 'sk1': 'Rukymas',
            'al1': 'Alkohoilis'}

        self.df = pd.DataFrame()

        self.csv2pd()  # nuskaitymas
        # self.kintamojo_paaišknimas() # pridėti kintamųjų paaiškinimus
        print(f'{metai} m. gyventojų sveikatos duomenys įkelti į vidinę strukūrą.')

    def info(self):
        self.df.info()

    def csv2pd(self):
        # nuskaityti csv
        self.df = pd.read_csv(self.csv_duomenys)
        # artinkti norimus kintamuosius - Audrius
        self.df = self.df[self.kintamieji]
        self.df.rename(columns=self.atitikmenys, inplace=True)



    def kintamojo_paaišknimas(self):
        # nebūtina, galima rankiniu būdu - Mindaugas?
        pass

    def valymas(self):
        # tuščių reikšmių atmetimas - Mindaugas
        self.df = self.df.dropna()
        print(' - atmestos tuščios eilutės')

    def atmesti_isskirtis(self, pasirinkti_kintamieji):
        # išskirčių atmetimas pagal IQR - Mindaugas
        # < Q1 - IQR * 1.5
        # > Q3 + IQR * 1.5
        kriterijus = 1.5  # bet kartais naudojama 3
        print(f'Išskirčių šalinimas, jei < Q1-IQR*{kriterijus} arba > Q3+IQR*{kriterijus}:')
        for k in pasirinkti_kintamieji:
            if k in self.df:
                eilučių_pradinis_skaicius = self.df[k].count()
                quantiles = self.df[k].quantile(q=[0.25, 0.75])
                iqr = quantiles[0.75] - quantiles[0.25]
                self.df = self.df[self.df[k] >= quantiles[0.25] - iqr * kriterijus]
                self.df = self.df[self.df[k] <= quantiles[0.75] + iqr * kriterijus]
                eilučių_skaičiaus_pokytis = eilučių_pradinis_skaicius - self.df[k].count()
                if eilučių_skaičiaus_pokytis == 0:
                    print(f' - kintamasis „{k}“ neturėjo išskirčių')
                else:
                    print(f' - iš kintamojo „{k}“ pašalintos išskirtys:', eilučių_skaičiaus_pokytis)
            else:
                print(f' - nepavyko rasti kintamojo „{k}“')

    def gauti_duomenis(self):
        return self.df

    def gauti_sutvarkytus_duomenis(self):
        self.valymas()  # valymas
        self.atmesti_isskirtis(['age'])
        return self.df


def main():
    duomenys2019 = Duomenys(2019)
    df = duomenys2019.gauti_sutvarkytus_duomenis()
    df.info()
    # print(df)


if __name__ == '__main__':
    main()
