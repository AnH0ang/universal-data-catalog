import os
from typing import Any, Type, Union

from omegaconf import DictConfig, OmegaConf

from .constants import ReservedKeys
from .exceptions import ReadOnlyError
from .provider.base_provider import BaseProvider
from .util.load_provider import load_provider_from_path


class DataCatalog:
    def __init__(self, config: Union[str, DictConfig], root_dir: str):
        if isinstance(config, str):
            self.config = self._load_catalog_config_from_yaml(config)
        elif isinstance(config, DictConfig):
            self.config = config
        else:
            raise ValueError()
        self.root_dir = root_dir

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
            raise ReadOnlyError()

        provider = self._load_provider(dataset_config)
        return provider(dataset_config).save(value)

    def _load_catalog_config_from_yaml(self, config_dir: str) -> DictConfig:
        assert os.path.exists(config_dir)
        conf = OmegaConf.load(config_dir)
        assert isinstance(conf, DictConfig)
        conf = self._overload_catalog_config(conf)
        return conf

    def _pick_dataset_config(self, name: str) -> DictConfig:
        assert name in self.config
        dataset_config = self.config[name]
        dataset_config = self._overload_dataset_config(dataset_config)
        return dataset_config

    def _load_provider(self, dataset_config: DictConfig) -> Type[BaseProvider]:
        assert ReservedKeys.TYPE in dataset_config
        return load_provider_from_path(dataset_config[ReservedKeys.TYPE])

    def _overload_dataset_config(self, dataset_config: DictConfig) -> DictConfig:
        # prepend root path to filepath
        dataset_config.filepath = os.path.join(self.root_dir, dataset_config.filepath)
        return dataset_config

    @staticmethod
    def _overload_catalog_config(config: DictConfig) -> DictConfig:
        # remove all entries with keys that start with a underscore
        for key in [k for k in config.keys() if k.startswith("_")]:  # type: ignore
            config.pop(key)
        return config
