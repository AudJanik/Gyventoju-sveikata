
Projekto pavadinimas: Gyventojų sveikata


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

Atlikome duomenų gryninimo veiksmus: atrinkome analizei reikalingus kintamuosius, apjungėme 2014 ir 2019 m. duomenys į vieną duomenų bazę.


Lietuvos gyventojų sveikatos duomenų VIZUALIZACIJA

Bendra sveikatos būklė pagal amziu 
1-labai gera, 2-gera, 3-vidutiniska, 4-bloga, 5-labai bloga

![paveikslas](https://github.com/AudJanik/Gyventoju-sveikata/assets/157985262/eb016cb7-dd56-4a20-9118-e210948d9759)


Bendra sveikatos būklė pagal lytį
1-labai gera, 2-gera, 3-vidutiniska, 4-bloga, 5-labai bloga

![paveikslas](https://github.com/AudJanik/Gyventoju-sveikata/assets/157985262/416b1869-4b3f-4390-931d-82550ae76b0c)


Bendra sveikatos būklė pagal miestas/kaimas
1-miestas, 2 - kaimas
![paveikslas](https://github.com/AudJanik/Gyventoju-sveikata/assets/157985262/f929ae0a-95c9-4450-819b-9e43d701fca8)

Lėtines ligos pagal amziu
Ar serga lėtinėmis ligomis: 1- Taip, 2 - ne


![paveikslas](https://github.com/AudJanik/Gyventoju-sveikata/assets/157985262/29d27378-7015-4b2e-a08a-00cfb45c0813)


Bendra sveikatos būklė pagal amžiaus kategorijas

![paveikslas](https://github.com/AudJanik/Gyventoju-sveikata/assets/157985262/e61a762a-6e33-40f5-bfc7-ba6a7155f12d)


