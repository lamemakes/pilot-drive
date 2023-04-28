"""
Typings used to assist with DBus/dasbus related activities.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, cast
from dasbus.connection import (  # type: ignore # missing
    SystemMessageBus,
)

from dasbus.typing import (  # type: ignore # missing
    ObjPath,
    Variant,
    Str,
)

from dasbus.server.interface import (  # type: ignore # missing
    dbus_signal,
)


class MessageBus(ABC):
    """
    A DBus message bus instance
    """

    @abstractmethod
    def publish_object(self, address: ObjPath, obj: Any) -> None:
        """
        Publish an object on the bus

        :param address: A DBus ObjPath to publish the object to
        :param obj: The object to be published
        """

    @abstractmethod
    def register_service(self, name: Str) -> None:
        """
        Register a new service

        :param name: the name of the service to register
        """

    @abstractmethod
    def get_proxy(self, name: Str, address: ObjPath) -> Any:
        """
        Get a proxy for a DBus object

        :param name: the name of the intended object to get a proxy for
        :param address: a DBus ObjPath to the intended object to get a proxy for
        """


def SystemBus() -> MessageBus:  # pylint: disable=invalid-name
    """
    Get a new DBus system bus

    :return: A new DBus system bus instance
    """
    return cast(MessageBus, SystemMessageBus())


class ObjectManagerAPI(ABC):  # pylint: disable=too-few-public-methods
    """
    Type for the DBus ObjectManager
    """

    interface = "org.freedesktop.DBus.ObjectManager"

    @abstractmethod
    def GetManagedObjects(  # pylint: disable=invalid-name
        self,
    ) -> Dict[ObjPath, Dict[Str, Dict[Str, Variant]]]:
        """
        Return all managed objects

        :return: a dict of all managed objects/interfaces
        """

    InterfacesAdded: dbus_signal  # pylint: disable=invalid-name

    InterfacesRemoved: dbus_signal  # pylint: disable=invalid-name


class PropertiesAPI(ABC):
    """
    Type for DBus properties
    """

    interface = "org.freedesktop.DBus.Properties"

    @abstractmethod
    def Get(self, interface: Str, name: Str) -> Variant:  # pylint: disable=invalid-name
        """
        Get a specific property

        :param interface: name of the interface containing the property
        :param name: name of the property to get
        """

    @abstractmethod
    def GetAll(  # pylint: disable=invalid-name
        self, interface: Str
    ) -> Dict[Str, Variant]:
        """
        Get all properties

        :param interface: name of the interface containing the properties
        """

    @abstractmethod
    def Set(  # pylint: disable=invalid-name
        self, interface: Str, name: Str, value: Variant
    ) -> None:
        """
        Set a specific property

        :param interface: name of the interface containing the property
        :param name: name of the property to set
        :param value: value of the property
        """

    PropertiesChanged: dbus_signal
