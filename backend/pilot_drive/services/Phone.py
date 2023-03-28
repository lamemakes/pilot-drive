from dataclasses import dataclass
import time
from typing import List
from MasterLogger import MasterLogger
from services.Settings import Settings
from .PhoneUtils.phone_constants import (
    PHONE_TYPES,
    PHONE_STATES,
    Notification,
    PhoneContainer,
)
from .PhoneUtils.abstract_manager import AbstractManager

from services import AbstractService
from MasterEventQueue import MasterEventQueue, EventType


class FailedToReadSettingsException(Exception):
    pass


class NoPhoneManagerException(Exception):
    pass


class Phone(AbstractService):
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
        self.__state = PHONE_STATES.DISCONNECTED

        if self.enabled:
            try:
                self.__type = PHONE_TYPES(self.__settings.get_setting("phone")["type"])
            except ValueError:
                raise FailedToReadSettingsException(
                    f'Invalid phone type provided: {self.__settings.get_setting("phone")["type"]}'
                )
            except KeyError:
                raise FailedToReadSettingsException(
                    "Failed to retrieve phone settings!"
                )

            match self.__type:
                case PHONE_TYPES.ANDROID:
                    from .PhoneUtils.android_manager import AndroidManager

                    self.__phone_manager = AndroidManager(logger=self.logger)
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
        """
        phone_settings = self.__settings.get_setting("phone")

        try:
            self.__type = PHONE_TYPES(self.__settings.get_setting("phone")["type"])
        except ValueError:
            self.__enabled = False
            raise FailedToReadSettingsException(
                f'Invalid phone type provided: {self.__settings.get_setting("phone")["type"]}'
            )

        settings_enabled = phone_settings.get("enabled") != None
        self.__enabled = settings_enabled

        return settings_enabled

    @property
    def state(self) -> PHONE_STATES:
        return self.__phone_manager.state

    def notificationsMatch(
        self, notif_list1: List[Notification], notif_list2: List[Notification]
    ):
        if len(notif_list1) != len(notif_list2):
            return False

        for i in range(len(notif_list1)):
            if notif_list1[i] != notif_list2[i]:
                return False
        else:
            return True

    def __android_loop(self, manager: AbstractManager):
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
                if self.__state == PHONE_STATES.DISCONNECTED:
                    phone_container.notifications = []
                phone_container.state = self.__state.value
                push_notifs = True

            if self.state == PHONE_STATES.CONNECTED:
                manager_notifs = manager.notifications
                manager_notifs.sort(key=self.__notification_sort, reverse=True)
                if not self.notificationsMatch(self.__notifications, manager_notifs):
                    self.__notifications = manager_notifs
                    phone_container.notifications = self.__notifications
                    push_notifs = True

            if push_notifs:
                self.push_to_queue(event=phone_container.__dict__)

            time.sleep(1)

    def push_to_queue(self, event: dict, event_type: dict = None):
        """
        Push a new event to the master queue.

        :param event: the dict that will be converted to json & passed to the queue, and in turn to the UI.
        :param event_type: the event type that will go on the queue. If no argument is specified, it defaults to the calling services type
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

        if self.__type == PHONE_TYPES.ANDROID:
            self.__android_loop(self.__phone_manager)
        else:
            self.logger.error(msg="Failed to get phone type, exiting phone manager!")

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
