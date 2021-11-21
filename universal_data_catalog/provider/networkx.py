import networkx as nx

from universal_data_catalog.constants import ReservedKeys

from .base_provider import BaseProvider


class GMLNetworkX(BaseProvider):
    """``GMLNetworkX`` loads/saves a graph from/to a GML file using networkx.

    It acts a thin abstraction layer for the networkx functions ``networkx.read_gml``
    and ``networkx.write_gml``.
    """

    def load(self) -> nx.Graph:
        """Load data using ``networkx.read_gml``.

        Returns:
            Loaded DataFrame.
        """
        assert ReservedKeys.FILEPATH in self.config
        return nx.read_gml(
            self.config[ReservedKeys.FILEPATH], **self.config.get("load_args", {})
        )  # type: ignore

    def save(self, value: nx.Graph) -> None:
        """Save data using ``networkx.write_gml``."""
        assert ReservedKeys.FILEPATH in self.config
        return nx.write_gml(value, self.config[ReservedKeys.FILEPATH])  # type: ignore
