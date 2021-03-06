import os
import shutil

import pandas as pd
import pytest
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig

from universal_data_catalog.data_catalog import DataCatalog
from universal_data_catalog.types import ConfigDict


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
    def test_load_from_dir(self) -> None:
        catalog = DataCatalog("data/catalog.yml", ".")
        df = catalog.load("titanic")
        titanic_assertion_tests(df)

    def test_load_from_dict(self) -> None:
        _config = OmegaConf.load("data/catalog.yml")
        assert isinstance(_config, DictConfig)
        config: ConfigDict = OmegaConf.to_object(_config)  # type: ignore
        catalog = DataCatalog(config, ".")
        df = catalog.load("titanic")
        titanic_assertion_tests(df)

    def test_load_from_dictconfig(self) -> None:
        config = OmegaConf.load("data/catalog.yml")
        assert isinstance(config, DictConfig)
        catalog = DataCatalog(config, ".")
        df = catalog.load("titanic")
        titanic_assertion_tests(df)

    def test_load_from_absolute(self) -> None:
        catalog = DataCatalog("data/catalog.yml", "test/test/test")
        df = catalog.load("titanic_absolute")
        titanic_assertion_tests(df)

    def test_save(self) -> None:
        df_orig = pd.read_csv("data/titanic.csv")
        catalog = DataCatalog("data/catalog.yml", ".")
        catalog.save("titanic_save", df_orig)
        df = pd.read_csv("data/titanic_saved.csv")
        titanic_assertion_tests(df)

    def test_fail_on_save_to_readonly(self) -> None:
        with pytest.raises(PermissionError):
            df_orig = pd.read_csv("data/titanic.csv")
            catalog = DataCatalog("data/catalog.yml", ".")
            catalog.save("titanic_save_readonly", df_orig)

    def test_load_with_default_not_found(self) -> None:
        catalog = DataCatalog("data/catalog.yml", "test/test/test")
        df = catalog.load_default("abc123", default=123)
        assert df == 123

    def test_load_with_default_is_found(self) -> None:
        catalog = DataCatalog("data/catalog.yml")
        df = catalog.load_default("titanic")
        titanic_assertion_tests(df)

    def test_decorator(self) -> None:
        catalog = DataCatalog("data/catalog.yml")
        df = catalog.load("titanic_faulty$csv")
        titanic_assertion_tests(df)


class TestExcelDataSet:
    def test_load(self) -> None:
        catalog = DataCatalog("data/catalog.yml", ".")
        df = catalog.load("titanic_excel")
        titanic_assertion_tests(df)

    def test_save(self) -> None:
        df_orig = pd.read_excel("data/titanic.xlsx")
        catalog = DataCatalog("data/catalog.yml", ".")
        catalog.save("titanic_excel_save", df_orig)
        df = pd.read_excel("data/titanic_saved.xlsx")
        titanic_assertion_tests(df)
