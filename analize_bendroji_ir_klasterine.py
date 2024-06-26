import duomenys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# import numpy as np

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)


def paimti_duomenis(metai=None):
    print('Įkeliami gyventojų sveikatos duomenys', metai if type(metai) is int else '')
    csv_bazinis_vardas = 'Sveikatos_duomenys_analizei'
    if metai in [None, []]:
        csv_rinkmena = f'{csv_bazinis_vardas}.csv'
    elif type(metai) is int:
        csv_rinkmena = f'{csv_bazinis_vardas}_{metai}.csv'
    elif type(metai) is list:
        print('Įspėjimas: nurodyti keli metai, bet neaišku, ar būtent tie metai būtų jungtiniame CSV')
        csv_rinkmena = f'{csv_bazinis_vardas}.csv'
    else:
        print(
            'Netinkamai nurodyti analizuotini metai. Nurodykite skaičių arba nenurodykite nieko visiems duomenims paimti')
        return None

    if os.path.exists(csv_rinkmena):
        print('  iš jau paruoštų csv', csv_rinkmena)
        df = pd.read_csv(csv_rinkmena)
    elif type(metai) is int:
        print('  iš pirminių csv')
        df = duomenys.Duomenys(metai).gauti_sutvarkytus_duomenis()
    else:
        print('Nerasta', csv_rinkmena)
        return None

    # Papildomai apskaičiuoti KMI
    df['KMI'] = df['Svoris, kg'] / ((df['Ūgis, cm'] / 100) ** 2)

    return df


def bendroji_analize(df):
    metai = unikalus_metai(df)
    if len(metai) == 1:
        metu_str = f' ({metai[0]} m.)'
    else:
        metu_str = f' ({", ".join(str(m) for m in metai)} m. kartu)'

    # Valentina
    print('Atliekama bendroji statistinė analizė...')

    bendras_apkaustuju_kiekis = df['ID'].count()
    print(f'Bendras aplaustuju_skaicius: {bendras_apkaustuju_kiekis}')
    print()

    lyciu_kategorijos = df.groupby(['Lytis'])['ID'].count()
    # print(lyciu_kategorijos)

    vyru_sveikatos_bukle = df[df['Lytis'] == 1].groupby(["Bendra sveikatos būklė", ]).agg(
        vyru=pd.NamedAgg(column="Lytis", aggfunc="count"))
    print(vyru_sveikatos_bukle)
    print()
    #
    moteru_sveikatos_bukle = df[df['Lytis'] == 2].groupby(["Bendra sveikatos būklė", ]).agg(
        moteru=pd.NamedAgg(column="Lytis", aggfunc="count"))
    print(moteru_sveikatos_bukle)
    print()

    amzius = df['Amžius']

    def amziaus_kategorijos(amzius):
        if amzius < 30:
            return "jaunas_amzius"
        elif 30 <= amzius <= 60:
            return 'vidutinis_amzius'
        else:
            return "vyresnis_amzius"

    kategorijos = df['Amžius'].apply(amziaus_kategorijos)
    # print(kategorijos)

    """
    Bendra sveikatos būklė
    1-labai gera, 2-gera, 3-vidutiniska, 4-bloga, 5-labai bloga
    """

    plt.figure(figsize=(10, 6))
    plt.hist(data=df,
             x='Bendra sveikatos būklė',
             color='skyblue')
    plt.title('Bendra sveikatos būklė' + metu_str, fontsize=20)
    plt.xlabel('Bendra sveikatos būklė')
    plt.ylabel('Asmenų skaičius')
    plt.savefig('rezultatai/Sveikatos būklė' + metu_str + '.png')
    plt.show()

    """
    pagal lytį: 1-vyras, 2-moteris
    """

    sns.barplot(data=df, y='Lytis', hue='Lytis')
    plt.title('Pasiskirstymas pagal lytį' + metu_str)
    plt.xlabel('Vyrai / moterys')
    plt.ylabel('Asmenų skaičius')
    plt.savefig('rezultatai/Lytis' + metu_str + '.png')
    plt.show()

    """
    pagal gyvenvietę:  1-miestas, 2-kaimas
    """

    sns.barplot(data=df, y='Miestas/Kaimas', hue='Miestas/Kaimas')
    plt.title('Pasiskirstymas pagal gyvenamą vietą' + metu_str)
    plt.ylabel('Asmenų skaičius')
    plt.xlabel('Miestas / Kaimas')
    plt.savefig('rezultatai/Gyvenvietė' + metu_str + '.png')
    plt.show()


