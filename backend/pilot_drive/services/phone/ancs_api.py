"""
The DBus APIs required by the IOS/ANCS manager
"""

from abc import abstractmethod
from typing import cast
from dasbus.typing import Str, UInt32, Bool
from dasbus.server.interface import (  # type: ignore # missing
    dbus_signal,
)

from ..shared.dbus_api import PropertiesAPI, MessageBus


class ANCSObserver(PropertiesAPI):
    """
    Type wrapper for the ANCS Observer service
    """

    name = "ancs4linux.Observer"
    path = "/"

    @classmethod
    def connect(cls, bus: MessageBus) -> "ANCSObserver":
        """
        Get a proxy for the ANCS Observer DBus object

        :return: an instance of BluezGattCharacteristic
        """
        return cast(ANCSObserver, bus.get_proxy(cls.name, cls.path))

    @abstractmethod
    def InvokeDeviceAction( # pylint: disable=invalid-name
        self, device_handle: Str, notification_id: UInt32, is_positive: Bool
    ):
        """
        Invoke an action on the ANCS device

        :param device_handle: the handle of the specified device
        :param notification_id: the id of the intended notification action
        :param is_positive: if the action is positive
        """

    DismissNotification: dbus_signal
    ShowNotification: dbus_signal
