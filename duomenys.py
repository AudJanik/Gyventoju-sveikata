import pandas as pd
import os


class Duomenys:
    def __init__(self, metai):
        self.metai = metai
        self.csv_duomenys = os.path.join('duomenys',
            str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv')
        self.csv_aprašymai = os.path.join('duomenys',
            str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv')
        self.df = pd.DataFrame()
        self.kintamieji = [
            'pid', 'sex', 'age', 'citizen', 'ap', 'm_k', 'hs1', 'hs2', 'cd2', 'pn1', 'pa1', 'pe6', 'sk1', 'al1']
        self.atitikmenys = {'pid': 'ID',
                            'sex': 'Lytis',
                            'age': 'Amžius',
                            'citizen': 'Pilietybė',
                            'ap': 'Apskritis',
                            'm_k': 'Miestas/Kaimas',
                            'hs1': 'Bendra sveikatos būklė',
                            'cd2': 'Bendra dantų būklė',
                            'hs2': 'Lėtines ligos',
                            'pn1': 'Kūno skausmas',
                            'pa1': 'Skiepai',
                            'pe6': 'Sportas',
                            'sk1': 'Rūkymas',
                            'al1': 'Alkoholis'}
        self.kintamieji_išskirčių_tikrinimui = ['Amžius']
        self.df = pd.DataFrame()
        self.csv2pd()  # nuskaitymas
        self.ar_duomenys_sutvarkyti = False
        print(f'{metai} m. gyventojų sveikatos duomenys įkelti į vidinę strukūrą. ' +
              ('' if self.ar_duomenys_sutvarkyti else 'Jie netvarkyti!'))



    def tvarkyti(self):
        self.pervadinti_kintamuosius()
        self.valyti()  # valymas
        self.atmesti_isskirtis(self.kintamieji_išskirčių_tikrinimui)
        self.ar_duomenys_sutvarkyti = True
        print(' - Duomenys baigti tvarkyti')

    def irasyti_csv(self,csv_rinkmena):
        self.df.to_csv(csv_rinkmena)
        print(f'{csv_rinkmena} irasyta sekmingai')
    def info(self):
        print()
        print(f'{self.metai} m. gyventojų sveikatos ' +
              ('sutvarkyti' if self.ar_duomenys_sutvarkyti else 'NEtvarkyti') +
              ' duomenys:')
        self.df.info()
        print()

    def csv2pd(self):
        # nuskaityti csv
        self.df = pd.read_csv(self.csv_duomenys)
        # artinkti norimus kintamuosius - Audrius
        self.df = self.df[self.kintamieji]

    def pervadinti_kintamuosius(self):
        # nebūtina, galima rankiniu būdu - Audrius
        self.df.rename(columns=self.atitikmenys, inplace=True)
        print(' - Kintamieji pervadinti')

    def valyti(self):
        # tuščių reikšmių atmetimas - Mindaugas
        eilučių_pradinis_skaičius = len(self.df)
        self.df = self.df.dropna()
        eilučių_pokytis = eilučių_pradinis_skaičius - len(self.df)
        if eilučių_pokytis == 0:
            print(' - Tuščių ar praleistų reikšmių nebuvo.')
        else:
            print(' - Atmestos eilutės sutuščiomis ar praleistomis reikšmėmis:', eilučių_pokytis)

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
    duomenys2019 = Duomenys(2019)
    #duomenys2019.info()
    duomenys2019.tvarkyti()
    duomenys2019.info()
    df = duomenys2019.gauti_duomenis()
    duomenys2019.irasyti_csv('Sveikatos_duomenys_analizei.csv')
    print(df)


if __name__ == '__main__':
    main()
