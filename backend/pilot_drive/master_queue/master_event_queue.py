"""
Module used to track and display  
"""

import json
from enum import StrEnum
from multiprocessing import Manager

from pilot_drive.master_logging.master_logger import MasterLogger


class EventType(StrEnum):
    """
    Enum used by services to add an event to the master queue
    """

    BLUETOOTH = "bluetooth"
    SETTINGS = "settings"
    PHONE = "phone"
    SYSTEM = "system"
    VEHICLE = "vehicle"
    MEDIA = "media"
    WEB = "web"


class MasterEventQueue:
    """
    The class that manages the master event queue. Services are passed the created MasterEventQueue
        object from the main loop, and use the push_event() method to add events to the queue. The
        main loop will use the is_new_event() and pop_event() methods to handle new events.
    """

    def __init__(self, logging: MasterLogger):
        manager = Manager()
        self.__queue = manager.Queue()
        self.__new_event = manager.Value("i", 0)
        self.__logging = logging

    def push_event(self, event_type: EventType, event: str):
        """
        Used to push a new event to the Master Event Queue

        :param event_type: the event source, utilizing the EventType enum
        :param event: the dict of the event to be converted to JSON
        """

        event = {"type": event_type, event_type: event}

        self.__logging.debug(msg=f"New Event: {json.dumps(event)}")

        self.__queue.put(event)
        self.__new_event.value = 1

    def get(self):
        """
        Remove and return an item from the queue

        :returns: event dict object of {"type": <type>, <type>: <event_json>}, or None if the queue
            is empty.
        """

        if self.__queue.empty():
            return None

        queue_return = self.__queue.get()

        if self.__queue.empty():
            self.__new_event.value = 0

        return queue_return

    def is_new_event(self):
        """
        Check if there is a new event on the event queue

        :returns: boolean if there is a new event or not
        """

        return not self.__new_event.value == 0
