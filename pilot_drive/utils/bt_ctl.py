# TODO: Should the function just set 

from pilot_drive.utils.bt_track import Track
from dbus.mainloop.glib import DBusGMainLoop    # Handling the DBus event based loop
from gi.repository import GLib                  # Handling the DBus event based loop
from time import sleep
import dbus
import threading
import logging


class BluetoothManager:
    def __init__(self):
        # Initialize the logger
        self.log = logging.getLogger()

        # Temp variable for the DBus Bluetooth player interface
        self.bt_player_iface = None  

        # General Info Variables
        self.connected = False
        self.device_name = None
        self.device_addr = None
        self.volume = None

        # Track Variables
        self.track_info = None


########## Utility/Info Getting Methods ##########

    def get_conn_device(self):
        for path, ifaces in self.mgr.GetManagedObjects().items():
            if "org.bluez.Device1" in str(ifaces):          
                # Check for device connecton, set name if connected.
                if ifaces["org.bluez.Device1"]["Connected"]:
                    self.log.debug(str(ifaces["org.bluez.Device1"]))                                             
                    self.device_name = ifaces["org.bluez.Device1"]["Name"]
                    self.device_addr = ifaces["org.bluez.Device1"]["Address"]
                    self.log.info("Bluetooth device: " + self.device_name + " connected with MAC address of " + self.device_addr + ".")
                    self.connected = True


    # Get the status of the current track (paused, playing)
    def get_track_status(self):
        self.status = self.track.status


    # Sets a dict object with all track metadata contained in it.
    def get_track_data(self):

        # If there's no active track playing, Sets none.
        if not self.track.active_track or not self.track:
            self.track_info = {
            "title" : None,
            "artist" : None,
            "album" : None,
            "duration" : None,
            "position" : None
            }

        else:
            self.track_info = {
            "title" : self.track.title,
            "artist" : self.track.artist,
            "album" : self.track.album,
            "duration" : self.track.duration,
            "position" : self.track.position  
            }

        # Update the status of the track
        self.get_track_status()


########## Signal Reciever Methods ##########

    def iface_added(self, path, iface):
        if "org.bluez.MediaTransport1" in str(iface):
            transport_mgr = iface["org.bluez.MediaTransport1"]
            self.volume = transport_mgr["Volume"]

        elif "org.bluez.MediaPlayer1" in str(iface):
            player_mgr = iface["org.bluez.MediaPlayer1"]
            self.position = player_mgr["Position"]

        if not self.connected:
            # If a device isn't already connected, changed the connected status and get the device name
            self.connected = True
            self.get_conn_device()
        

    def iface_removed(self, path, iface):
        self.connected = False


    def prop_changed(self, iface, changed, invalidated):
        # TODO: Sync volume control here, seems to be an update field.
        if "Title" in str(changed.items()):
            if "org.bluez.MediaPlayer1" in str(iface):
                self.log.debug("Track properties updated: " + str(changed.items()))
                self.track = Track(self.mgr) 
                self.track.get_track(changed)
                self.get_track_data()


########## Main Methods ########## 

    def bluetooth_manager(self):
        # Start the main loop
        DBusGMainLoop(set_as_default=True)

        # Initialize DBus interface to read from
        self.bus = dbus.SystemBus()

        # Create the object manager
        self.mgr = dbus.Interface(self.bus.get_object("org.bluez", "/"), 'org.freedesktop.DBus.ObjectManager')

        # Initialize the Track object
        self.track = Track(self.mgr)

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
    
    # Implements controls such as pause, play, skip, back, etc...
    def bluetooth_ctl(self, control):
        for path, ifaces in self.mgr.GetManagedObjects().items():
            if "org.bluez.MediaPlayer1" in str(ifaces):  
                player_iface = dbus.Interface(self.bus.get_object('org.bluez', path), 'org.bluez.MediaPlayer1')

                # A dictionary of controls and their corresponding method calls
                controls = {
                    "play" : player_iface.Play,
                    "pause" : player_iface.Pause,
                    "next" : player_iface.Next,
                    "prev" : player_iface.Previous
                }

                # Do the control specified by parameter via the dict
                controls[control]()


    def run(self):
        metaThr = threading.Thread(target=self.bluetooth_manager, name = 'bluetooth_manager', daemon=True)
        metaThr.start()


if __name__ == "__main__":
    # Testing of the bt_ctl & bt_track class.

    newBlue = BluetoothManager()
    newBlue.run()
    
    def main():

        # A delay is neccesary to allow the threads to start and initialize the dbus object manager.
        sleep(0.01)

        newBlue.get_track_data()

        track = newBlue.track_info
        status = newBlue.status

        if newBlue.track_info:
            for key in newBlue.track_info.keys():
                print(key.capitalize() + " : " + str(newBlue.track_info[key]))
                track = newBlue.track_info
            print("-" * 32)

        while True:
            if newBlue.track_info != track:
                for key in newBlue.track_info.keys():
                    print(key.capitalize() + " : " + str(newBlue.track_info[key]))
                    track = newBlue.track_info
                print("-" * 32)

            if newBlue.status != status:
                print("Status : " + status)
                status = newBlue.status
                print("-" * 32)
        
            sleep(0.01)

    mainThr = threading.Thread(target=main, name = 'main', daemon=True)
    mainThr.start()

    sleep(0.5)

    # Loop to add control of the track. Sleep is neccesary to allow track status to update
    while True:
        print("Command Input")
        command = input("Command:")
        newBlue.bluetooth_ctl(command)
        sleep(.5)
        print(("*" * 8) + newBlue.status)
