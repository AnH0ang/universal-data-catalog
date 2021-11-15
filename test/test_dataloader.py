import os
import shutil

import pytest

from universal_data_catalog.data_catalog import DataCatalog


@pytest.fixture(autouse=True)
def run_around_tests():
    assert os.path.exists("test")
    os.chdir("test")

    try:
        assert os.path.exists("_data")
        assert not os.path.exists("data_catalog")
        shutil.copytree(os.path.join("_data", "data_catalog", "extra"), "extra")
        shutil.copytree(os.path.join("_data", "data_catalog", "data"), "data")
        yield
    finally:
        shutil.rmtree("extra", ignore_errors=True)
        shutil.rmtree("data", ignore_errors=True)
        os.chdir("..")


class TestDataLoader:
    def test_load_custom_provider(self):
        catalog = DataCatalog("data/catalog.yml", ".")
        value = catalog.load("custom_provider")
        assert value == "test\n"
