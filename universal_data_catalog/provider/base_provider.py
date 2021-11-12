import abc
from typing import Any

from omegaconf import DictConfig


class BaseProvider(abc.ABC):
    def __init__(self, config: DictConfig, **kwargs: Any) -> None:
        self.config = config

    @abc.abstractmethod
    def load(self) -> Any:
        pass

    @abc.abstractmethod
    def save(self, value: Any) -> None:
        pass
