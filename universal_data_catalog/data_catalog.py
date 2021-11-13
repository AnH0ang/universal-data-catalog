import importlib
import os
from typing import Any, Type

from omegaconf import DictConfig

from .provider.base_provider import BaseProvider


class DataCatalog:
    def __init__(self, config: DictConfig, root_dir: str):
        self.config = config
        self.root_dir = root_dir

    def load(self, name: str) -> Any:
        dataset_config = self._get_dataset_config(name)
        provider = self._get_provider(dataset_config)
        return provider(dataset_config).load()

    def save(self, name: str, value: Any) -> None:
        dataset_config = self._get_dataset_config(name)
        provider = self._get_provider(dataset_config)
        return provider(dataset_config).save(value)

    def _get_dataset_config(self, name: str) -> DictConfig:
        assert name in self.config
        dataset_config = self.config[name]
        dataset_config = self._overload_dataset_config(dataset_config)
        return dataset_config

    def _get_provider(self, dataset_config: DictConfig) -> Type[BaseProvider]:
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
        assert importlib.util.find_spec(relative_path, provider_module)
        module = importlib.import_module(relative_path, provider_module)
        assert hasattr(module, class_name)
        return getattr(module, class_name)
