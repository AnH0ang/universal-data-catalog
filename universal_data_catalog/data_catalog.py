import os
from typing import Any, Type, Union

from omegaconf import DictConfig, OmegaConf

from universal_data_catalog.constants import ReservedKeys
from universal_data_catalog.provider.base_provider import BaseProvider
from universal_data_catalog.types import ConfigDict
from universal_data_catalog.util.load_provider import load_provider_from_path


class DataCatalog:
    def __init__(self, config: Union[str, ConfigDict], root_dir: str):
        self.root_dir = root_dir

        # load config from config from input
        if isinstance(config, str):
            self.config = self._load_catalog_config_from_yaml(config)
        elif isinstance(config, dict):
            self.config = config
        elif isinstance(config, DictConfig):
            self.config: ConfigDict = OmegaConf.to_object(config)  # type: ignore
        else:
            raise ValueError("Expects 'config' to be of type str, dict or DictConfig.")

        # overload config
        self.config = self._overload_catalog_config(self.config)

    def load(self, name: str) -> Any:
        dataset_config = self._pick_dataset_config(name)
        provider = self._load_provider(dataset_config)
        return provider(dataset_config).load()

    def save(self, name: str, value: Any) -> None:
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
