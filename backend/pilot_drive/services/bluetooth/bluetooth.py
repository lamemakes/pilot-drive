"""
Module for the Bluetooth service
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Optional, Callable
from dasbus.connection import (  # type: ignore # missing
    SystemMessageBus,
)
from dasbus.typing import ObjPath, Variant, Str

from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue import MasterEventQueue, EventType

from .exceptions import NoAdapterException, NoPlayerException
from .constants import ANCS_CHARS, MEDIA_UUIDS

from ..shared.bluez_api import (
    MessageBus,
    BluezAdapter,
    BluezDevice,
    BluezMediaPlayer,
    BluezGattCharacteristic,
)
from ..abstract_service import AbstractService


@dataclass
class BluetoothDevice:  # pylint: disable=too-many-instance-attributes
    """
    Dataclass used to store information and states on BlueZ devices.
    """

    bluez_device: BluezDevice = field(repr=False)
    path: ObjPath = field(repr=False)
    props_changed_callback: Callable = field(repr=False)
    logger: MasterLogger = field(repr=False)
    name: str = field(init=False)
    alias: str = field(init=False)
    address: str = field(init=False)
    connected: bool = field(init=False)
    media: bool = field(init=False)
    ancs: bool = False  # This is populated after the device is created

    def __is_av_device(self, device: BluezDevice) -> bool:
        """
        Determine if the BlueZ device is a media device or not based on A2DP UUIDs

        :param device: a BluezDevice instance to check for media profiles on
        :return: True if the device has media capabilities, False if not.
        """
        media_temp_uuids = list(MEDIA_UUIDS)
        for uuid in device.UUIDs:
            if uuid in MEDIA_UUIDS:
                media_temp_uuids.remove(uuid)

        # If the list is empty, it has all media UUIDs and is a media device
        return not media_temp_uuids

    def __post_init__(self):
        self.name = self.bluez_device.Name
        self.alias = self.bluez_device.Alias
        self.address = self.bluez_device.Address
        self.connected = self.bluez_device.Connected
        self.media = self.__is_av_device(device=self.bluez_device)

    def prop_changed(
        self,
        interface: str,
        changes: Dict[str, Variant],
        invalidated_properties: List[Str],
    ) -> None:
        """
        The callback used when a BlueZ device property changed to update internal states

        :param interface: the interface that changed
        :param changes: the changes to device properties
        :invalidated_properties: a list of invalidated properties
        """
        if "Connected" in changes:
            prev_state = self.connected
            self.connected = changes["Connected"].unpack()
            if self.connected != prev_state:
                if self.connected is True:
                    self.logger.info(
                        msg=f"""Bluetooth Device "{self.name}"
                         with address {self.address} has connected."""
                    )
                elif self.connected is False:
                    self.logger.info(
                        msg=f"""Bluetooth Device "{self.name}"
                         with address {self.address} has disconnected."""
                    )

        self.props_changed_callback(interface, changes, invalidated_properties)

    def serialize(self) -> Dict:
        """
        Serializes the BluetoothDevice Object

        :return: a dict of the device's informational attributes.
        """
        # Attributes to removed as they aren't informational/serializable.
        attrs_to_remove = {"bluez_device", "path", "props_changed_callback", "logger"}
        device_dict = self.__dict__.copy()
        for attribute in attrs_to_remove:
            device_dict.pop(attribute)

        return device_dict


class Bluetooth(AbstractService):
    """
    The service that manages the DBus Bluetooth APIs of PILOT Drive.
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
        bus: Optional[MessageBus] = None,
    ):
        """
        Initialize the Bluetooth service.

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on
            the event queue
        :param logger: an instance of MasterLogger
        :param bus: Provide an optional system bus, otherwise one will be created
        """
        super().__init__(master_event_queue, service_type, logger)
        self.bus, self.bluez_root = Bluetooth.get_bus_and_bluez_root(bus=bus)

    def push_bluetooth_to_queue(self, devices: List[BluetoothDevice]) -> None:
        """
        Push bluetooth information to the queue

        :param devices: A list of devices track by the external service using bluetooth. This is
            temporary and will likely be integrated into the Bluetooth service itself soon.
        """
        bluetooth_adapter = self.bluez_adapter

        if (
            bluetooth_adapter.Alias
            and bluetooth_adapter.Alias != bluetooth_adapter.Name
        ):
            hostname = bluetooth_adapter.Alias
        else:
            hostname = bluetooth_adapter.Name

        bluetooth_event = {
            "hostname": hostname,
            "address": bluetooth_adapter.Address,
            "powered": bluetooth_adapter.Powered,
            "devices": self.__serialize_devices(devices),
        }

        self.push_to_queue(event=bluetooth_event)

    def __serialize_devices(self, devices: List[BluetoothDevice]) -> List[Dict]:
        """
        Format devices in a way that the frontend expects/is serializable

        :param: a list containing many BluezDevice instances
        :return: a serialized device list
        """
        serialized_devices = []
        for device in devices:
            serialized_devices.append(device.serialize())

        return serialized_devices

    @staticmethod
    def get_bus_and_bluez_root(
        bus: Optional[MessageBus] = None,
    ) -> Tuple[MessageBus, Any]:
        """
        Get a new instance of the DBus system bus along with the BlueZ root

        :param bus: Provide an optional bus to create a BlueZ root from

        :return: a tuple with the DBus system bus along with the BlueZ root
        """
        if bus is None:
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

    def get_bluez_device(
        self, path: ObjPath, props_changed_callback: Callable
    ) -> BluetoothDevice:
        """
        Create a new BluetoothDevice instace from a BlueZ device path

        :param path: The path to the BlueZ device
        :param props_changed_callback: the callback to connect for when device properties change
        """
        bluez_device = BluezDevice.connect(self.bus, path)
        device = BluetoothDevice(
            path=path,
            bluez_device=bluez_device,
            props_changed_callback=props_changed_callback,
            logger=self.logger,
        )
        return device

    # @property
    # def devices(self) -> List[BluezDevice]:
    #     """
    #     Get a list of all devices - previous and currently connected

    #     :return: a list of BluezDevice instances
    #     """
    #     devices: List[BluezDevice] = []
    #     for path, services in self.bluez_root.GetManagedObjects().items():
    #         if BluezDevice.interface in services:
    #             device_obj = BluezDevice.connect(bus=self.bus, path=path)
    #             devices.append(device_obj)
    #     for device in devices:
    #         #print(device.Name)
    #         print(device.Address)
    #         print(device.Connected)
    #     print()
    #     return devices

    # @property
    # def serialized_devices(self) -> List[BluezDevice]:  # type: ignore
    #     """
    #     Get a list of all connected devices

    #     :return: a list of connected BluezDevice instances
    #     """
    #     devices = self.devices
    #     connected_devices: List[BluezDevice] = []
    #     for device in devices:
    #         if device.Connected:
    #             connected_devices.append(device)

    #     return connected_devices

    # @property
    # def av_devices(self) -> List[str]:
    #     """
    #     Get a list of all connected devices capable of being a media device

    #     :return: a list of connected device MAC addresses capable of being a media device
    #     """
    #     av_list: List[str] = []

    #     # Check that the device has all needed UUIDs for metadata (AVRCP) & audio (A2DP/Source)
    #     temp_uuids = MEDIA_UUIDS
    #     for device in self.connected_devices:
    #         for uuid in device.UUIDs:
    #             if uuid in MEDIA_UUIDS:
    #                 temp_uuids.remove(uuid)

    #         if len(temp_uuids) == 0:
    #             av_list.append(device.Address)

    #     return av_list

    @property
    def active_ancs_devices(self) -> List[str]:
        """
        Get a list of all connected devices that have Apple Notification Center Service (ANCS)
            capabilities

        :return: a list of connected device MAC addresses capable of ANCS
        """

        ancs_devices = []
        for path, services in self.bluez_root.GetManagedObjects().items():
            if BluezGattCharacteristic.interface in services:
                uuid = services[BluezGattCharacteristic.interface]["UUID"].unpack()
                if uuid in ANCS_CHARS:
                    device_path = "/".join(path.split("/")[:-2])
                    device = BluezDevice.connect(bus=self.bus, path=device_path)
                    if device.Connected and device.Address not in ancs_devices:
                        ancs_devices.append(device.Address)

        return ancs_devices

    def refresh(self) -> None:
        """
        Pushes stored bluetooth data to queue
        """
        # self.push_bluetooth_to_queue()

    def main(self) -> None:
        """
        Currently a do-nothing method but may get it's own loop eventually.
        """
