import networkx as nx

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class GMLNetworkX(BaseProvider):
    def load(self) -> nx.Graph:
        assert ReservedKeys.FILEPATH in self.config
        return nx.read_gml(
            self.config[ReservedKeys.FILEPATH], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: nx.Graph) -> None:
        assert ReservedKeys.FILEPATH in self.config
        return nx.write_gml(value, self.config[ReservedKeys.FILEPATH])  # type: ignore