def koreliacine_analize(df, corr_kintamieji=[]):
    metai = unikalus_metai(df)
    if len(metai) == 1:
        metu_str = f' ({metai[0]} m.)'
    else:
        metu_str = f' ({", ".join(str(m) for m in metai)} m. kartu)'

    print('Atliekama koreliacinė analizė...')
    # Koreliacijos analizė.
    if corr_kintamieji is None:
        corr_kintamieji = [kintamasis for kintamasis in df]
    print()

    corr = df[corr_kintamieji].corr()
    corr = corr.replace(1, pd.NA)  # pakeisti koreliacijas su savimi į NaN
    print(corr)

    # print()
    # print('Koreliacija tarp amžiaus ir kitų pasirinktų kintamųjų:')
    # print(corr['Amžius'].drop(['Amžius']))
    # print()
    # print('Koreliacija tarp KMI ir kitų pasirinktų kintamųjų:')
    # print(corr['KMI'].drop(['KMI', 'Amžius']))
    # print()
    # print('Koreliacija tarp vaisių vartojimo ir kitų pasirinktų kintamųjų:')
    # print(corr['Vaisių porcijos per dieną'].drop(['KMI', 'Amžius', 'Vaisių porcijos per dieną']))
    # print()

    # Duomenų vizualizacija ir išvadų pateikimas.

    stipriausia_koreliacija = corr.apply(abs).max().max()
    # 2x2 dydžio lentelė, dvi porų reikšmės vienodos, iš porų yra NaN:
    corr_max_lent = corr[corr.apply(abs) == stipriausia_koreliacija].dropna(how="all", axis=0).dropna(how="all", axis=1)
    # corr_max_lent1 = corr_max_lent.iloc[[0], [1]]  # 1x1 lentelė
    corr_max_kint = list(corr_max_lent.idxmax())  # du kintamieji
    print(f'{str(metai[0]) + " m. gyventojų" if len(metai) == 1 else "Gyventojų"} sveikatos duomenyse '
          f'stipriausia koreliacija rasta tarp \n  '
          f'„{corr_max_kint[0]}“ ir „{corr_max_kint[1]}“ '
          f'(r = {stipriausia_koreliacija:.3f})')
    if stipriausia_koreliacija < 0.2:
        print('Tačiau visos koreliacijos tarp pasirinktų tolydžiųjų kintamųjų yra labai silpnos (Pirsono |r| < 0,2).')

    plt.figure(figsize=(5, 5))
    plt.scatter(df[corr_max_kint[1]], df[corr_max_kint[0]], alpha=0.10)
    plt.title(f'{(str(metai[0]) + " m. gyventojų") if len(metai) == 1 else "Gyventojų"} sveikatos duomenys:\n'
              f'stipriausia rasta koreliacija r={stipriausia_koreliacija:.3f}')
    plt.xlabel(corr_max_kint[1])
    plt.ylabel(corr_max_kint[0])
    plt.savefig('rezultatai/Didžiausia koreliacija ' + metu_str + '.png')
    plt.show()

    # Atlikite laiko analizę, siekiant nustatyti sveikatos rodiklių pokyčius per laiką.
    # Tai gali apimti tendencijų, sezoniškumo ir prognozių modeliavimą.


def unikalus_metai(df):
    return df['Metai'].unique().tolist()


def main():
    corr_kintamieji = ['Amžius', 'KMI', 'Sportas']

    # Analizė nepriklausomai nuo metų
    df = paimti_duomenis()
    if df is not None:
        print()
        print(f'ANALIZUOJAMI METAI IMANT DUOMENIS KARTU: {", ".join(str(metai) for metai in unikalus_metai(df))}')
        bendroji_analize(df)
        koreliacine_analize(df, corr_kintamieji)

    for metai in [2014, 2019]:
        print()
        print()
        df = paimti_duomenis(metai)
        if df is not None:
            print()
            print(f'ANALIZUOJAMI METAI IMANT DUOMENIS ATSKIRAI: {unikalus_metai(df)}')
            print()
            bendroji_analize(df)
            koreliacine_analize(df, corr_kintamieji)


if __name__ == '__main__':
    main()
