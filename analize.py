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
    csv_bazinis_vardas = 'Sveikatos_duomenys_analizei'
    if metai is None:
        csv_rinkmena = f'{csv_bazinis_vardas}.csv'
    elif len(metai) == 1:
        csv_rinkmena = f'{csv_bazinis_vardas}_{metai}.csv'
    else:
        print('Nurodyti keli metai, bet neaišku, ar būtent tie metai būtų jungtiniame CSV')
        csv_rinkmena = f'{csv_bazinis_vardas}.csv'

    if os.path.exists(csv_rinkmena):
        df = pd.read_csv(csv_rinkmena)
    elif len(metai) == 1:
        df = duomenys.Duomenys(metai).gauti_sutvarkytus_duomenis()
    else:
        print('Nerasta', csv_rinkmena)
        df = pd.DataFrame()  # FIXME: kitoje eilutėje bus klaida, nes nebus kintamųjų

    # Papildomai apskaičiuoti KMI
    df['KMI'] = df['Svoris, kg'] / ((df['Ūgis, cm'] / 100) ** 2)

    return df


def bendroji_analize(df):
    # Valentina

    bendras_apkaustuju_kiekis = df['ID'].count()
    # print(f'Bendras aplaustuju_skaicius: {bendras_apkaustuju_kiekis}')

    lyciu_kategorijos = df.groupby(['Lytis'])['ID'].count()
    # print(lyciu_kategorijos)

    vyru_sveikatos_bukle = df[df['Lytis'] == 1].groupby(["Bendra sveikatos būklė", ]).agg(
        vyru=pd.NamedAgg(column="Lytis", aggfunc="count"))
    # print(vyru_sveikatos_bukle)
    #
    moteru_sveikatos_bukle = df[df['Lytis'] == 2].groupby(["Bendra sveikatos būklė", ]).agg(
        moteru=pd.NamedAgg(column="Lytis", aggfunc="count"))
    # # print(moteru_sveikatos_bukle)

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
    Bendra sveikatos būklė pagal amziu
    1-labai gera, 2-gera, 3-vidutiniska, 4-bloga, 5-labai bloga
    """

    plt.figure(figsize=(10, 6))
    plt.bar(df['Bendra sveikatos būklė'],
            df['Amžius'], color='skyblue')
    plt.title('Bendra sveikatos būklė pagal amžių', fontsize=20)
    plt.xlabel('Bendra sveikatos būklė')
    plt.ylabel('Amžius')
    plt.show()

    """
    Bendra sveikatos būklė pagal lytį
    1-labai gera, 2-gera, 3-vidutiniska, 4-bloga, 5-labai bloga
    """

    sns.barplot(data=df, x='Bendra sveikatos būklė', y='Amžius', hue='Lytis')
    plt.title('bendra sveikatos būklė pagal lytį')
    plt.xlabel('Bendra sveikatos būklė')
    plt.ylabel('Amžius')
    plt.show()

    """
    Bendra sveikatos būklė pagal miestas/kaimas
    1-miestas, 2 - kaimas
    """

    sns.barplot(data=df, x='Bendra sveikatos būklė', y='Amžius', hue='Miestas/Kaimas')
    plt.title('bendra sveikatos būklė miestas/kaimas')
    plt.xlabel('Bendra sveikatos būklė')
    plt.ylabel('Amžius')
    plt.show()

    """
    Lėtines ligos pagal amziu
    Ar serga lėtinėmis ligomis: 1- Taip, 2 - ne
    """

    sns.barplot(x='Lėtines ligos', y='Amžius', data=df, hue='Amžius', palette='Set2', dodge=False)
    plt.title('Lėtines ligos pagal amžių')
    plt.ylabel('Amžius')
    plt.xlabel('Lėtines ligos')
    plt.legend([])
    plt.tight_layout()
    plt.show()

    """
    Bendra sveikatos būklė pagal amžiaus kategorijas

    """

    sns.barplot(data=df, x='Bendra sveikatos būklė', y='Lytis', hue=kategorijos)
    plt.title('bendra sveikatos būklė pagal amžių')
    plt.xlabel('Bendra sveikatos būklė')
    plt.ylabel('Lytis')
    plt.show()


def koreliacine_analize(df, corr_kintamieji=[]):
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
    print(f'Stipriausia koreliacija rasta tarp '
          f'„{corr_max_kint[0]}“ ir „{corr_max_kint[1]}“ '
          f'(r = {stipriausia_koreliacija:.3f})')
    if stipriausia_koreliacija < 0.2:
        print('Tačiau visos koreliacijos tarp pasirinktų tolydžiųjų kintamųjų yra labai silpnos (Pirsono |r| < 0,2).')

    plt.figure(figsize=(5, 5))
    plt.scatter(df[corr_max_kint[1]], df[corr_max_kint[0]], alpha=0.10)
    plt.title(f'Gyventojų sveikatos duomenys:\n'
              f'stipriausia rasta koreliacija r={stipriausia_koreliacija:.3f}')
    plt.xlabel(corr_max_kint[1])
    plt.ylabel(corr_max_kint[0])
    plt.show()

    # Atlikite laiko analizę, siekiant nustatyti sveikatos rodiklių pokyčius per laiką.
    # Tai gali apimti tendencijų, sezoniškumo ir prognozių modeliavimą.


def main():
    df = paimti_duomenis()
    bendroji_analize(df)
    corr_kintamieji = ['Amžius', 'KMI', 'Sportas']
    koreliacine_analize(df, corr_kintamieji)


if __name__ == '__main__':
    main()
