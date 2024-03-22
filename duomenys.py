import pandas as pd
import os


class Duomenys:
    # Duomenys tik vieniems pasirinktiems metams
    def __init__(self, metai):
        self.metai = metai
        self.csv_duomenys = os.path.join('duomenys',
            str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv')
        self.csv_aprašymai = os.path.join('duomenys',
            str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv')
        self.df = pd.DataFrame()
        self.kintamieji = [
            'pid', 'sex', 'age', 'm_k', 'hs1', 'hs2', 'pe6', 'sk1', 'al1', 'am3', 'bm1', 'bm2'
        ]
        # am3 atsakymų nėra >1000 žmonių
        # dh4 atsakymų nėra >2000 žmonių
        self.atitikmenys = {'pid': 'ID',
                            'sex': 'Lytis',
                            'age': 'Amžius',
                            'm_k': 'Miestas/Kaimas',
                            'hs1': 'Bendra sveikatos būklė',
                            'hs2': 'Lėtines ligos',
                            'pe6': 'Sportas',
                            'sk1': 'Rūkymas',
                            'al1': 'Alkoholis',
                            'am3': 'Kartai pas šeimos gydytoją per 4 sav.',
                            'bm1': 'Ūgis, cm',
                            'bm2': 'Svoris, kg'
                            }
        self.kintamieji_išskirčių_tikrinimui = [
            'Amžius',
            'Kartai pas šeimos gydytoją per 4 sav.', 'Ūgis, cm', 'Svoris, kg'
        ]
        self.df = pd.DataFrame()
        self.ar_duomenys_sutvarkyti = False
        self.csv2pd()  # nuskaitymas

    def info(self):
        print()
        print(f'{self.metai} m. gyventojų sveikatos ' +
              ('sutvarkyti' if self.ar_duomenys_sutvarkyti else 'NEtvarkyti') +
              ' duomenys:')
        self.df.info()
        print()

    def tvarkyti(self):
        self.pervadinti_kintamuosius()
        self.valyti()  # valymas
        self.atmesti_isskirtis(self.kintamieji_išskirčių_tikrinimui)
        self.ar_duomenys_sutvarkyti = True
        print(' - Duomenys baigti tvarkyti')

    def irasyti_csv(self,csv_rinkmena):
        self.df.to_csv(csv_rinkmena, index=False)
        print(f'{csv_rinkmena} irasyta sekmingai')

    def csv2pd(self):
        # nuskaityti csv
        self.df = pd.read_csv(self.csv_duomenys)
        # artinkti norimus kintamuosius - Audrius
        self.df = self.df[self.kintamieji]
        self.df['Metai'] = self.metai
        print(f'{self.metai} m. gyventojų sveikatos duomenys įkelti į vidinę strukūrą. ' +
              ('' if self.ar_duomenys_sutvarkyti else 'Jie netvarkyti!'))

    def pervadinti_kintamuosius(self):
        # nebūtina, galima rankiniu būdu - Audrius
        self.df.rename(columns=self.atitikmenys, inplace=True)
        print(' - Kintamieji pervadinti')

    def valyti(self):
        # prisiminti pradinį skaičių palyginimui
        eilučių_pradinis_skaičius = len(self.df)

        # tuščių ir praleistus reikšmių atmetimas - Mindaugas
        self.df = self.df.dropna()
        #self.df = self.df[self.df.notnull().all(axis=1)]

        # Kai kuriuose kintamuosiuose neigiamomis reikšmėmis žymimi neanalizuotini duomenys, pvz.,
        # -1 Nenurodyta
        # -2 Netaikoma
        # -3 Neįtraukiama į skaičiavimus (Proxy = 2 arba 3)
        for k in self.df:
            self.df = self.df[self.df[k] >= 0]

        # pokytis
        eilučių_pokytis = eilučių_pradinis_skaičius - len(self.df)
        if eilučių_pokytis == 0:
            print(' - Tuščių/praleistų ir neigiamų reikšmių nebuvo.')
        else:
            print(' - Atmestos eilutės sutuščiomis/praleistomis ir neigiamomis reikšmėmis:', eilučių_pokytis)

    def atmesti_isskirtis(self, pasirinkti_kintamieji):
        # išskirčių atmetimas pagal IQR - Mindaugas
        # < Q1 - IQR * 1.5
        # > Q3 + IQR * 1.5
        kriterijus = 1.5  # bet kartais naudojama 3
        print(f' - Išskirčių šalinimas, jei < Q1-IQR*{kriterijus} arba > Q3+IQR*{kriterijus}:')
        for k in pasirinkti_kintamieji:
            if k in self.df:
                eilučių_pradinis_skaicius = self.df[k].count()
                quantiles = self.df[k].quantile(q=[0.25, 0.75])
                iqr = quantiles[0.75] - quantiles[0.25]
                self.df = self.df[self.df[k] >= quantiles[0.25] - iqr * kriterijus]
                self.df = self.df[self.df[k] <= quantiles[0.75] + iqr * kriterijus]
                eilučių_skaičiaus_pokytis = eilučių_pradinis_skaicius - self.df[k].count()
                if eilučių_skaičiaus_pokytis == 0:
                    print(f'   - kintamasis „{k}“ neturėjo išskirčių')
                else:
                    print(f'   - iš kintamojo „{k}“ pašalintos išskirtys:', eilučių_skaičiaus_pokytis)
            else:
                print(f'   - nepavyko rasti kintamojo „{k}“')

    def gauti_duomenis(self):
        return self.df

    def gauti_sutvarkytus_duomenis(self):
        if not self.ar_duomenys_sutvarkyti:
            self.tvarkyti()
        return self.df


def main():
    for metai in [2014, 2019]:
        duomenys = Duomenys(metai)
        duomenys.tvarkyti()
        #duomenys.info()
        duomenys.irasyti_csv(f'Sveikatos_duomenys_analizei_{metai}.csv')
        #df = duomenys.gauti_duomenis()



if __name__ == '__main__':
    main()
