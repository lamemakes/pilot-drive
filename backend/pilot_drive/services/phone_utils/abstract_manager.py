"""
Module containing the abstract manager used for phone connectivity
"""

from abc import ABC, abstractmethod
from typing import List
from .phone_constants import PhoneStates


class AbstractManager(ABC):
    """
    Abstract manager that to encourage proper implementation of Android/iOS devices
    """

    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def notifications(self) -> List[dict]:
        """
        Get the list of aggregated notifications

        :return: a list of notifications collected by the manager
        """

    @property
    @abstractmethod
    def state(self) -> PhoneStates:
        """
        Return the state of the connected device

        :return: the current state of the phone via the PhoneState attribute
        """

    @property
    @abstractmethod
    def device_name(self) -> str:
        """
        Get the name of the connected device

        :return: the name of the connected device
        """
