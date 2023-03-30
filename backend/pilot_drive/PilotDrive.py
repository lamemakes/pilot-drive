import json
from multiprocessing import Process
import signal
from typing import List, Tuple
import asyncio
import websockets

from pilot_drive import constants
from pilot_drive.MasterLogger import MasterLogger
from pilot_drive.MasterEventQueue import MasterEventQueue, EventType
from pilot_drive.web import Web
from pilot_drive.services import Settings, Bluetooth, Vehicle, Phone, ServiceExceptions, AbstractService

class FailedToCreateServiceException(Exception):
    pass

class PilotDrive:
    def __init__(self):
        # Logging initialization
        try:
            log_settings = Settings.get_raw_settings()["logging"]
        except ServiceExceptions.FailedToReadSettingsException:
            log_settings = constants.DEFAULT_LOG_SETTINGS

        self.logging = MasterLogger(log_settings=log_settings)
        self.logger_proc = Process(target=self.logging.main)
        self.logger_proc.start()

        # Queue initialization
        self.master_queue = MasterEventQueue(logging=self.logging)

        # Sevice initialization
        self.__services: List[Tuple[AbstractService, Process]] = []

        self.settings: Settings = self.service_factory(service=Settings)
        self.web:Web = self.service_factory(service=Web, port=constants.STATIC_WEB_PORT, relative_directory=constants.STATIC_WEB_PATH)
        self.bluetooth: Bluetooth = self.service_factory(service=Bluetooth)
        self.phone: Phone = self.service_factory(service=Phone, settings=self.settings)
        if self.settings.get_setting('vehicle')['enabled']:
            self.vehicle = self.service_factory(service=Vehicle, obd_port='')

        # Set message handlers for your services, ie. if there is a new "settings" type recieved from the websocket, pass it to
        # settings.set_web_settings as it is a settings change event.
        self.service_msg_handlers = {
            EventType.SETTINGS.value: self.settings.set_web_settings,
            EventType.BLUETOOTH.value: self.bluetooth.bluetooth_control,
        }

    def service_factory(self, service: AbstractService, **kwargs):
        try:
            event_type = EventType(service.__name__.lower())
            new_service = service(master_event_queue=self.master_queue, service_type=event_type, logger=self.logging, **kwargs)
            
            p = Process(target=new_service.main)
            p.start()

            self.__services.append((new_service, p))

            return new_service

        except ValueError:
            raise FailedToCreateServiceException(f'Invalid service: "{service.__name__}" not found in EventType Enum!')
        except TypeError:
            raise FailedToCreateServiceException(f'Failed to create service: "{service.__name__}", are the accessory arguments correct?')


    def refresh(self):
        self.settings.refresh()
        self.bluetooth.refresh()
        self.phone.refresh()

    def handle_message(self, message: str):
        if message:
            try:
                message_in = json.loads(s=message)
                try:
                    handler = self.service_msg_handlers.get(
                        message_in["type"]
                    )  # Get the handler for the message type
                    handler(
                        message_in.get(message_in["type"])
                    )  # Pass in the content of the websocket message
                except KeyError:
                    self.logging.error(
                        msg=f'Failed to find a service handler for message of type: {message_in["type"]}'
                    )
            except json.JSONDecodeError as err:
                self.logging.error(
                    msg=f"Failed to decode recieved websocket message: {err.msg} {message_in}"
                )  # TODO: Replace with logging!

    async def consumer(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                self.handle_message(message=message)
            except websockets.ConnectionClosedOK:
                break

    async def producer(self, websocket):
        self.refresh()  # When the app is initialized/the UI is refreshed, it expects a settings even on the bus.
        while True:
            try:
                if self.master_queue.is_new_event():
                    event = self.master_queue.get()
                    await websocket.send(json.dumps(event))
                await asyncio.sleep(0.05)
            except websockets.ConnectionClosedOK:
                break

    async def handler(self, websocket):
        self.settings.refresh()  # When the app is initialized/the UI is refreshed, it expects a settings even on the bus.
        await asyncio.gather(
            self.consumer(websocket=websocket), self.producer(websocket=websocket)
        )

    async def main(self):
        try:
            self.logging.info(msg="Initializing PILOT Drive main loop!")
            async with websockets.serve(self.handler, "", constants.WS_PORT):
                self.logging.info(msg="Starting WebSocket server!")
                await asyncio.Future()  # run forever
        except asyncio.CancelledError:
            self.logging.info(f'SIGINT/SIGTERM recieved, terminating websocket server!')

    def terminate(self, signum, frame):
        for service in self.__services:
            service_obj, process = service
            process.terminate()
        
        self.logger_proc.terminate()