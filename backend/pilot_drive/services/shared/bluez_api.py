"""
Wrappers/API for the DBus BlueZ interface that PILOT Drive utilizes or plans to utilize.

For more info, see: https://github.com/bluez/bluez/tree/master/doc
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast
from dasbus.typing import (  # type: ignore # missing
    Bool,
    Byte,
    ObjPath,
    Str,
    UInt16,
    UInt32,
)

from .dbus_api import PropertiesAPI, ObjectManagerAPI, MessageBus


class BluezBaseApi(ABC):  # pylint: disable=too-few-public-methods
    """
    Base class for the BlueZ APIs
    """

    name = "org.bluez"

    @classmethod
    @abstractmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> Any:
        """
        Get a proxy for the specified API

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: proxy to the specified API
        """


class BluezRootApi(ObjectManagerAPI, ABC):
    """
    Type wrapper for the BlueZ DBus root
    """

    name = "org.bluez"
    path = ObjPath("/")

    @classmethod
    def connect(cls, bus: MessageBus) -> "BluezRootApi":
        """
        Get a proxy to the BlueZ root

        :param bus: an instance of the DBus system bus
        :return: an instance of BluezRootApi
        """
        return cast(BluezRootApi, bus.get_proxy(cls.name, cls.path))


class BluezAdapter(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for the org.bluez.Adapter1

    https://github.com/bluez/bluez/blob/master/doc/adapter-api.txt
    """

    name = "org.bluez"
    interface = "org.bluez.Adapter1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezAdapter":
        """
        Get a proxy for the BlueZ Adapter1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezAdapter
        """
        return cast(BluezAdapter, bus.get_proxy(cls.name, path))

    @abstractmethod
    def StartDiscovery(self) -> None:  # pylint: disable=invalid-name
        """
        This method starts the device discovery session. This
            includes an inquiry procedure and remote device name
            resolving. Use StopDiscovery to release the sessions
            acquired.
        """

    @abstractmethod
    def StopDiscovery(self) -> None:  # pylint: disable=invalid-name
        """
        This method will cancel any previous StartDiscovery
            transaction.
        """

    @abstractmethod
    def RemoveDevice(self, device: ObjPath) -> None:  # pylint: disable=invalid-name
        """
        This removes the remote device object at the given
            path. It will remove also the pairing information

        :param device: path to device to be removed
        """

    @abstractmethod
    def SetDiscoveryFilter(  # pylint: disable=invalid-name
        self, filter_in: Dict
    ) -> None:
        """
        This method sets the device discovery filter for the
            caller. When this method is called with no filter
            parameter, filter is removed.

        :param filter: Dict of filters to be used, for exhaustive list see:
            https://github.com/bluez/bluez/blob/master/doc/adapter-api.txt#L53
        """

    @abstractmethod
    def GetDiscoveryFilters(self) -> List[Str]:  # pylint: disable=invalid-name
        """
        Return available filters that can be given to
        SetDiscoveryFilter.

        :return: current discovery filters
        """

    @abstractmethod
    def ConnectDevice(  # pylint: disable=invalid-name
        self, properties: Dict
    ) -> ObjPath:
        """
        This method connects to device without need of
            performing General Discovery. Connection mechanism is
            similar to Connect method from Device1 interface with
            exception that this method returns success when physical
            connection is established. After this method returns,
            services discovery will continue and any supported
            profile will be connected. There is no need for calling
            Connect on Device1 after this call. If connection was
            successful this method returns object path to created
            device object.

        :param properties: the properties to use to connect to the specified device, for an
            exhaustive list see:
            https://github.com/bluez/bluez/blob/master/doc/adapter-api.txt#L174
        """

    Address: Str
    AddressType: Str
    Name: Str
    Alias: Str
    Class: UInt32
    Powered: Bool
    PowerState: Str
    Discoverable: Bool
    Pairable: Bool
    PairableTimeout: UInt32
    DiscoverableTimeout: UInt32
    Discovering: Bool
    Modalias: Str
    Roles: List[Str]
    ExperimentalFeatures: List[Str]


