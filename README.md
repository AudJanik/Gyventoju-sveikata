
Projektaso pavadinimas: Gyventojų sveikata


Darbo autoriai: Mindaugas B., Audrius Janikunas, Valentina Verikė.

Projekto tema: Lietuvos gyventojų sveikatos duomenų analizė

Duomenų šaltinis: atviri šaltiniai
https://open-data-ls-osp-sdg.hub.arcgis.com/datasets/26d03b90d0db4a1190279c58917b1dea_0/about

Projekto aprašymas: Gyventojų sveikatos statistinis tyrimas Lietuvoje atliekamas kas 5 metus. 
Rengiama ir skelbiama išsami statistinė informacija apie gyventojų sveikatos būklę, sveikatos priežiūrą, 
sveikatą lemiančius veiksnius ir naudojimąsi sveikatos priežiūros paslaugomis. 

Analizuojami: 2014 m. ir  2019 m. atlikto gyventojų sveikatos statistinio tyrimo duomenys. 
Analizuojami kintamieji nurodantys įprastinę asmens būklę, ligas, pasitenkinimą sveikatos priežiūros įstaigomis, 
asmeninių įpročių įtaką sveikatai (skiepai, fizinis aktyvumas, rūkimas, alkoholio vartojimas). 

Darbas atliktas Python kalba, panaudojant bidliotekas: requests, pandas, json, matplotlib, beautifulsoup ir seaborn.

PROJEKTO SEKA

Duomenys.py

Panaudotos bibliotekos: requests, pandas, json, beautifulsoup
Duomenų šaltinis:
https://open-data-ls-osp-sdg.hub.arcgis.com/datasets/26d03b90d0db4a1190279c58917b1dea_0/about
Duomenų apimtys:
2014_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv
2014_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv
2019_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_duomenys.csv
2019_m._atlikto_gyventojų_sveikatos_statistinio_tyrimo_kintamieji_ir_jų_paaiškinimai.csv

Analize.py

Panaudotos bibliotekos: pandas, matplotlib, seaborn, matplotlib ir beautifulsoup

Atlikome duomenų gryninimo veiksmus: atrinkome analizei reikalingus kintamuosiu, apjungėme 2014 ir 2019 m. duomenys į vieną duomenų bazę.


Lietuvos gyventojų sveikatos duomenų VIZUALIZACIJA