from typing import List
from .abstract_manager import AbstractManager
from pilot_drive.MasterEventQueue import MasterEventQueue
import dbus
import json

from ..BluetoothUtils.constants import IFaceTypes, Device, AdapterAttributes
from .phone_constants import PHONE_STATES

class MissingDBusPropertyException(Exception):
    pass

class IOSManager(AbstractManager):
    def __init__(self, logger: MasterEventQueue) -> None:
        self.logger = logger
        # self.__bus = None
        # self.__mgr = None
        self.__reset()  # Initialize resetable vars

    def __reset(self):
        self.__notifications: List[dict] = []
        # self.__device_name = None

    # Util Methods
    def parse_notification(self, notification_str: str) -> dict:
        notif_dict = json.loads(notification_str)
        return notif_dict

    @property
    def bus(self):
        if self.__bus == None:
            raise MissingDBusPropertyException('A bus was not provided!')
        
        return self.__bus
    
    @bus.setter
    def bus(self, bus):
        self.__bus = bus

    # @property
    # def enabled(self):
    #     """
    #     The property for the bluetooth power state of the host (ie. if bluetooth is enabled or not). 

    #     :return: boolean of if system-wide bluetooth is enabled or not
    #     """

    #     try:
    #         bus = self.bus
    #         mgr = self.mgr
    #     except AttributeError:
    #         bus = dbus.SystemBus()
    #         mgr = dbus.Interface(
    #         bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")

    #     enabled = None
    #     enabled = self.__get_iface_items(IFaceTypes.ADAPTER_1, mgr=mgr)[0]
    #     enabled = enabled.get(AdapterAttributes.POWER_STATE)

    #     try:
    #         if self.__enabled != enabled:   # state change

    #             self.__enabled = enabled
    #     except AttributeError:
    #         self.__enabled = enabled

    #     return (enabled == "on")

    # @property
    # def state(self):
    #     """
    #     Handles the bluetooth device connection state. When used with the prop_changed callback, the connection properties can be fed directly to the method, rather than making a new DBus query.

    #     :param changed_props: Optional DBus dictionary of changed props
    #     """
    #     self.__handle_connect()
    #     return self.__state
    
    # @state.setter
    # def state(self, new_state: PHONE_STATES):
    #     self.__state = new_state
    
    @property
    def state(self):
        return PHONE_STATES.CONNECTED

    @property
    def notifications(self) -> List[dict]:
        return self.__notifications

    @property
    def device_name(self):
        return 'Yeebus'
    
    @device_name.setter
    def device_name(self, device_name: str):
        self.__device_name = device_name

    '''
    DBus BlueZ methods, many of these are pulled and modified from Bluetooth.py service
    TODO: Make bluetooth utils modular and usable from both this and the bluetooth service
    '''
    # def __get_iface_items(self, iface: IFaceTypes, mgr = None):
    #     """
    #     A getter for the items of a specified interface.

    #     :return: an array of DBus items from each instance of the interface (ie. Device1 will return an array containing each device & it's properties.)
    #     """
    #     if mgr == None:
    #         mgr = self.mgr

    #     iface_items = []
    #     for path, ifaces in mgr.GetManagedObjects().items():
    #         if iface in str(ifaces):
    #             iface_items.append(ifaces[iface])

    #     return iface_items if len(iface_items) > 0 else None
    
    # def __handle_connect(self, changed_props: dbus.Dictionary = None):
    #     """
    #     Handles the bluetooth device connection state. Sets the connection state on the Bluetooth.bluetooth object. When used with the prop_changed callback, the connection properties can be fed directly to the method, rather than making a new DBus query.

    #     :param changed_props: Optional DBus dictionary of changed props
    #     """
    #     connected = False
    #     if self.enabled:
    #         if changed_props:
    #             connected = changed_props
    #         else:
    #             for device in self.__get_iface_items(IFaceTypes.DEVICE_1):
    #                 if device.get(Device.CONNECTED):
    #                     connected = True
    #                     self.device_name = device.get(Device.NAME)

    #         if connected:
    #             self.state = PHONE_STATES.CONNECTED
    #         else:
    #             self.state = PHONE_STATES.DISCONNECTED
    #             self.__reset()
    #     else:
    #         self.state = PHONE_STATES.BLUETOOTH_DISABLED


    '''
    DBus signal reciever methods
    '''
    def show_notification(self, notification_str: str):
        notif = self.parse_notification(notification_str)
        self.__notifications.append(notif)

    def dismiss_notification(self, notification_str: str):
        print("***DISMISS NOTIFICATION: ")
        print(notification_str)
        pass

    # def iface_added(self, path, iface):
    #     """
    #     Callback for when an interface is added. This typically means the device is connected, but calls the handle_connect method to confirm.

    #     :param path: the path to the specified removed interface
    #     :param iface: the interface that was removed
    #     """
    #     self.__handle_connect()

    # def iface_removed(self, path, iface):
    #     """
    #     Callback for when an interface is removed. This typically means the device disconnected, but calls the handle_connect method to confirm.

    #     :param path: the path to the specified removed interface
    #     :param iface: the interface that was removed
    #     """
    #     self.__handle_connect()
