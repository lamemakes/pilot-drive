"""
Module for the Bluetooth service
"""
from typing import Any, Dict, List, Tuple
from dasbus.connection import (  # type: ignore # missing
    SystemMessageBus,
)
from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue import MasterEventQueue, EventType

from .exceptions import NoAdapterException, NoPlayerException
from .constants import MEDIA_UUIDS

from ..shared.bluez_api import (
    MessageBus,
    BluezAdapter,
    BluezDevice,
    BluezMediaPlayer,
)
from ..abstract_service import AbstractService


class Bluetooth(AbstractService):
    """
    The service that manages the DBus Bluetooth APIs of PILOT Drive.
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
    ):
        """
        Initialize the Bluetooth service.

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on
        the event queue
        """
        super().__init__(master_event_queue, service_type, logger)
        self.bus, self.bluez_root = Bluetooth.get_bus_and_bluez_root()

    def push_bluetooth_to_queue(self) -> None:
        """
        Push bluetooth information to the queue
        """
        bluetooth_adapter = self.bluez_adapter
        bluetooth_event = {
            "hostname": bluetooth_adapter.Name,
            "address": bluetooth_adapter.Address,
            "powered": bluetooth_adapter.Powered,
            "devices": self.__serialize_devices(self.devices),
        }
        self.push_to_queue(event=bluetooth_event)

    def __serialize_devices(self, devices: List[BluezDevice]) -> List[Dict]:
        """
        Format devices in a way that the frontend expects/is serializable

        :param: a list containing many BluezDevice instances
        :return: a serialized device list
        """
        serialized_devices: List[Dict] = []
        for device in devices:
            serialized_devices.append(
                {
                    "name": device.Name,
                    "address": device.Address,
                    "connected": device.Connected,
                    "isMediaSource": device.Address in self.av_devices,
                }
            )

        return serialized_devices

    @staticmethod
    def get_bus_and_bluez_root() -> Tuple[MessageBus, Any]:
        """
        Get a new instance of the DBus system bus along with the BlueZ root

        :return: a tuple with the DBus system bus along with the BlueZ root
        """
        bus = SystemMessageBus()
        return bus, bus.get_proxy("org.bluez", "/")

    @property
    def bluez_adapter(self) -> BluezAdapter:
        """
        Get the BlueZ Adapter1

        :return: a BluezAdapter instance
        """
        for path, services in self.bluez_root.GetManagedObjects().items():
            if BluezAdapter.interface in services:
                adapter_obj = BluezAdapter.connect(bus=self.bus, path=path)
                return adapter_obj

        raise NoAdapterException("No BlueZ Adapter was found!")

    @property
    def bluez_media_player(self) -> BluezMediaPlayer:
        """
        Get the BlueZ MediaPlayer1

        :return: a BluezMediaPlayer instance
        """
        for path, services in self.bluez_root.GetManagedObjects().items():
            if BluezMediaPlayer.interface in services:
                player_obj = BluezMediaPlayer.connect(bus=self.bus, path=path)
                return player_obj

        raise NoPlayerException("No BlueZ media player was found!")

    @property
    def devices(self) -> List[BluezDevice]:
        """
        Get a list of all devices - previous and currently connected

        :return: a list of BluezDevice instances
        """
        devices: List[BluezDevice] = []
        for path, services in self.bluez_root.GetManagedObjects().items():
            if BluezDevice.interface in services:
                device_obj = BluezDevice.connect(bus=self.bus, path=path)
                devices.append(device_obj)
        for device in devices:
            print(device.Address)
            print(device.Connected)
        print()
        return devices

    @property
    def connected_devices(self) -> List[BluezDevice]:  # type: ignore
        """
        Get a list of all connected devices

        :return: a list of connected BluezDevice instances
        """
        devices = self.devices
        connected_devices: List[BluezDevice] = []
        for device in devices:
            if device.Connected:
                connected_devices.append(device)

        return connected_devices

    @property
    def av_devices(self) -> List[str]:
        """
        Get a list of all connected devices capable of being a media device

        :return: a list of connected device MAC addresses capable of being a media device
        """
        av_list: List[str] = []

        # Check that the device has all needed UUIDs for metadata (AVRCP) & audio (A2DP/Source)
        temp_uuids = MEDIA_UUIDS
        for device in self.connected_devices:
            for uuid in device.UUIDs:
                if uuid in MEDIA_UUIDS:
                    temp_uuids.remove(uuid)

            if len(temp_uuids) == 0:
                av_list.append(device.Address)

        return av_list

    def refresh(self) -> None:
        """
        Pushes stored bluetooth data to queue
        """
        self.push_bluetooth_to_queue()

    def main(self) -> None:
        """
        Currently a do-nothing method but may get it's own loop eventually.
        """
