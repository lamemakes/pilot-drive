"""
Module contains an abstract service used as a template for other service implementations
"""

from abc import ABC, abstractmethod
from pilot_drive.master_queue import MasterEventQueue, EventType
from pilot_drive.master_logging import MasterLogger


class AbstractService(ABC):
    """
    The abstract class used to implement all other services
    """

    @abstractmethod
    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
    ):
        """
        Initialize the service

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on
        the event queue
        """
        self.event_queue = master_event_queue
        self.service_type = service_type

        self.logger = logger
        self.logger.info(msg=f"Initializing {service_type} service!")

    def push_to_queue(self, event: dict, event_type: dict = None) -> None:
        """
        Push a new event to the master queue.

        :param event: the dict that will be converted to json & passed to the queue, and in turn to
        the UI.
        :param event_type: the event type that will go on the queue. If no argument is specified,
        it defaults to the calling services type
        """
        if not event_type:
            event_type = self.service_type

        self.event_queue.push_event(event_type=self.service_type, event=event)

    @abstractmethod
    def refresh(self) -> None:
        """
        Add any stored events back to the event queue, as this will be called in a client refresh.
        """

    @abstractmethod
    def main(self) -> None:
        """
        runs servce main loop and logic
        """

    @abstractmethod
    def terminate(self) -> None:
        """
        Attempts to clean up the service's resources
        """