class BluezDevice(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for the org.bluez.Device1

    https://github.com/bluez/bluez/blob/master/doc/device-api.txt
    """

    name = "org.bluez"
    interface = "org.bluez.Device1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezDevice":
        """
        Get a proxy for the BlueZ Device1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezDevice
        """
        return cast(BluezDevice, bus.get_proxy(cls.name, path))

    @abstractmethod
    def Connect(self) -> None:  # pylint: disable=invalid-name
        """
        This is a generic method to connect any profiles
            the remote device supports that can be connected
            to and have been flagged as auto-connectable on
            our side. If only subset of profiles is already
            connected it will try to connect currently disconnected
            ones.
        """

    @abstractmethod
    def Disconnect(self) -> None:  # pylint: disable=invalid-name
        """
        This method gracefully disconnects all connected
            profiles and then terminates low-level ACL connection.
        """

    @abstractmethod
    def ConnectProfile(self, uuid: Str) -> None:  # pylint: disable=invalid-name
        """
        This method connects a specific profile of this
            device. The UUID provided is the remote service
            UUID for the profile.
        """

    @abstractmethod
    def DisconnectProfile(self, uuid: Str) -> None:  # pylint: disable=invalid-name
        """
        This method disconnects a specific profile of
            this device. The profile needs to be registered
            client profile.
        """

    @abstractmethod
    def Pair(self) -> None:  # pylint: disable=invalid-name
        """
        This method will connect to the remote device,
            initiate pairing and then retrieve all SDP records
            (or GATT primary services).
        """

    @abstractmethod
    def CancelPairing(self) -> None:  # pylint: disable=invalid-name
        """
        This method can be used to cancel a pairing
            operation initiated by the Pair method.
        """

    Adapter: ObjPath
    Address: Str
    AddressType: Str
    AdvertisingData: Dict
    AdvertisingFlags: List[Byte]
    Alias: Str
    Appearance: UInt16
    Blocked: Bool
    Bonded: Bool
    Class: UInt32
    Connected: Bool
    Icon: Str
    LegacyPairing: Bool
    ManufacturerData: Dict
    Modalias: Str
    Name: Str
    Paired: Bool
    RSSI: UInt16
    Sets: List
    ServiceData: Dict
    ServicesResolved: Bool
    Trusted: Bool
    TxPower: UInt16
    UUIDs: List[Str]
    WakeAllowed: Bool


class BluezMediaPlayer(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for the org.bluez.MediaPlayer1
    https://github.com/bluez/bluez/blob/master/doc/media-api.txt#L167
    """

    name = "org.bluez"
    interface = "org.bluez.MediaPlayer1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezMediaPlayer":
        """
        Get a proxy for the BlueZ MediaPlayer1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezMediaPlayer
        """
        return cast(BluezMediaPlayer, bus.get_proxy(cls.name, path))

    @abstractmethod
    def Play(self) -> None:  # pylint: disable=invalid-name
        """
        Resume playback.
        """

    @abstractmethod
    def Pause(self) -> None:  # pylint: disable=invalid-name
        """
        Pause playback.
        """

    @abstractmethod
    def Stop(self) -> None:  # pylint: disable=invalid-name
        """
        Stop playback.
        """

    @abstractmethod
    def Next(self) -> None:  # pylint: disable=invalid-name
        """
        Next item.
        """

    @abstractmethod
    def Previous(self) -> None:  # pylint: disable=invalid-name
        """
        Previous item.
        """

    @abstractmethod
    def FastForward(self) -> None:  # pylint: disable=invalid-name
        """
        Fast forward playback, this action is only stopped when another method in this interface is
            called.
        """

    @abstractmethod
    def Rewind(self) -> None:  # pylint: disable=invalid-name
        """
        Previous item.
        """

    @abstractmethod
    def Press(self, avc_key: Byte) -> None:  # pylint: disable=invalid-name
        """
        Press a specific key to send as through command.
            The key will be released automatically. Use Hold()
            instead if the intention is to hold down the key.

        :param avc_key: the key to be pressed
        """

    @abstractmethod
    def Hold(self, avc_key: Byte) -> None:  # pylint: disable=invalid-name
        """
        Press and hold a specific key to send as through
            command. It is your responsibility to make sure that
            Release() is called after calling this method. The held
            ey will also be released when any other method in this
            interface is called.

        :param avc_key: the key to be pressed
        """

    @abstractmethod
    def Release(self) -> None:  # pylint: disable=invalid-name
        """
        Release the previously held key invoked using Hold().
        """

    Equalizer: Str
    Repeat: Str
    Shuffle: Str
    Scan: Str
    Position: UInt32
    Track: Dict
    Device: ObjPath
    Name: Str
    Type: Str
    Status: Str
    Subtype: Str
    Browsable: Bool
    Searchable: Bool
    Playlist: ObjPath


class BluezNetwork(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for the org.bluez.Network1

    https://github.com/bluez/bluez/blob/master/doc/network-api.txt
    """

    name = "org.bluez"
    interface = "org.bluez.Network1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezNetwork":
        """
        Get a proxy for the BlueZ Network1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezNetwork
        """
        return cast(BluezNetwork, bus.get_proxy(cls.name, path))

    @abstractmethod
    def Connect(self, uuid: Str) -> None:  # pylint: disable=invalid-name
        """
        Connect to the network device and return the network
            interface name. Examples of the interface name are
            bnep0, bnep1 etc.

        :param uuid: uuid can be either one of "gn", "panu" or "nap" (case insensitive) or a
            traditional string representation of UUID or a hexadecimal number.
        """

    @abstractmethod
    def Disconnect(self) -> None:  # pylint: disable=invalid-name
        """
        Disconnect from the network device.
        """

    Connected: Bool
    Interface: Str
    UUID: Str


class BluezMediaTransport(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for org.bluez.MediaTransport1
        getall https://github.com/bluez/bluez/blob/master/doc/media-api.txt#L718
    """

    name = "org.bluez"
    interface = "org.bluez.MediaTransport1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezMediaTransport":
        """
        Get a proxy for the BlueZ MediaTransport1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezMediaTransport
        """
        return cast(BluezMediaTransport, bus.get_proxy(cls.name, path))

    @abstractmethod
    def Acquire(self) -> int:  # pylint: disable=invalid-name
        """
        Acquire transport file descriptor and the MTU for read
        and write respectively.
        """

    @abstractmethod
    def TryAcquire(self) -> int:  # pylint: disable=invalid-name
        """
        Acquire transport file descriptor only if the transport
            is in "pending" state at the time the message is
            received by BlueZ. Otherwise no request will be sent
            to the remote device and the function will just fail
            with org.bluez.Error.NotAvailable.
        """

    @abstractmethod
    def Release(self) -> None:  # pylint: disable=invalid-name
        """
        Releases the file descriptor
        """

    Device: ObjPath
    UUID: Str
    Codec: Byte
    Configuration: List[Byte]
    State: Str
    Delay: UInt16
    Volume: UInt16


class BluezMediaItem(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for the org.bluez.MediaItem1

    https://github.com/bluez/bluez/blob/master/doc/media-api.txt#L464
    """

    name = "org.bluez"
    interface = "org.bluez.MediaItem1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezMediaItem":
        """
        Get a proxy for the BlueZ Item1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezMediaItem
        """
        return cast(BluezMediaItem, bus.get_proxy(cls.name, path))

    @abstractmethod
    def Play(self) -> None:  # pylint: disable=invalid-name
        """
        Play Item
        """

    @abstractmethod
    def AddtoNowPlayer(self) -> None:  # pylint: disable=invalid-name
        """
        Add item to now playing list
        """

    Player: ObjPath
    Name: Str
    Type: Str
    FolderType: Str
    Playable: Bool
    Metadata: Dict


class BluezGattCharacteristic(BluezBaseApi, PropertiesAPI, ABC):
    """
    Type wrapper for the org.bluez.GattCharacteristic1

    https://github.com/bluez/bluez/blob/master/doc/gatt-api.txt#L68
    """

    interface = "org.bluez.GattCharacteristic1"

    @classmethod
    def connect(cls, bus: MessageBus, path: ObjPath) -> "BluezGattCharacteristic":
        """
        Get a proxy for the BlueZ GattCharacteristic1

        :param bus: an instance of the DBus system bus
        :param path: an ObjPath to intended object

        :return: an instance of BluezGattCharacteristic
        """
        return cast(BluezGattCharacteristic, bus.get_proxy(cls.name, path))

    UUID: Str
    Service: ObjPath
