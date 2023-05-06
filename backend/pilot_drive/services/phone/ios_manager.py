"""
The iOS notification manager for PILOT Drive phone notifications
"""

import json
from typing import List, Dict
from dasbus.typing import ObjPath, Str, Variant

from pilot_drive.master_logging import MasterLogger
from ..bluetooth import Bluetooth, BluetoothDevice
from ..shared.bluez_api import BluezDevice, BluezAdapter
from .constants import Notification, PhoneStates
from .exceptions import NoANCSDeviceConnectedException


class IOSManager:
    """
    Abstract manager that to encourage proper implementation of Android/iOS devices
    """

    def __init__(self, logger: MasterLogger, bluetooth: Bluetooth) -> None:
        self.logger = logger
        self.__notifications: List[Notification] = []
        self.bluetooth = bluetooth
        self.__devices: List[BluetoothDevice] = []

    @property
    def notifications(self) -> List[Notification]:
        """
        Get the list of aggregated notifications

        :return: a list of notifications collected by the manager
        """
        if self.bluetooth.active_ancs_devices:
            return self.__notifications

        raise NoANCSDeviceConnectedException(
            "Cannot get device notifications, none connected!"
        )

    @property
    def state(self) -> PhoneStates:
        """
        Return the state of the connected ANCS device

        :return: the current state of the phone via the PhoneState attribute
        """
        if not self.bluetooth.bluez_adapter.Powered:
            return PhoneStates.BLUETOOTH_DISABLED

        # Get a list of connected devices
        connected_devices = [device for device in self.__devices if device.connected]

        if self.bluetooth.active_ancs_devices and connected_devices:
            return PhoneStates.CONNECTED

        return PhoneStates.DISCONNECTED

    @property
    def device_name(self) -> str:
        """
        Get the name of the connected device

        :return: the name of the connected device
        """
        ancs_devices = self.bluetooth.active_ancs_devices

        if not ancs_devices:
            raise NoANCSDeviceConnectedException(
                "Cannot get device name, none connected!"
            )

        for device in self.__devices:
            # Temporarily assume the first device in the ANCS list is the intended one
            if device.address.upper() == ancs_devices[0].upper():
                return device.name

        raise NoANCSDeviceConnectedException("Failed to get device name!")

    def device_added(
        self, device: BluetoothDevice
    ) -> None:  # pylint: disable=unused-argument
        """
        Callback utilized when a new interface is added

        :param path: DBus path to the new interface
        :param interface: name of the interface that was added
        """
        self.__devices.append(device)

    def interfaces_removed(
        self, path: ObjPath, interfaces: List[Str]
    ) -> None:  # pylint: disable=unused-argument
        """
        Callback utilized when an interface is removed

        :param path: DBus path to the new interface
        :param interface: list of names of interfaces that were removed
        """  # pylint: disable=duplicate-code
        if BluezDevice.interface in interfaces:
            for count, device in enumerate(self.__devices):
                if device.path == path:
                    self.__devices.pop(count)
                    break

        self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)

    def properties_changed(
        self,
        interface: str,
        changes: Dict[str, Variant],  # pylint: disable=unused-argument
        invalidated_properties: List[str],  # pylint: disable=unused-argument
    ) -> None:
        """
        Callback utilized when an interface's properties change

        :param interface: names of interface that had a property change
        :param changes: a dict of changes on the properties of the interface
        :param invalidated_properties: a list of properties that were invalidated
        """
        match interface:
            case BluezAdapter.interface:
                self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)
            case BluezDevice.interface:
                self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)

    # def initialize_observers(self) -> None:
    #     for path, services in self.bluetooth.bluez_root.GetManagedObjects().items():
    #         self.interfaces_added(path, services)

    #     self.bluetooth.bluez_root.InterfacesAdded.connect(self.interfaces_added)
    #     self.bluetooth.bluez_root.InterfacesRemoved.connect(self.interfaces_removed)

    def show_notification(self, notification_json: str) -> None:
        """
        Callback used when a new notification is detected on the iOS device

        :param notification_json: JSON string passed by ANCS containing new notification
        """
        notification = json.loads(notification_json)
        formatted_notif = {
            # Only the last 3 digits of the ID matter, found via trial and error
            "id": int(str(notification["id"])[-3:]),
            "body": notification["body"],
            "app_name": notification["app_name"],
            "app_id": notification["app_id"],
            "title": notification["title"],
            "time": 0,
            "device": notification["device_name"],
        }

        try:
            notif_obj = Notification(**formatted_notif)
            for count, notification in enumerate(self.__notifications):
                if notification.id == notif_obj.id:
                    self.__notifications[count] = notif_obj
                    return

            self.__notifications.append(notif_obj)

        except (
            TypeError
        ) as exc:  # If the needed values didn't exist, don't create the notification object
            self.logger.debug(
                msg=f'Failed to create notification from: "{formatted_notif}": {exc}'
            )

    def dismiss_notification(self, notification_id: int) -> None:
        """
        Callback used when a notification is dismissed on the iOS device

        :param notification_id: integer indicating the notification ID to be dismissed
        """
        # All cases aren't handled, as if an ID doesn't exist it was likely there bfore the device
        # was connected. There is no support for previous notifications, only ones received while
        # connected.
        for count, notification in enumerate(self.__notifications):
            if notification.id == notification_id:
                self.__notifications.pop(count)
                return
