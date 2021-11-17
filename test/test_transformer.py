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
        assert not os.path.exists("extra")

        shutil.copytree(os.path.join("_data", "transformer", "extra"), "extra")
        shutil.copytree(os.path.join("_data", "transformer", "data"), "data")
        yield
    finally:
        shutil.rmtree("extra", ignore_errors=True)
        shutil.rmtree("data", ignore_errors=True)
        os.chdir("..")


class TestTransformer:
    def test_after_load_custom_transformer(self):
        catalog = DataCatalog("data/catalog.yml", ".")
        df = catalog.load("titanic")
        assert isinstance(df, pd.DataFrame)
        assert "new_col" in df.columns
        assert (df["new_col"] == "test1").all()

    def test_before_save_custom_transformer(self):
        catalog = DataCatalog("data/catalog.yml", ".")
        df = pd.read_csv("data/titanic.csv")
        assert "new_col" not in df.columns
        catalog.save("titanic_save", df)
        df_saved = pd.read_csv("data/titanic_save.csv")
        assert "new_col" in df_saved.columns
        assert (df_saved["new_col"] == "test2").all()

    def test_before_load_custom_transformer(self):
        catalog = DataCatalog("data/catalog.yml", ".")
        df = catalog.load("titanic_modify_path")
        assert isinstance(df, pd.DataFrame)
        assert df.shape[1] == 12
