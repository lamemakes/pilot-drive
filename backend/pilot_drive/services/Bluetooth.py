from utils.bt_track import Track
from dbus.mainloop.glib import DBusGMainLoop    # Handling the DBus event based loop
from gi.repository import GLib                  # Handling the DBus event based loop
from time import sleep
import dbus

from services import AbstractService
from MasterEventQueue import MasterEventQueue, EventType

class Bluetooth(AbstractService):
    '''
    The service that manages Bluetooth for PILOT Drive, such as media being played, devices connected, etc.
    '''
    def __init__(self, master_event_queue: MasterEventQueue, service_type: EventType):
        super().__init__(master_event_queue, service_type)


    def get_current_track(self):
        try:
            # Create the initial track object to be used to get info on the track
            for path, iface in mgr.GetManagedObjects().items():
                if "org.bluez.MediaPlayer1" in str(iface):
                    self.track_obj = iface.get("org.bluez.MediaPlayer1")

            self.active_track = False
            self.status = None

            # Set all needed values to be able to pull track metadata when class is instantiated.
            self.get_track()

            if self.active_track:
                if "Status" in str(self.track_obj):
                    self.get_status(self.track_obj)
                # TODO: Implement position
                if "Position" in str(self.track_obj):
                    self.position = ""
                    self.get_position()
        except Exception as err:
            print(err)  # WA DEBUG


    def main(self):
        # Start the main loop
        DBusGMainLoop(set_as_default=True)

        # Initialize DBus interface to read from
        self.bus = dbus.SystemBus()

        # Create the object manager
        self.mgr = dbus.Interface(self.bus.get_object("org.bluez", "/"), 'org.freedesktop.DBus.ObjectManager')

        # Create a receiver to monitor for a newly connected device
        self.bus.add_signal_receiver(
            self.iface_added, 
            signal_name='InterfacesAdded', 
            dbus_interface="org.freedesktop.DBus.ObjectManager", 
            bus_name="org.bluez")

        # Create a receiver to monitor for a disconnected device
        self.bus.add_signal_receiver(
            self.iface_removed, 
            signal_name='InterfacesRemoved', 
            dbus_interface="org.freedesktop.DBus.ObjectManager", 
            bus_name="org.bluez")

        # Create a reciever to monitor song changes
        self.bus.add_signal_receiver(
            self.prop_changed,
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties',
            bus_name='org.bluez')

        self.get_conn_device()
        
            
        GLib.MainLoop().run()