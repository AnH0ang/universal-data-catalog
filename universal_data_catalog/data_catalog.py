import importlib
import os
from importlib.util import find_spec
from typing import Any, Type

from omegaconf import DictConfig, OmegaConf

from .provider.base_provider import BaseProvider


class DataCatalog:
    def __init__(self, config_dir: str, root_dir: str):
        self.config = self._load_catalog_config_from_yaml(config_dir)
        self.root_dir = root_dir

    def load(self, name: str) -> Any:
        dataset_config = self._pick_dataset_config(name)
        provider = self._load_provider(dataset_config)
        return provider(dataset_config).load()

    def save(self, name: str, value: Any) -> None:
        dataset_config = self._pick_dataset_config(name)
        provider = self._load_provider(dataset_config)
        return provider(dataset_config).save(value)

    def _load_catalog_config_from_yaml(self, config_dir: str) -> DictConfig:
        assert os.path.exists(config_dir)
        conf = OmegaConf.load(config_dir)
        assert isinstance(conf, DictConfig)
        return conf

    def _pick_dataset_config(self, name: str) -> DictConfig:
        assert name in self.config
        dataset_config = self.config[name]
        dataset_config = self._overload_dataset_config(dataset_config)
        return dataset_config

    def _load_provider(self, dataset_config: DictConfig) -> Type[BaseProvider]:
        assert "type" in dataset_config
        return self._import_provider(dataset_config["type"])

    def _overload_dataset_config(self, dataset_config: DictConfig) -> DictConfig:
        dataset_config.filepath = os.path.join(self.root_dir, dataset_config.filepath)
        return dataset_config

    @staticmethod
    def _import_provider(name: str) -> Any:
        relativ_path_list, class_name = name.split(".")[:-1], name.split(".")[-1]
        provider_module = "universal_data_catalog.provider"
        relative_path = "." + ".".join(relativ_path_list)
        assert find_spec(relative_path, provider_module)
        module = importlib.import_module(relative_path, provider_module)
        assert hasattr(module, class_name)
        return getattr(module, class_name)
