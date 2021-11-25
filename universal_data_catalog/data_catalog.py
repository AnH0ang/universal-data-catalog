from __future__ import annotations

import os
from typing import Any, Union

from omegaconf import DictConfig, OmegaConf

from universal_data_catalog.constants import ReservedKeys
from universal_data_catalog.provider.base_provider import BaseProvider
from universal_data_catalog.transformer.base_transformer import BaseTransformer
from universal_data_catalog.types import ConfigDict
from universal_data_catalog.util.load_provider import (
    load_provider_from_path,
    load_transformer_from_path,
)


class DataCatalog:
    """``Data Catalog`` acts as an general interface for all data read and writes.

    It provides ``load`` and ``save`` capabilities from anywhere in the program.
    To use a ``DataCatalog``, you need to instantiate it with the path to the configuration
    file or a configuration dictionary. Then it will act as a
    single point of reference for your calls, relaying load and save
    functions to the underlying data sets.

    Examples:

        >>> catalog = DataCatalog("catalog.yml")
        >>> df = catalog.load("titanic")
        >>> catalog.save("titanic", df)

    """

    def __init__(self, config: Union[str, ConfigDict, DictConfig], root_dir: str = "."):
        """Initialize the Data Catalog with the path to a config file or a config dictionary.

        Args:
            config: path to a configuration yaml file or a configuration dictionary.
            root_dir: directory which acts as a root for all relative paths specified in the config.

        Raises:
            ValueError: argument ``config`` has an invalid type.
        """
        self.root_dir = root_dir

        # load config from config from input
        if isinstance(config, str):
            self.config = self._load_catalog_config_from_yaml(config)
        elif isinstance(config, dict):
            self.config = config  # type: ignore
        elif isinstance(config, DictConfig):
            self.config: ConfigDict = OmegaConf.to_object(config)  # type: ignore
        else:
            raise ValueError("Expects 'config' to be of type str, dict or DictConfig.")

        # overload config
        self.config = self._overload_catalog_config(self.config)  # type: ignore

    def load(self, name: str) -> Any:
        """Load a dataset by name from the catalog.

        Args:
            name: Name of the dataset that should be loaded.

        Returns:
            The loaded dataset.
        """
        # load dataset
        dataset_config = self._pick_dataset_config(name)
        transformers = self._load_transformers(dataset_config)
        dataset_config = self._apply_pre_load(transformers, dataset_config)

        # load provider
        provider = self._load_provider(dataset_config)

        # load value
        value = provider.load()
        value = self._apply_after_load(transformers, value)
        return value

    def save(self, name: str, value: Any) -> None:
        """Save dataset to catalog with the specified name.

        Args:
            name: Name under which the dataset will be registered
            value: Dataset that will be saved.

        Raises:
            PermissionError: The Dataset is read only.
        """
        # get dataset configuration
        dataset_config = self._pick_dataset_config(name)

        # raise error is real only flag is set to true
        if (ReservedKeys.READONLY in dataset_config) and dataset_config[
            ReservedKeys.READONLY
        ]:
            raise PermissionError(
                f"Trying to save to dataset '{name}' which is read only."
            )

        # load transformers
        transformers = self._load_transformers(dataset_config)

        # apply transformers
        dataset_config, value = self._apply_pre_save(
            transformers, dataset_config, value
        )

        # save value
        provider = self._load_provider(dataset_config)
        provider.save(value)

    def _load_catalog_config_from_yaml(self, config_dir: str) -> ConfigDict:
        assert os.path.exists(config_dir)
        conf = OmegaConf.load(config_dir)
        assert isinstance(conf, DictConfig)
        conf_dict = OmegaConf.to_object(conf)
        return conf_dict  # type: ignore

    def _pick_dataset_config(self, name: str) -> ConfigDict:
        assert name in self.config
        dataset_config = self.config[name]
        return dataset_config

    def _load_provider(self, dataset_config: ConfigDict) -> BaseProvider:
        assert ReservedKeys.TYPE in dataset_config
        provider_class = load_provider_from_path(dataset_config[ReservedKeys.TYPE])
        provider = provider_class(dataset_config)
        return provider

    def _load_transformers(self, data_config: ConfigDict) -> list[BaseTransformer]:
        if ReservedKeys.TRANSFORMER not in data_config:
            return []
        else:
            assert isinstance(data_config[ReservedKeys.TRANSFORMER], list)

            transformers: list[BaseTransformer] = []
            for transformer_config in data_config[ReservedKeys.TRANSFORMER]:
                assert ReservedKeys.TYPE in transformer_config
                transformer_class = load_transformer_from_path(
                    transformer_config[ReservedKeys.TYPE]
                )
                transformers.append(transformer_class(transformer_config))
            return transformers

    def _apply_after_load(self, transformers: list[BaseTransformer], value: Any) -> Any:
        for transformer in transformers:
            value = transformer.after_load(value)
        return value

    def _apply_pre_load(
        self, transformers: list[BaseTransformer], dataset_config: ConfigDict
    ) -> ConfigDict:
        for transformer in transformers:
            dataset_config = transformer.before_load(dataset_config)
        return dataset_config

    def _apply_pre_save(
        self,
        transformers: list[BaseTransformer],
        dataset_config: ConfigDict,
        value: Any,
    ):
        for transformer in transformers:
            dataset_config, value = transformer.before_save(dataset_config, value)
        return dataset_config, value

    def _overload_catalog_config(self, config: ConfigDict) -> ConfigDict:
        # remove all entries with keys that start with a underscore
        for key in list(config.keys()):
            if key.startswith("_"):  # type: ignore
                config.pop(key)

        # overload each datset entry individually
        for key in config:
            config[key] = self._overload_dataset_config(config[key])

        return config

    def _overload_dataset_config(self, dataset_config: ConfigDict) -> ConfigDict:
        # prepend root path to filepath
        if ReservedKeys.FILEPATH in dataset_config and not dataset_config.get(
            ReservedKeys.ISABSOLUTE, False
        ):
            dataset_config[ReservedKeys.FILEPATH] = os.path.join(
                self.root_dir, dataset_config[ReservedKeys.FILEPATH]
            )
        return dataset_config
