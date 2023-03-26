import json
from dbus.mainloop.glib import DBusGMainLoop  # Handling the DBus event based loop
from gi.repository import GLib  # Handling the DBus event based loop
import dbus
import socket

from constants import (
    AdapterAttributes,
    MediaSources,
    IFaceTypes,
    TrackAttributes,
    TrackControl,
    TrackStatus,
    Device,
    MediaItemAttributes,
    MediaPlayerAttributes,
    MediaTransportAttributes,
)
from services import AbstractService
from MasterEventQueue import MasterEventQueue, EventType


class Bluetooth(AbstractService):
    """
    The service that manages the bluetooth media of PILOT Drive.
    """

    def __init__(self, master_event_queue: MasterEventQueue, service_type: EventType):
        super().__init__(master_event_queue, service_type)

        self.__local_hostname = socket.gethostname()
        self.bluetooth = None
        self.__reset_vars()

    """
    Utility Methods
    """

    def __reset_vars(self):
        """
        Cleanses the diffent internal states. Intended to prevent leaching of values.
        """

        # If the class has already been initialized and the cars are just being cleaned, preserve the bluetooth enabled var
        if self.bluetooth:
            is_enabled = self.bluetooth["enabled"]
        else:
            is_enabled = False

        self.bluetooth = {
            "enabled": is_enabled,
            "connected": False,
            "connectedName": None,
            "localHostname": self.__local_hostname,
            "battery": None,
            "address": None,
        }

        self.media = {
            "source": MediaSources.BLUETOOTH,
            "song": {
                "title": None,
                "artist": None,
                "album": None,
                "duration": None,
                "position": None,
                "isPlaying": False,
                "cover": None,
            },
        }

    def __push_media_to_queue(self):
        """
        Similar to the push_to_queue method, but pushes the media object to the event queue with the type of "media"
        """
        media_json = self.media
        self.event_queue.push_event(event_type=EventType.MEDIA, event=media_json)

    def __handle_connect(self, changed_props: dbus.Dictionary = None):
        """
        Handles the bluetooth device connection state. Sets the connection state on the Bluetooth.bluetooth object. When used with the prop_changed callback, the connection properties can be fed directly to the method, rather than making a new DBus query.

        :param changed_props: Optional DBus dictionary of changed props
        """
        connected = False
        if self.bluetooth["enabled"]:
            if changed_props:
                connected = changed_props
            else:
                for device in self.__get_iface_items(IFaceTypes.DEVICE_1):
                    if device.get(Device.CONNECTED):
                        connected = True
                        device_name = device.get(Device.NAME)
                        device_addr = device.get(Device.ADDRESS)
                        print(
                            "Bluetooth device: "
                            + device_name
                            + " connected with MAC address of "
                            + device_addr
                            + "."
                        )  # TODO: Add logging
                        self.bluetooth["connectedName"] = device_name
                        self.bluetooth["address"] = device_addr

            if connected:
                self.bluetooth["connected"] = True
                self.__set_track()
                self.__set_status()
                self.__set_position()
            else:
                self.__reset_vars()
        else:
            print("Enable bluetooth to proceed!")

        self.push_to_queue(self.bluetooth)
        if self.bluetooth["connected"]:
            self.__push_media_to_queue()

    def __get_iface_items(self, iface: IFaceTypes):
        """
        A getter for the items of a specified interface.

        :return: an array of DBus items from each instance of the interface (ie. Device1 will return an array containing each device & it's properties.)
        """
        iface_items = []
        for path, ifaces in self.mgr.GetManagedObjects().items():
            if iface in str(ifaces):
                iface_items.append(ifaces[iface])

        return iface_items if len(iface_items) > 0 else None

    def __set_powered(self, changed_props: dbus.Dictionary = None):
        """
        The setter for the bluetooth power state of the host (ie. if bluetooth is enabled or not). Sets power state/enabled within the Bluetooth.bluetooth object. When used with the prop_changed callback, the changed power state properties can be fed directly to the method, rather than making a new DBus query.

        :param changed_props: Optional DBus dictionary of changed props
        """
        enabled = None
        if changed_props:
            enabled = changed_props
        else:
            enabled = self.__get_iface_items(IFaceTypes.ADAPTER_1)[0]

        enabled = enabled.get(AdapterAttributes.POWER_STATE)

        self.bluetooth["enabled"] = (
            enabled == "on"
        )  # Other states exist for PowerState, like "off", "off-enabling", "off-disabling", and "off-blocked". For all intensive purposes here though, it's either on of off.

    def __set_status(self, changed_props: dbus.Dictionary = None):
        """
        The setter for the track status. Sets status attributes within the Bluetooth.media object. When used with the prop_changed callback, the changed status properties can be fed directly to the method, rather than making a new DBus query.

        :param changed_props: Optional DBus dictionary of changed props
        """
        status = None
        try:
            if self.bluetooth["connected"]:
                # If being passed changed props use them, but if nothing is passed check in the managed items for track info
                if changed_props:
                    status = changed_props
                else:
                    status = self.__get_iface_items(IFaceTypes.MEDIA_PLAYER_1)[0]

                try:
                    status = status.get(MediaPlayerAttributes.STATUS)

                    self.media["song"]["isPlaying"] = (
                        True if status == TrackStatus.PLAYING else False
                    )
                except AttributeError:
                    return  # Likely that the track wasn't loaded yet, ie. the device just connected and hasn't sent it yet.

        except dbus.exceptions.DBusException as e:
            print(e)  # TODO: Logging...

    def __set_position(self, changed_props: dbus.Dictionary = None):
        """
        The setter for the timestamp of the track. Sets position attributes within the Bluetooth.media object. When used with the prop_changed callback, the changed position properties can be fed directly to the method, rather than making a new DBus query.

        :param changed_props: Optional DBus dictionary of changed props
        """
        position = None
        try:
            if self.bluetooth["connected"]:
                # If being passed changed props use them, but if nothing is passed check in the managed items for track info
                if changed_props:
                    position = changed_props
                else:
                    position = self.__get_iface_items(IFaceTypes.MEDIA_PLAYER_1)[0]

                try:
                    position = position.get(MediaPlayerAttributes.POSITION)

                    self.media["song"]["position"] = position if position else None
                except AttributeError:
                    return  # Likely that the track wasn't loaded yet, ie. the device just connected and hasn't sent it yet.

        except dbus.exceptions.DBusException as e:
            print(e)  # TODO: Logging...

    def __set_track(self, changed_props: dbus.Dictionary = None):
        """
        The setter for the track. Sets track attributes within the Bluetooth.media object. When used with the prop_changed callback, the changed track properties can be fed directly to the method, rather than making a new DBus query.

        :param changed_props: Optional DBus dictionary of changed props
        """
        track = None
        try:
            if self.bluetooth["connected"]:
                # If being passed changed props use them, but if nothing is passed check in the managed items for track info
                if changed_props:
                    track = changed_props
                else:
                    track = self.__get_iface_items(IFaceTypes.MEDIA_PLAYER_1)[0]

                try:
                    track = track.get(MediaPlayerAttributes.TRACK)

                    # Set all needed values to be able to pull track metadata when class is instantiated.
                    if track:
                        # Set values as default to prevent previous values from leaching over if values aren't populated
                        metadata = {}

                        EMPTY = ""

                        if track.get(
                            TrackAttributes.TITLE
                        ):  # if the track doesn't have a title, there is no real point in displaying.
                            metadata["title"] = (
                                str(track.get(TrackAttributes.TITLE))
                                if track.get(TrackAttributes.TITLE)
                                else EMPTY
                            )
                            metadata["artist"] = (
                                str(track.get(TrackAttributes.ARTIST))
                                if track.get(TrackAttributes.ARTIST)
                                else EMPTY
                            )
                            metadata["album"] = (
                                str(track.get(TrackAttributes.ALBUM))
                                if track.get(TrackAttributes.ALBUM)
                                else EMPTY
                            )
                            metadata["duration"] = (
                                str(track.get(TrackAttributes.DURATION))
                                if track.get(TrackAttributes.DURATION)
                                else EMPTY
                            )

                            self.media["song"] = {
                                **self.media["song"],
                                **metadata,
                            }  # Set track vars, but preserve everything else
                except AttributeError:
                    return  # Likely that the track wasn't loaded yet, ie. the device just connected and hasn't sent it yet.

        except dbus.exceptions.DBusException as e:
            print(e)  # TODO: Logging...

    """
    Signal Reciever Methods
    """

    def iface_added(self, path, iface):
        """
        Callback for when an interface is add. This typically means the device is connected, but calls the handle_connect method to confirm.

        :param path: the path to the specified removed interface
        :param iface: the interface that was removed
        """
        self.__handle_connect()

    def iface_removed(self, path, iface):
        """
        Callback for when an interface is removed. This typically means the device disconnected, but calls the handle_connect method to confirm.

        :param path: the path to the specified removed interface
        :param iface: the interface that was removed
        """
        self.__handle_connect()

    def prop_changed(
        self, iface: str, changed: dbus.Dictionary, invalidated: dbus.Array
    ):
        """
        Callback for a change event on the bluez bus

        :param iface: The interface from where the change occurred
        :param changed: The props that have changed (ie. "dbus.Dictionary({dbus.String('Position'): dbus.UInt32(671, variant_level=1)}, signature=dbus.Signature('sv'))")
        :param invalidated: Invalidated DBus props
        """

        changed_key = list(changed.keys())[
            0
        ]  # In my experience, changed will never return more than one top-level key.

        match iface:
            case IFaceTypes.MEDIA_PLAYER_1:
                match changed_key:
                    case MediaPlayerAttributes.TRACK:
                        self.__set_track(changed_props=changed)
                    case MediaPlayerAttributes.STATUS:
                        self.__set_status(changed_props=changed)
                    case MediaPlayerAttributes.POSITION:
                        self.__set_position(changed_props=changed)
            case IFaceTypes.MEDIA_TRANSPORT_1:
                match changed_key:
                    case MediaItemAttributes.METADATA:  # This returns duplicate information to "Track". Don't waste processing power on it
                        return
                    case MediaTransportAttributes.STATE:  # Also not useful at the moment. Indicates active/idle. May be implemented later.
                        return
            case IFaceTypes.ADAPTER_1:
                match changed_key:
                    case AdapterAttributes.POWER_STATE:
                        self.__set_powered(changed_props=changed)
                    case AdapterAttributes.CLASS:  # Class specifies specific bluetooth capabilities, not used at the moment
                        return
            case IFaceTypes.DEVICE_1:
                match changed_key:
                    case Device.CONNECTED:
                        self.__handle_connect(changed_props=changed)
            case _:
                print(
                    'Unrecognized keyword: "'
                    + changed_key
                    + '" from interface: "'
                    + iface
                    + '"'
                )

        # Push the changes to the Queue to be sent to the frontend.
        if self.bluetooth["enabled"] and self.bluetooth["connected"]:
            self.__push_media_to_queue()

    def bluetooth_control(self, action: TrackControl):
        """
        Control the current song

        :param action: the intended control action using the TrackControl enum, ie. Play, Pause, Skip Next or Skip Previous.
        """
        player = None
        bus = dbus.SystemBus()
        mgr = dbus.Interface(
            bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager"
        )
        for path, ifaces in mgr.GetManagedObjects().items():
            if "org.bluez.MediaPlayer1" in str(ifaces):
                player = dbus.Interface(
                    bus.get_object("org.bluez", path), "org.bluez.MediaPlayer1"
                )

        if player:
            match action:
                case TrackControl.PLAY:
                    player.Play()
                case TrackControl.PAUSE:
                    player.Pause()
                case TrackControl.NEXT:
                    player.Next()
                case TrackControl.PREV:
                    player.Previous()
                case _:
                    print(
                        'Unknown bluetooth control action: "' + action + '"!'
                    )  # TODO: Logging!

    """
    Run the main loop
    """

    def main(self):
        """
        Run the main bluetooth DBus loop
        """
        # Start the main loop
        DBusGMainLoop(set_as_default=True)

        # Initialize DBus interface to read from
        self.bus = dbus.SystemBus()

        # Create the object manager
        self.mgr = dbus.Interface(
            self.bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager"
        )

        # Create a receiver to monitor for a newly connected device
        self.bus.add_signal_receiver(
            self.iface_added,
            signal_name="InterfacesAdded",
            dbus_interface="org.freedesktop.DBus.ObjectManager",
            bus_name="org.bluez",
        )

        # Create a receiver to monitor for a disconnected device
        self.bus.add_signal_receiver(
            self.iface_removed,
            signal_name="InterfacesRemoved",
            dbus_interface="org.freedesktop.DBus.ObjectManager",
            bus_name="org.bluez",
        )

        # Create a reciever to monitor song changes
        self.bus.add_signal_receiver(
            self.prop_changed,
            signal_name="PropertiesChanged",
            dbus_interface="org.freedesktop.DBus.Properties",
            bus_name="org.bluez",
        )

        self.__reset_vars()
        self.__set_powered()
        self.__handle_connect()

        GLib.MainLoop().run()

    def refresh(self):
        """
        The refresh method to re-push the current bluetooth & media objects to the mast queue.
        """
        self.push_to_queue(event=self.bluetooth)
        if self.bluetooth["connected"]:
            self.__push_media_to_queue()
