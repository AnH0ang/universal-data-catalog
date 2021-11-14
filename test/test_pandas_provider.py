# More infos under https://docs.pytest.org

import os
import shutil

import pandas as pd
import pytest

from universal_data_catalog.data_catalog import DataCatalog


@pytest.fixture(autouse=True)
def run_around_tests():
    assert os.path.exists("test")
    os.chdir("test")

    try:
        assert os.path.exists("_data")
        assert not os.path.exists("data")
        shutil.copytree(os.path.join("_data", "pandas"), "data")
        yield
    finally:
        shutil.rmtree("data", ignore_errors=True)
        os.chdir("..")


def titanic_assertion_tests(df):
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 891
    assert (
        df.columns
        == [
            "PassengerId",
            "Survived",
            "Pclass",
            "Name",
            "Sex",
            "Age",
            "SibSp",
            "Parch",
            "Ticket",
            "Fare",
            "Cabin",
            "Embarked",
        ]
    ).all()
    assert (df.Embarked.head(5) == ["S", "C", "S", "S", "S"]).all()


class TestCSVDataSet:
    def test_load(self) -> None:
        catalog = DataCatalog("conf/catalog.yml", ".")
        df = catalog.load("titanic")
        titanic_assertion_tests(df)

    def test_save(self) -> None:
        df_orig = pd.read_csv("data/titanic.csv")
        catalog = DataCatalog("conf/catalog.yml", ".")
        catalog.save("titanic_save", df_orig)
        df = pd.read_csv("data/titanic_saved.csv")
        titanic_assertion_tests(df)


class TestExcelDataSet:
    def test_load(self) -> None:
        catalog = DataCatalog("conf/catalog.yml", ".")
        df = catalog.load("titanic_excel")
        titanic_assertion_tests(df)

    def test_save(self) -> None:
        df_orig = pd.read_excel("data/titanic.xlsx")
        catalog = DataCatalog("conf/catalog.yml", ".")
        catalog.save("titanic_excel_save", df_orig)
        df = pd.read_excel("data/titanic_saved.xlsx")
        titanic_assertion_tests(df)
