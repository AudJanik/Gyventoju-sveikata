import pandas as pd
import os


class Duomenys:
    # Duomenys tik vieniems pasirinktiems metams
    def __init__(self, metai, kintamieji=None, rodyti_pagalba=1):
        self.metai = metai
        self.csv_duomenys = os.path.join('duomenys', str(metai) +
                                         '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv')
        self.csv_aprašymai = os.path.join('duomenys',
                                          str(metai) + '_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv')
        self.df = pd.DataFrame()
        if kintamieji is None:
            self.kintamieji = ['pid', 'sex', 'age', 'm_k', 'hs1', 'hs2', 'pe6', 'sk1', 'al1', 'am3', 'bm1', 'bm2']
        else:
            self.kintamieji = kintamieji

        # kodavimo_keitimas()
        self.kintamieji_taip_ne = [
            # 'sex', 'm_k',  # lytis ir miestas/kaimas nėra taip/ne, tačiau irgi dvireikšmiai
            'cd1a', 'cd1b', 'cd1c', 'cd1d', 'cd1e', 'cd1f', 'cd1g',
            'cd1h', 'cd1i', 'cd1j', 'cd1k', 'cd1l', 'cd1m', 'cd1n', 'cd1o',
            'ac1a', 'ac1b', 'ac1c'
            ]

        # pervadinti_kintamuosius()
        self.atitikmenys = {
                            # PAGRINDINIAI SOCIALINIAI KINTAMIEJI
                            'pid': 'ID',
                            'sex': 'Lytis',
                            'age': 'Amžius',
                            'm_k': 'Miestas/Kaimas',

                            # SVEIKATOS KINTAMIEJI
                            'hs1': 'Bendra sveikatos būklė',
                            'hs2': 'Lėtines ligos',

                            # Ligos ir lėtinės būklės: Ar per pastaruosius 12 mėn. sirgote kuria nors iš išvardytų ligų?
                            'cd1a': 'Astma',
                            'cd1b': 'Bronchitas',
                            'cd1c': 'Miokardo infarktas',
                            'cd1d': 'Širdies liga',
                            'cd1e': 'Padidėjęs kraujospūdis',
                            'cd1f': 'Insultas',
                            'cd1g': 'Artrozė',
                            'cd1h': 'Nugaros liga',
                            'cd1i': 'Kaklo liga',
                            'cd1j': 'Cukrinis diabetas',
                            'cd1k': 'Alergija',
                            'cd1l': 'Kepenų cirozė',
                            'cd1m': 'Šlapimo nelaikymas',
                            'cd1n': 'Inkstų problemos',
                            'cd1o': 'Depresija',

                            # Nelaimingi atsitikimai: Ar per pastaruosius 12 mėn. Jums buvo nutikęs kuris nors iš
                            # išvardytų nelaimingų atsitikimų, kurio metu buvote sužeistas (-a)?
                            # (Įskaitant apsinuodijimą, gyvūnų arba vabzdžių sukeltą žalą.
                            # Neįskaitant kitų asmenų tyčiniais veiksmais sukeltų sužalojimų)
                            'ac1a': 'Eismo įvyis',  # a) Kelių eismo įvykis
                            'ac1b': 'Nelaimė namuose',  # b) Nelaimingas atsitikimas namuose
                            'ac1c': 'Nelaimė darbe',  # c) Nelaimingas atsitikimas laisvalaikio metu

                            # Ar dėl šio nelaimingo atsitikimo Jums reikėjo medicinos pagalbos?
                            'ac2': 'Medicininė pagalba po nelaimės',  # 1 ir 2 – taip, 3 - ne

                            # SVEIKATĄ LEMIANTYS VEIKSNIAI
                            'bm1': 'Ūgis, cm',
                            'bm2': 'Svoris, kg',
                            'pe6': 'Sportas',
                            'dh1': 'Vaisų vartojimo dažnumas',  # 2019 m.
                            'fv1': 'Vaisų vartojimo dažnumas',  # 2014 m.
                            'dh3': 'Daržovių vartojimo dažnumas',  # 2019 m.
                            'fv3': 'Daržovių vartojimo dažnumas',  # 2014 m.
                            'sk1': 'Rūkymas',
                            'al1': 'Alkoholis',
            
                            # SVEIKATOS PRIEŽIŪRA
                            'am3': 'Kartai pas šeimos gydytoją per 4 sav.',  # am3 atsakymų nėra >1000 žmonių
                            }
        self.kintamieji_išskirčių_tikrinimui = [
            'Amžius', 'Kartai pas šeimos gydytoją per 4 sav.', 'Ūgis, cm', 'Svoris, kg'
            ]
        self.df = pd.DataFrame()
        self.ar_duomenys_sutvarkyti = False
        self.csv2pd()  # nuskaitymas

        if rodyti_pagalba:
            if self.ar_duomenys_sutvarkyti:
                print('Norėdami gauti duomenis, naudokite .gauti_duomenis()')
            else:
                print('Norėdami gauti sutvarkytus duomenis, naudokite .gauti_sutvarkytus_duomenis()')

    def info(self):
        print()
        print(f'{self.metai} m. gyventojų sveikatos ' +
              ('sutvarkyti' if self.ar_duomenys_sutvarkyti else 'NEtvarkyti') +
              ' duomenys:')
        self.df.info()
        print()

    def kodavimo_keitimas(self):
        # Pradiniuose duomenyse kai kurie kintamieji užkoduoti: 1=Taip, 2=Ne.
        # Čia 2=Ne pakeiskime į 0=Ne
        kintamieji_su_pakeistu_kodavimu = []
        for k in self.df:
            if k in self.kintamieji_taip_ne:
                self.df[k] = abs(self.df[k] - 2)
                kintamieji_su_pakeistu_kodavimu.append(k)
        # specialus atvejis 'ac2' - pagalba po nelaimingo atsitikimo
        if 'ac2' in self.df:
            # 1,2 -> 1 „taip“, -2,3 -> 0 „ne“
            self.df['ac2'] =  self.df['ac2'].apply(lambda x: int((x > 0) & (x < 2)))
            kintamieji_su_pakeistu_kodavimu.append('ac2')
        if kintamieji_su_pakeistu_kodavimu:
            print(' - Pakeistas kintamųjų kodavimas:', kintamieji_su_pakeistu_kodavimu)

    def tvarkyti(self):
        self.kodavimo_keitimas()
        self.pervadinti_kintamuosius()
        self.valyti()  # valymas
        kintamieji_išskirčių_tikrinimui = set(self.df.columns).intersection(self.kintamieji_išskirčių_tikrinimui)
        if kintamieji_išskirčių_tikrinimui:
            self.atmesti_isskirtis(kintamieji_išskirčių_tikrinimui)
        else:
            print(' - Tarp pasirinktų kintamųjų nebuvo tokių, kurie pažymėti išskirčių atmetimui. Galite kviesti .atmesti_isskirtis() atskirai.')
        self.ar_duomenys_sutvarkyti = True
        print(' - Duomenys baigti tvarkyti')

    def irasyti_csv(self, csv_rinkmena):
        self.df.to_csv(csv_rinkmena, index=False)
        print(f'{csv_rinkmena} irasyta sekmingai')

    def csv2pd(self):
        # nuskaityti csv
        self.df = pd.read_csv(self.csv_duomenys)
        # artinkti norimus kintamuosius - Audrius
        self.df = self.df[self.kintamieji]
        # Prijungus vėlesnių metų duomenis, galėti atskirti juos
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
        # self.df = self.df[self.df.notnull().all(axis=1)]

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
    # nuskaityti didžiuosius duomenis, atsirinkti mums reikalingus,
    # įrašyti į csv

    csv_bazinis_vardas_saugojimui = 'Sveikatos_duomenys_analizei'
    norimi_metai = [2014, 2019]

    df = pd.DataFrame()  # rezertuoti kintamąjį, kad PyCharm nerodytų įspėjimų
    for i, metai in enumerate(norimi_metai):
        duomenys = Duomenys(metai, rodyti_pagalba=0)
        duomenys.tvarkyti()
        # duomenys.info()
        duomenys.irasyti_csv(f'{csv_bazinis_vardas_saugojimui}_{metai}.csv')

        # išstraukti duomenis dėl vėlesnio sujungimo
        df1 = duomenys.gauti_duomenis()
        if len(norimi_metai) > 1:
            # pakeisti ID, kad nesidubliuotų su kitų metų, jei būtų
            df1['ID'] = metai * 100000 + df1['ID']
        if i == 0:
            df = df1
        else:
            df = pd.concat([df, df1], axis=0)  # prijungti eilutes

    df.to_csv(f'{csv_bazinis_vardas_saugojimui}.csv')
    print(f'Atrinktieji {", ".join(str(metai) for metai in norimi_metai)} m. '
          f'duomenys sėkmingai įrašyti į „{csv_bazinis_vardas_saugojimui}.csv“')


if __name__ == '__main__':
    main()
