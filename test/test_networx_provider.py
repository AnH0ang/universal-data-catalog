import os
import shutil

import networkx as nx
import pytest
from omegaconf import DictConfig, OmegaConf

from universal_data_catalog.data_catalog import DataCatalog


@pytest.fixture(autouse=True)
def run_around_tests():
    assert os.path.exists("test")
    os.chdir("test")

    try:
        assert os.path.exists("_data")
        assert not os.path.exists("data")
        shutil.copytree(os.path.join("_data", "networkx"), "data")
        yield
    finally:
        shutil.rmtree("data", ignore_errors=True)
        os.chdir("..")


@pytest.fixture
def sample_graph() -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([1, 3, 6])
    G.add_nodes_from(
        [
            (4, {"color": "red"}),
            (5, {"color": "green"}),
        ]
    )
    G.add_edge(1, 3)
    G.add_edges_from([(3, 4), (1, 5)])
    return G


def graph_assertion_test(graph: nx.Graph):
    assert isinstance(graph, nx.Graph)
    assert graph.number_of_edges() == 3
    assert graph.number_of_nodes() == 5
    assert list(graph.nodes) == ["1", "3", "6", "4", "5"]
    assert graph.nodes["4"].get("color") == "red"


class TestGMLNetworkx:
    def test_load(self):
        conf = OmegaConf.load("conf/catalog.yml")
        assert isinstance(conf, DictConfig)
        catalog = DataCatalog(conf, ".")
        graph = catalog.load("graph")
        graph_assertion_test(graph)

    def test_save(self, sample_graph: nx.Graph):
        conf = OmegaConf.load("conf/catalog.yml")
        assert isinstance(conf, DictConfig)
        catalog = DataCatalog(conf, ".")
        catalog.save("graph_save", sample_graph)
        assert os.path.exists("data/graph_save.gml")
        graph = nx.read_gml("data/graph_save.gml")
        graph_assertion_test(graph)
