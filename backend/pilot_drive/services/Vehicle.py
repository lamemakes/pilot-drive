import obd
from services import AbstractService
from MasterEventQueue import MasterEventQueue, EventType


class Vehicle(AbstractService):
    def __init__(self, master_event_queue: MasterEventQueue, service_type: EventType):
        super().__init__(master_event_queue, service_type)

    def __handle_connect(self):
        pass

    def main():
        pass

    def refresh(self):
        pass