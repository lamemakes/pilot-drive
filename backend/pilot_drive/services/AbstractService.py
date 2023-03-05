from abc import ABC, abstractmethod
from MasterEventQueue import MasterEventQueue, EventType
from multiprocessing import Process

class AbstractService(ABC):
    @abstractmethod
    def __init__(self, master_event_queue: MasterEventQueue, service_type: EventType):
        '''
        Initialize the service

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on the event queue
        '''
        self.event_queue = master_event_queue
        self.service_type = service_type.value
        

    def push_to_queue(self, event_json: str):
        '''
        Push a new event to the master queue.

        :param event_json: the JSON string that will be passed to the queue, and in turn to the UI.
        '''
        self.event_queue.push_event(event_type=self.service_type, event_json=event_json)

    
    @abstractmethod
    def main():
        pass