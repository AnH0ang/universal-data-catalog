from __future__ import annotations

from typing import Any

from universal_data_catalog.types import ConfigDict


class BaseTransformer:
    def __init__(self, config: ConfigDict) -> None:
        self.config = config

    def before_load(self, data_config: ConfigDict) -> ConfigDict:
        return data_config

    def after_load(self, value: Any) -> Any:
        return value

    def before_save(
        self, data_config: ConfigDict, value: Any
    ) -> tuple[ConfigDict, Any]:
        return data_config, value
