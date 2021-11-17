from __future__ import annotations

from typing import Any

from universal_data_catalog.types import ConfigDict


class BaseTransformer:
    def before_load(self, config: ConfigDict) -> ConfigDict:
        return config

    def after_load(self, value: Any) -> Any:
        return value

    def before_save(self, config: ConfigDict, value: Any) -> tuple[ConfigDict, Any]:
        return config, value
