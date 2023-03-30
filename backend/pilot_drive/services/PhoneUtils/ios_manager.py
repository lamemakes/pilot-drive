from dbus.mainloop.glib import DBusGMainLoop  # Handling the DBus event based loop
from gi.repository import GLib  # Handling the DBus event based loop
from .abstract_manager import AbstractManager
from pilot_drive.MasterEventQueue import MasterEventQueue
import dbus
import json


class IOSManager(AbstractManager):
    def __init__(self, logger: MasterEventQueue) -> None:
        self.logger = logger
        self.all_notifs = []

    # Util Methods
    def parse_notification(self, notification_str: str) -> dict:
        return json.loads(notification_str)

    # Signal Reciever Methods

    def show_notification(self, notification_str: str):
        notif = self.parse_notification(notification_str)
        pass

    def dismiss_notification(self, notification_str: str):
        pass

    def main(self):
        """
        Run the main bluetooth DBus loop
        """
        # Start the main loop
        DBusGMainLoop(set_as_default=True)

        # Initialize DBus interface to read from
        self.bus = dbus.SystemBus()

        # Create the object manager
        # self.mgr = dbus.Interface(self.bus.get_object('org.bluez', '/'), 'org.freedesktop.DBus.ObjectManager')

        # Create a receiver to monitor for a newly connected device
        self.bus.add_signal_receiver(
            self.show_notification,
            signal_name="ShowNotification",
            dbus_interface="ancs4linux.Observer",
            bus_name="ancs4linux.Observer",
        )

        # Create a receiver to monitor for a disconnected device
        self.bus.add_signal_receiver(
            self.dismiss_notification,
            signal_name="DismissNotification",
            dbus_interface="ancs4linux.Observer",
            bus_name="ancs4linux.Observer",
        )

        GLib.MainLoop().run()
