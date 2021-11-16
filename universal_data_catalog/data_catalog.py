from __future__ import annotations

import os
from typing import Any, Type, Union

from omegaconf import DictConfig, OmegaConf

from universal_data_catalog.constants import ReservedKeys
from universal_data_catalog.provider.base_provider import BaseProvider
from universal_data_catalog.types import ConfigDict
from universal_data_catalog.util.load_provider import load_provider_from_path


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

    def __init__(self, config: Union[str, ConfigDict, DictConfig], root_dir: str):
        """Initilize the Data Catalog with the path to a config file or a config dictionary.

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
            self.config = OmegaConf.to_object(config)
        else:
            raise ValueError("Expects 'config' to be of type str, dict or DictConfig.")

        # overload config
        self.config = self._overload_catalog_config(self.config)

    def load(self, name: str) -> Any:
        """Load a dataset by name from the catalog.

        Args:
            name: Name of the dataset that should be loaded.

        Returns:
            The loaded dataset.
        """
        dataset_config = self._pick_dataset_config(name)
        provider = self._load_provider(dataset_config)
        return provider(dataset_config).load()

    def save(self, name: str, value: Any) -> None:
        """Save dataset to catalog with the specified name.

        Args:
            name: Name under which the dataset will be registered
            value: Dataset that will be saved.

        Raises:
            PermissionError: The Dataset is read only.
        """
        dataset_config = self._pick_dataset_config(name)

        # raise error is real only flag is set to true
        if (ReservedKeys.READONLY in dataset_config) and dataset_config[
            ReservedKeys.READONLY
        ]:
            raise PermissionError(
                f"Trying to save to dataset '{name}' which is read only."
            )

        provider = self._load_provider(dataset_config)
        return provider(dataset_config).save(value)

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

    def _load_provider(self, dataset_config: ConfigDict) -> Type[BaseProvider]:
        assert ReservedKeys.TYPE in dataset_config
        return load_provider_from_path(dataset_config[ReservedKeys.TYPE])

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
        dataset_config[ReservedKeys.FILEPATH] = os.path.join(
            self.root_dir, dataset_config[ReservedKeys.FILEPATH]
        )
        return dataset_config
