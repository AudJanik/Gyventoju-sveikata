import pandas as pd
import duomenys
import matplotlib.pyplot as plt
# import os

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)

metai = 2019

df = duomenys.Duomenys(metai).gauti_sutvarkytus_duomenis()
# csv_rinkmena = 'Sveikatos_duomenys_analizei.csv'
# if not os.path.exists(csv_rinkmena):
#     print('Nerasta', csv_rinkmena)
#     exit(1)
# df = pd.read_csv(csv_rinkmena)

# Papildomai apskaičiuoti KMI
df['KMI'] = df['Svoris, kg'] / ((df['Ūgis, cm']/100)**2)

# Koreliacijos analizė.
print()
corr_kintamieji = [
    'Amžius', 'KMI', 'Vaisių porcijos per dieną', 'Sportas',
    'Naktų ligoninėje per metus', 'Kartai stacionare per metus']
corr = df[corr_kintamieji].corr()
corr = corr.replace(1, pd.NA)  # pakeisti koreliacijas su savimi į NaN

stipriausia_koreliacija = corr.apply(abs).max().max()
# 2x2 dydžio lentelė, dvi porų reikšmės vienodos, iš porų yra NaN:
corr_max_lent = corr[corr.apply(abs) == stipriausia_koreliacija].dropna(how="all", axis=0).dropna(how="all", axis=1)
# corr_max_lent1 = corr_max_lent.iloc[[0], [1]]  # 1x1 lentelė
corr_max_kint = list(corr_max_lent.idxmax()) # du kintamieji
print(f'Stipriausia koreliacija rasta tarp '
      f'„{corr_max_kint[0]}“ ir „{corr_max_kint[1]}“ '
      f'(r = {stipriausia_koreliacija:.3f})')
if stipriausia_koreliacija < 0.2:
     print('Tačiau visos koreliacijos tarp pasirinktų tolydžiųjų kintamųjų yra labai silpnos (Pirsono |r| < 0,2).')

print()
print('Koreliacija tarp amžiaus ir kitų pasirinktų kintamųjų:')
print(corr['Amžius'].drop(['Amžius']))
print()
print('Koreliacija tarp KMI ir kitų pasirinktų kintamųjų:')
print(corr['KMI'].drop(['KMI', 'Amžius']))
print()
print('Koreliacija tarp vaisių vartojimo ir kitų pasirinktų kintamųjų:')
print(corr['Vaisių porcijos per dieną'].drop(['KMI', 'Amžius', 'Vaisių porcijos per dieną']))
print()

# Duomenų vizualizacija ir išvadų pateikimas.
plt.figure(figsize=[5,5])
plt.scatter(df[corr_max_kint[1]], df[corr_max_kint[0]], alpha=0.10)
plt.title(f'{metai} m. gyventojų sveikatos duomenys:\n'
          f'stipriausia rasta koreliacija r={stipriausia_koreliacija:.3f}')
plt.xlabel(corr_max_kint[1])
plt.ylabel(corr_max_kint[0])
plt.show()

# Atlikite laiko analizę, siekiant nustatyti sveikatos rodiklių pokyčius per laiką.
# Tai gali apimti tendencijų, sezoniškumo ir prognozių modeliavimą.
