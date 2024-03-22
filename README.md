
Darbo autoriai: Mindaugas B., Audrius Janikunas, Valentina Verikė.

# Lietuvos gyventojų sveikata

Analizuojami: 2014 m. ir  2019 m. atlikto gyventojų sveikatos statistinio tyrimo duomenys. 

Darbas atliktas Python kalba, panaudojant bibliotekas: pandas, matplotlib, seaborn.



## PROJEKTO svarbiausios dalys:

### Duomenys

`duomenys.py` - duomenų nuskaitymas, kintamųjų atrinkimas, tvarkymas, 2014 ir 2019 m. duomenų jungimas.

`duomenys` - katalogas su pirminiais duomenimis

### Analizė

`analize.py` - bendroji aprašomoji statistika ir koreliacinė analizė

### Rezultatai

`rezultatai` - katalogas, kuriame patalpinti analizės grafikai:

Pasiskirstymas pagal lytį (1-vyras, 2-moteris)

![paveikslas](rezultatai/Lytis%20(2014,%202019%20m.%20kartu).png)


Pasiskirstymas pagal gyvenvietę (1-miestas, 2 - kaimas)

![paveikslas](rezultatai/Gyvenvietė%20(2014,%202019%20m.%20kartu).png)


Koreliacinė analizė

![paveikslas](rezultatai/Didžiausia%20koreliacija%20%20(2014%20m.).png)
![paveikslas](rezultatai/Didžiausia%20koreliacija%20%20(2019%20m.).png)



Bendra sveikatos būklė(1-labai gera, 2-gera, 3-vidutiniska, 4-bloga, 5-labai bloga)

![paveikslas](rezultatai/Sveikatos%20būklė%20(2014%20m.).png)

![paveikslas](rezultatai/Sveikatos%20būklė%20(2019%20m.).png)

 ### Testasvimas

`test_duomenys.py`
