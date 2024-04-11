# Audrius ir Mindaugas
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
from duomenys import Duomenys


def ar_sveikata_gera(x):
    if x >= 3:
        return 0  # vidutiška, bloga ir labai bloga sveikata
    else:
        return 1  # gera ir labai gera sveikata



df = Duomenys(
    2019,  # metai
    ['hs1', 'pe1', 'pe2', 'pe3', 'pe4', 'pe5', 'pe6', 'pe8'],  # kintamieji iki pervadinimo
    atitikmenys={
        'pe1': 'Darbo tipas',
        'pe3': 'Ėjimo trukmė',
        'pe5': 'Mynimo trukmė',
    },
    rodyti_pagalba=False,
).gauti_sutvarkytus_duomenis()  # grąžina jau pervadintus ir sutvarkytus kintamuosius
df['Sėdimas arba stovimas darbas'] = df['Darbo tipas'] == 1
df['Vidut. sunkumo fiz. darbas'] = df['Darbo tipas'] == 2
df['Sunkus fizinis darbas'] = df['Darbo tipas'] == 3
df['Ėjimo trukmė 10-29 min/d.'] = df['Ėjimo trukmė'] == 1
df['Ėjimo trukmė 30-59 min/d.'] = df['Ėjimo trukmė'] == 2
df['Ėjimo trukmė 1-2 val./d.'] = df['Ėjimo trukmė'] == 3
df['Ėjimo trukmė >3 val./d.'] = df['Ėjimo trukmė'] == 4
df['Važiavimo dviračiu trukmė 10-29 min/d.'] = df['Mynimo trukmė'] == 1
df['Važiavimo dviračiu trukmė 30-59 min/d.'] = df['Mynimo trukmė'] == 2
df['Važiavimo dviračiu trukmė 1-2 val./d.'] = df['Mynimo trukmė'] == 3
df['Važiavimo dviračiu trukmė >3 val./d.'] = df['Mynimo trukmė'] == 4

y = df['Bendra sveikatos būklė'].apply(ar_sveikata_gera)
X = df.drop(columns=['Bendra sveikatos būklė', 'Metai', 'Darbo tipas', 'Ėjimo trukmė', 'Mynimo trukmė'])
feature_names = X.columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# print(f'Modelio tiklsumas: {accuracy * 100:.2f}%')
feature_importances = pd.DataFrame(clf.feature_importances_, index=feature_names,
                                   columns=['importance']).sort_values(by='importance', ascending=False)
# print(feature_importances)
plt.figure(figsize=(15, 10))
sns.barplot(x=feature_importances.importance, y=feature_importances.index)
plt.title(f'Geros sveikatos būklę lemiantys fizinio aktyvumo veiksniai\n '
          f'(atsit. miškų klasif. metodo tikslumas su testiniais duomenimis {accuracy * 100:.2f}%)')
plt.xlabel('Veiksnio svarbumas')
plt.ylabel('Fizinio aktyvumo veiksnys')
plt.tight_layout()  # kad nenukirstų x ašyje kintamųjų pavadinimų
plt.show()
