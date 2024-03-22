import os

import pytest
from duomenys import Duomenys

@pytest.fixture(scope="class")

def testiniai_duomenys():
    kintamieji=['pid', 'sex', 'age', 'm_k', 'hs1', 'hs2', 'pe6', 'sk1', 'al1', 'am3', 'bm1', 'bm2']
    # duomenys_objektas = Duomenys(testiniai_duomenys)
    return kintamieji

# def test_pervadinti_kintamuosius(testiniai_duomenys):

def test_valyti(testiniai_duomenys):
    duomenys_objektas = Duomenys(2019, testiniai_duomenys)
    duomenys_objektas.valyti()
    isvalyti_duomenis =duomenys_objektas.gauti_duomenis()
    for k in isvalyti_duomenis:
        assert not any(isvalyti_duomenis[k].isnull())





           # assert isvalyti_duomenis[i]










