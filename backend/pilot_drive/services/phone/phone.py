"""
The module that handles the phone connectivity to PILOT Drive
"""
import time
from typing import Dict, List
from dasbus.loop import EventLoop  # type: ignore # missing
from dasbus.typing import ObjPath, Str, Variant
from dasbus.connection import (  # type: ignore # missing
    SystemMessageBus,
)

from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue.master_event_queue import MasterEventQueue, EventType

from ..settings import Settings
from ..bluetooth import Bluetooth
from ..abstract_service import AbstractService
from ..shared.bluez_api import BluezDevice
from .android_manager import AndroidManager
from .ios_manager import IOSManager
from .ancs_api import ANCSObserver
from .constants import (
    PhoneTypes,
    PhoneStates,
    Notification,
    PhoneContainer,
)


class FailedToReadSettingsException(Exception):
    """
    Raised when the settings have failed to be read
    """


class NoPhoneManagerException(Exception):
    """
    Raised when no phone manager is instantiated
    """


class Phone(AbstractService):
    """
    The phone service that interfaces with the (Android/iOS) connected device
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
        settings: Settings,
    ):
        super().__init__(master_event_queue, service_type, logger)
        self.__settings = settings

        self.__enabled = False

        # Device state variables
        self.__notifications: List[Notification] = []
        self.__state = PhoneStates.DISCONNECTED

        if self.enabled:
            try:
                self.__type = PhoneTypes(self.__settings.get_setting("phone")["type"])
            except ValueError as exc:
                raise FailedToReadSettingsException(
                    f'Invalid phone type provided: {self.__settings.get_setting("phone")["type"]}'
                ) from exc
            except KeyError as exc:
                raise FailedToReadSettingsException(
                    "Failed to retrieve phone settings!"
                ) from exc

            match self.__type:
                case PhoneTypes.ANDROID:
                    self.__phone_manager = AndroidManager(logger=self.logger)
                case PhoneTypes.IOS:
                    self.bus = SystemMessageBus()
                    bluetooth = Bluetooth(
                        master_event_queue=self.event_queue,
                        service_type=EventType.BLUETOOTH,
                        logger=self.logger,
                    )
                    self.__phone_manager = IOSManager(
                        logger=self.logger, bluetooth=bluetooth
                    )
                case _:
                    raise FailedToReadSettingsException("Unrecognized phone type!")
        else:
            self.push_to_queue(PhoneContainer(enabled=False).__dict__)

    def __notification_sort(self, notification: Notification):
        return notification.time

    @property
    def enabled(self) -> bool:
        """
        Checks if phone notifications are enabled & properly typed.

        :return: a boolean of whether the phone is enabled
        """
        phone_settings = self.__settings.get_setting("phone")

        try:
            self.__type = PhoneTypes(self.__settings.get_setting("phone")["type"])
        except ValueError as exc:
            self.__enabled = False
            raise FailedToReadSettingsException(
                f'Invalid phone type provided: {self.__settings.get_setting("phone")["type"]}'
            ) from exc

        settings_enabled = phone_settings.get("enabled") is True
        self.__enabled = settings_enabled

        return settings_enabled

    @property
    def state(self) -> PhoneStates:
        """
        Get the phone state

        :return: the current phone state from PhoneStates
        """
        return self.__phone_manager.state

    def notifications_match(
        self, notif_list1: List[Notification], notif_list2: List[Notification]
    ) -> bool:
        """
        Check if two notification lists are equal

        :param notif_list1: the first list of notifications
        :param notif_list2: the second list of notifications
        :return: a boolean whether the two lists match
        """
        if len(notif_list1) != len(notif_list2):
            return False

        for count, value in enumerate(notif_list1):
            if value != notif_list2[count]:
                return False
        return True

    def __android_loop(self, manager: AndroidManager) -> None:
        """
        The loop used for an android connected device

        :param manager: an instantiated AndroidManager object
        """
        self.push_to_queue(
            PhoneContainer(
                enabled=self.__enabled, type=self.__type.value, state=self.state.value
            ).__dict__
        )
        while True:
            push_notifs = False
            phone_container = PhoneContainer(
                enabled=self.__enabled,
                type=self.__type.value,
                state=self.state.value,
                notifications=self.__notifications,
            )

            if self.state != self.__state:
                self.logger.info(
                    msg=f' Android phone state changed from "{self.__state}" to "{self.state}"'
                )
                self.__state = self.state
                if self.__state == PhoneStates.DISCONNECTED:
                    phone_container.notifications = []
                phone_container.state = self.__state.value
                push_notifs = True

            if self.state == PhoneStates.CONNECTED:
                manager_notifs = manager.notifications
                manager_notifs.sort(key=self.__notification_sort, reverse=True)
                if not self.notifications_match(self.__notifications, manager_notifs):
                    self.__notifications = manager_notifs
                    phone_container.notifications = self.__notifications
                    push_notifs = True

            if push_notifs:
                self.push_to_queue(event=phone_container.__dict__)

            time.sleep(1)

    def __ios__loop(self, manager: IOSManager):
        """
        The loop used for an IOS connected device

        :param manager: an instantiated IOSManager object
        """

        self.push_to_queue(
            PhoneContainer(
                enabled=self.__enabled, type=self.__type.value, state=self.state.value
            ).__dict__
        )

        loop = EventLoop()
        # manager.initialize_observers()
        ancs = ANCSObserver.connect(bus=self.bus)

        def interfaces_added(path: ObjPath, interface: str) -> None:
            if BluezDevice.interface in interface:
                bt_device = manager.bluetooth.get_bluez_device(
                    path=path, props_changed_callback=properties_changed
                )
                bt_device.bluez_device.PropertiesChanged.connect(bt_device.prop_changed)
                manager.device_added(bt_device)
                phone_container = PhoneContainer(
                    enabled=self.__enabled,
                    type=self.__type.value,
                    state=self.state.value,
                    notifications=self.__notifications,
                )
                self.push_to_queue(event=phone_container.__dict__)

        def interfaces_removed(
            self, path: ObjPath, interfaces: List[Str]
        ) -> None:  # pylint: disable=unused-argument
            """
            Callback utilized when an interface is removed

            :param path: DBus path to the new interface
            :param interface: list of names of interfaces that were removed
            """
            manager.interfaces_removed(path=path, interfaces=interfaces)
            phone_container = PhoneContainer(
                enabled=self.__enabled,
                type=self.__type.value,
                state=self.state.value,
                notifications=self.__notifications,
            )
            self.push_to_queue(event=phone_container.__dict__)

        def properties_changed(
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
            manager.properties_changed(
                interface=interface,
                changes=changes,
                invalidated_properties=invalidated_properties,
            )
            phone_container = PhoneContainer(
                enabled=self.__enabled,
                type=self.__type.value,
                state=self.state.value,
                notifications=self.__notifications,
            )
            self.push_to_queue(event=phone_container.__dict__)

        def show_ios_notification(notification_json: str) -> None:
            manager.show_notification(notification_json=notification_json)
            self.__notifications = manager.notifications
            phone_container = PhoneContainer(
                enabled=self.__enabled,
                type=self.__type.value,
                state=self.state.value,
                notifications=self.__notifications,
            )
            self.push_to_queue(event=phone_container.__dict__)

        def dismiss_ios_notification(notification_id: int) -> None:
            manager.dismiss_notification(notification_id=notification_id)
            self.__notifications = manager.notifications
            phone_container = PhoneContainer(
                enabled=self.__enabled,
                type=self.__type.value,
                state=self.state.value,
                notifications=self.__notifications,
            )
            self.push_to_queue(event=phone_container.__dict__)

        # Initialize observers
        for path, services in manager.bluetooth.bluez_root.GetManagedObjects().items():
            interfaces_added(path, services)

        manager.bluetooth.bluez_root.InterfacesAdded.connect(interfaces_added)
        manager.bluetooth.bluez_root.InterfacesRemoved.connect(interfaces_removed)

        ancs.ShowNotification.connect(show_ios_notification)
        ancs.DismissNotification.connect(dismiss_ios_notification)

        loop.run()

    def push_to_queue(self, event: dict, event_type: dict = None):
        """
        Push a new event to the master queue.

        :param event: the dict that will be converted to json & passed to the queue, and in turn
            to the UI.
        :param event_type: the event type that will go on the queue. If no argument is specified,
            it defaults to the calling services type
        """
        if not event_type:
            event_type = self.service_type

        # Convert Notification object to a serializable form
        json_notifs = []
        for item in event["notifications"]:
            json_notifs.append(item.__dict__)

        event["notifications"] = json_notifs

        self.event_queue.push_event(event_type=self.service_type, event=event)

    def main(self):
        if not self.__enabled:
            return

        match self.__type:
            case PhoneTypes.ANDROID:
                self.__android_loop(self.__phone_manager)
            case PhoneTypes.IOS:
                self.__ios__loop(self.__phone_manager)
            case _:
                self.logger.error(
                    msg="Failed to get phone type, exiting phone manager!"
                )

    def refresh(self):
        if not self.__enabled:
            self.push_to_queue(PhoneContainer(enabled=self.__enabled).__dict__)
        else:
            notif_refresh = PhoneContainer(
                enabled=self.__enabled,
                type=self.__type.value,
                state=self.state.value,
                notifications=self.__notifications,
            )
            self.push_to_queue(event=notif_refresh.__dict__)
