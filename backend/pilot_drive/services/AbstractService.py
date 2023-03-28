from abc import ABC, abstractmethod
from MasterEventQueue import MasterEventQueue, EventType
from MasterLogger import MasterLogger
from multiprocessing import Process


class AbstractService(ABC):
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
        :param service_type: the EvenType enum that indicated what the service will appear as on the event queue
        """
        self.event_queue = master_event_queue
        self.service_type = service_type

        self.logger = logger
        self.logger.info(msg=f"Initializing {service_type} service!")

    def push_to_queue(self, event: dict, event_type: dict = None):
        """
        Push a new event to the master queue.

        :param event: the dict that will be converted to json & passed to the queue, and in turn to the UI.
        :param event_type: the event type that will go on the queue. If no argument is specified, it defaults to the calling services type
        """
        if not event_type:
            event_type = self.service_type

        self.event_queue.push_event(event_type=self.service_type, event=event)

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def main(self):
        pass
