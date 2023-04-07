"""
The module that handles the phone connectivity to PILOT Drive
"""
import time
from typing import List

from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.services.settings import Settings
from pilot_drive.master_queue.master_event_queue import MasterEventQueue, EventType

from .abstract_service import AbstractService
from .phone_utils.android_manager import AndroidManager
from .phone_utils.phone_constants import (
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
                # case PhoneTypes.IOS:
                #     self.__phone_manager = IOSManager(logger=self.logger)
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

        settings_enabled = phone_settings.get("enabled") is None
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

    def terminate(self):
        self.logger.info(
            msg=f"Stop signal recieved, terminating service: {self.service_type}"
        )
