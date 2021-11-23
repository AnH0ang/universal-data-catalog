from __future__ import annotations

from typing import Any

from universal_data_catalog.types import ConfigDict


class BaseTransformer:
    """A base class for transformer providers that can hook in before/after read/save operations."""

    def __init__(self, config: ConfigDict) -> None:
        """Initialize the transformer.

        Args:
            config: Configuration that was passed from the catalog yaml file.
        """
        self.config = config

    def before_load(self, data_config: ConfigDict) -> ConfigDict:
        """Hook that is run before loading the data.

        The ``data_config`` is passed to through this function which will later be used
        to initialize the provider.

        Args:
            data_config: Configuration for the dataset provider.

        Returns:
            Modified data_config.
        """
        return data_config

    def after_load(self, value: Any) -> Any:
        """Hook that is run after loading the data.

        The value that is loaded is passed to through this function and can be modified.

        Args:
            value: Loaded value.

        Returns:
            Modified value.
        """
        return value

    def before_save(
        self, data_config: ConfigDict, value: Any
    ) -> tuple[ConfigDict, Any]:
        """Hook that is run before saveing the data.

        The value that is will be saved and that data_config that is used to initialize that
        dataset provider are passed through this function and can be modified.

        Args:
            data_config: Save provider configuration.
            value: Value that will be saved.

        Returns:
            Modified `data_config` and `value`.
        """
        return data_config, value
