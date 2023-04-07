from abc import ABC, abstractmethod
from typing import List
from .phone_constants import PhoneStates


class AbstractManager(ABC):
    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def notifications(self) -> List[dict]:
        pass

    @property
    @abstractmethod
    def state(self) -> PhoneStates:
        pass

    @property
    @abstractmethod
    def device_name(self) -> str:
        pass
