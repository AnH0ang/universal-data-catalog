import importlib
from importlib.util import find_spec
from typing import Type

from universal_data_catalog.exceptions import ProviderNotFoundError
from universal_data_catalog.provider.base_provider import BaseProvider
from universal_data_catalog.transformer.base_transformer import BaseTransformer


def load_provider_from_path(path: str) -> Type[BaseProvider]:
    relative_path_list, class_name = path.split(".")[:-1], path.split(".")[-1]
    provider_module = "universal_data_catalog.provider"
    relative_path = ".".join(relative_path_list)

    if module_exists("." + relative_path, provider_module):
        module = importlib.import_module("." + relative_path, provider_module)
    elif module_exists(relative_path):
        module = importlib.import_module(relative_path)
    else:
        raise ProviderNotFoundError()

    assert hasattr(module, class_name)
    return getattr(module, class_name)


def load_transformer_from_path(path: str) -> Type[BaseTransformer]:
    relative_path_list, class_name = path.split(".")[:-1], path.split(".")[-1]
    provider_module = "universal_data_catalog.transformer"
    relative_path = ".".join(relative_path_list)

    if module_exists("." + relative_path, provider_module):
        module = importlib.import_module("." + relative_path, provider_module)
    elif module_exists(relative_path):
        module = importlib.import_module(relative_path)
    else:
        raise ProviderNotFoundError()

    assert hasattr(module, class_name)
    return getattr(module, class_name)


def module_exists(name, package=None):
    try:
        loader = find_spec(name, package)
        return loader is not None
    except ModuleNotFoundError:
        return False
