import os

import pytest
from duomenys import Duomenys


@pytest.fixture(scope="class")
def testiniai_kintamieji():
    kintamieji = ['pid', 'sex', 'age', 'm_k', 'hs1', 'hs2', 'pe6', 'sk1', 'al1', 'am3', 'bm1', 'bm2']
    # duomenys_objektas = Duomenys(testiniai_duomenys)
    return kintamieji


def test_pervadinti_kintamuosius(testiniai_kintamieji):
    duomenu_obj = Duomenys(2019, testiniai_kintamieji)
    df = duomenu_obj.gauti_duomenis()
    assert testiniai_kintamieji != [k for k in df]


def test_valyti(testiniai_kintamieji):
    duomenys_objektas = Duomenys(2019, testiniai_kintamieji)
    duomenys_objektas.valyti()
    isvalyti_duomenys = duomenys_objektas.gauti_duomenis()
    for k in isvalyti_duomenys:
        assert not any(isvalyti_duomenys[k].isnull())
        assert not any(isvalyti_duomenys[k] < 0)
