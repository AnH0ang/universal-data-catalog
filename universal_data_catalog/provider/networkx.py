import networkx as nx

from .base_provider import BaseProvider


class GMLNetworkX(BaseProvider):
    def load(self) -> nx.Graph:
        assert "filepath" in self.config
        return nx.read_gml(
            self.config["filepath"], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: nx.Graph) -> None:
        assert "filepath" in self.config
        return nx.write_gml(value, self.config["filepath"])  # type: ignore
