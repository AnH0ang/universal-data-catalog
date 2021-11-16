import os
import pickle
import shutil

import pytest

from universal_data_catalog.data_catalog import DataCatalog


@pytest.fixture(autouse=True)
def run_around_tests():
    assert os.path.exists("test")
    os.chdir("test")

    try:
        assert os.path.exists("_data")
        assert not os.path.exists("data")
        shutil.copytree(os.path.join("_data", "pickle"), "data")
        yield
    finally:
        shutil.rmtree("data", ignore_errors=True)
        os.chdir("..")


class TestPickleData:
    def test_save(self) -> None:
        catalog = DataCatalog("data/catalog.yml", ".")
        value = {"a": 1, "b": 3}
        catalog.save("dict_read", value)
        with open("data/dict.pickle", "rb") as f:
            read_value = pickle.load(f)
        assert read_value == value

    def test_read(self) -> None:
        catalog = DataCatalog("data/catalog.yml", ".")
        value = {"a": 1, "b": 3}
        read_value = catalog.load("dict_saved")
        assert read_value == value
