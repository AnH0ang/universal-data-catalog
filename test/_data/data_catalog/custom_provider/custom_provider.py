from typing import Any

from universal_data_catalog.constants import ReservedKeys
from universal_data_catalog.provider.base_provider import BaseProvider


class CustomProvider(BaseProvider):
    def load(self) -> str:
        file_path = self.config[ReservedKeys.FILEPATH]
        with open(file_path, "r+") as f:
            return f.read()

    def save(self, value: Any) -> None:
        pass
