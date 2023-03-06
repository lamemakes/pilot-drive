import json
from dbus.mainloop.glib import DBusGMainLoop    # Handling the DBus event based loop
from gi.repository import GLib                  # Handling the DBus event based loop
import dbus

from constants import MediaSources, IFaceTypes, TrackAttributes, Status, BluetoothDevice, MediaItemAttributes, MediaPlayerAttributes, MediaTransportAttributes
from services import AbstractService
from MasterEventQueue import MasterEventQueue, EventType


class Bluetooth(AbstractService):
    def __init__(self, master_event_queue: MasterEventQueue, service_type: EventType):
        super().__init__(master_event_queue, service_type)

        self.__reset_vars()


    '''
    Utility Methods
    '''
    def __reset_vars(self):
        self.bluetooth = {
            'connected': False,
            'connectedName': None,
            'localHostname': None,
            'battery': None,
            'address': None
        }

        self.media = {
            'source': MediaSources.BLUETOOTH.value,
            'song': {
                'title': None,
                'artist': None,
                'album': None,
                'duration': None,
                'position': None,
                'isPlaying': False,
                'cover': None
            }

        }

    def __push_media_to_queue(self):
        media_json = self.media
        self.event_queue.push_event(event_type=EventType.MEDIA.value, event_json=media_json)


    def __handle_connect(self, connected:bool = None):
        if connected == None:
            device = self.__get_iface_items(IFaceTypes.DEVICE_1)
            connected = device.get(BluetoothDevice.CONNECTED.value)
        

        if connected:
            self.bluetooth["connected"] = True
            self.__set_connected_device()
            self.__set_track()
            self.__set_status()
            self.__set_position()
            self.push_to_queue(self.bluetooth)
            self.__push_media_to_queue()
        else:
            self.__reset_vars()
            self.push_to_queue(self.bluetooth)
            self.__push_media_to_queue()


    def __get_iface_items(self, iface: IFaceTypes):
        for path, ifaces in self.mgr.GetManagedObjects().items():
            if iface.value in str(ifaces):
                return ifaces[iface.value]
            
        return None


    def __set_connected_device(self):
        iface_items = self.__get_iface_items(IFaceTypes.DEVICE_1)
        if iface_items:                                  
                device_name = iface_items.get(BluetoothDevice.NAME.value)
                device_addr = iface_items.get(BluetoothDevice.ADDRESS.value)
                print('Bluetooth device: ' + device_name + ' connected with MAC address of ' + device_addr + '.') # TODO: Add logging
                self.bluetooth['connectedName'] = device_name
                self.bluetooth['address'] = device_addr


    def __set_status(self, changed_props: dbus.Dictionary=None):
        status = None
        try:
            if self.bluetooth['connected']:
                # If being passed changed props use them, but if nothing is passed check in the managed items for track info
                if changed_props:
                    status = changed_props
                else:
                    status = self.__get_iface_items(IFaceTypes.MEDIA_PLAYER_1)

                status = status.get(MediaPlayerAttributes.STATUS.value)

                self.media['song']['isPlaying'] = True if status == Status.PLAYING.value else False
            
        except dbus.exceptions.DBusException as e:
            print(e)    # TODO: Logging...


    def __set_position(self, changed_props: dbus.Dictionary=None):
        position = None
        try:
            if self.bluetooth['connected']:
                # If being passed changed props use them, but if nothing is passed check in the managed items for track info
                if changed_props:
                    position = changed_props
                else:
                    position = self.__get_iface_items(IFaceTypes.MEDIA_PLAYER_1)

                position = int(position.get(MediaPlayerAttributes.POSITION.value))

                self.media['song']['position'] = position 
            
        except dbus.exceptions.DBusException as e:
            print(e)    # TODO: Logging...


    def __set_track(self, changed_props: dbus.Dictionary=None):
        track = None
        try:
            if self.bluetooth['connected']:
                # If being passed changed props use them, but if nothing is passed check in the managed items for track info
                if changed_props:
                    track = changed_props
                else:
                    track = self.__get_iface_items(IFaceTypes.MEDIA_PLAYER_1)

                track = track.get(MediaPlayerAttributes.TRACK.value)

                # Set all needed values to be able to pull track metadata when class is instantiated.
                if track:
                    # Set values as default to prevent previous values from leaching over if values aren't populated
                    metadata = {
                        'title': '', 
                        'artist': '', 
                        'album': '', 
                        'duration': ''
                    }

                    EMPTY = ''

                    print(track)

                    if track:
                        metadata['title'] = str(track.get(TrackAttributes.TITLE.value)) if track.get(TrackAttributes.TITLE.value) else EMPTY
                        metadata['artist'] = str(track.get(TrackAttributes.ARTIST.value)) if track.get(TrackAttributes.ARTIST.value) else EMPTY
                        metadata['album'] = str(track.get(TrackAttributes.ALBUM.value)) if track.get(TrackAttributes.ALBUM.value) else EMPTY
                        metadata['duration'] = str(track.get(TrackAttributes.DURATION.value)) if track.get(TrackAttributes.DURATION.value) else EMPTY
                    
                        self.media['song'] = {**self.media['song'], **metadata} # Set track vars, but preserve everything else

                    print(self.media)
            
        except dbus.exceptions.DBusException as e:
            print(e)    # TODO: Logging...

    '''
    Signal Reciever Methods
    '''
    def iface_added(self, path, iface):
        pass

    def iface_removed(self, path, iface):
        print('*******IFACE REMOVED: ' + str(iface))
        print()
        self.connected = False


    def prop_changed(self, iface: str, changed: dbus.Dictionary, invalidated: dbus.Array):
        '''
        Callback for a change event on the bluez bus

        :param iface: The interface from where the change occurred
        :param changed: The props that have changed (ie. "dbus.Dictionary({dbus.String('Position'): dbus.UInt32(671, variant_level=1)}, signature=dbus.Signature('sv'))")
        :param invalidated: Invalidated DBus props
        '''

        changed_key = list(changed.keys())[0]   # In my experience, changed will never return more than one top-level key.

        match changed_key:
            case BluetoothDevice.CONNECTED.value:
                self.__handle_connect(connected=changed.get(BluetoothDevice.CONNECTED.value))
            case MediaPlayerAttributes.TRACK.value:
                self.__set_track(changed_props=changed)
            case MediaPlayerAttributes.STATUS.value:
                self.__set_status(changed_props=changed)
            case MediaPlayerAttributes.POSITION.value:
                self.__set_position(changed_props=changed)
            case MediaItemAttributes.METADATA.value:        # This returns duplicate information to "Track". Don't waste processing power on it
                return
            case MediaTransportAttributes.STATE.value:      # Also not useful at the moment. Indicates active/idle. May be implemented later.
                return 
            case _:
                print("Unrecognized key: " + changed_key)
                return

        # Push the changes to the Queue to be sent to the frontend.
        self.__push_media_to_queue()


    '''
    Run the main loop
    '''
    def main(self):
        # Start the main loop
        DBusGMainLoop(set_as_default=True)

        # Initialize DBus interface to read from
        self.bus = dbus.SystemBus()

        # Create the object manager
        self.mgr = dbus.Interface(self.bus.get_object('org.bluez', '/'), 'org.freedesktop.DBus.ObjectManager')

        # Create a receiver to monitor for a newly connected device
        self.bus.add_signal_receiver(
            self.iface_added, 
            signal_name='InterfacesAdded', 
            dbus_interface='org.freedesktop.DBus.ObjectManager', 
            bus_name='org.bluez')

        # Create a receiver to monitor for a disconnected device
        self.bus.add_signal_receiver(
            self.iface_removed, 
            signal_name='InterfacesRemoved', 
            dbus_interface='org.freedesktop.DBus.ObjectManager', 
            bus_name='org.bluez')

        # Create a reciever to monitor song changes
        self.bus.add_signal_receiver(
            self.prop_changed,
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties',
            bus_name='org.bluez')

        self.__handle_connect()
            
        GLib.MainLoop().run()