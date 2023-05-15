"""
The main PILOT Drive module that contains the class that starts the services and runs the 
websockets logic.
"""

import json
from multiprocessing import Process
from typing import Generic, List, Tuple, TypeVar
import asyncio
import websockets

from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue import MasterEventQueue, EventType
from pilot_drive.web import Web
from pilot_drive.services import (
    Settings,
    Bluetooth,
    Vehicle,
    Phone,
    AbstractService,
    Camera,
    Media,
)
from pilot_drive.services.settings.exceptions import FailedToReadSettingsException

from . import constants


class FailedToCreateServiceException(Exception):
    """
    Exception that occurs when a service could not be created
    """


class PilotDrive:
    """
    The main class of PILOT Drive. Creates services (distributes logging & events queues), handles
    asyncio websockets, and attempts to properly exit services.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        """
        Initialize the logger, all specified services and their handlers.
        """

        # Logging initialization
        try:
            log_settings = Settings.get_raw_settings()["logging"]
        except FailedToReadSettingsException:
            log_settings = constants.DEFAULT_LOG_SETTINGS

        self.logging = MasterLogger(log_settings=log_settings)
        self.logger_proc = Process(target=self.logging.main, daemon=True)
        self.logger_proc.start()

        # Queue initialization
        self.master_queue = MasterEventQueue(logging=self.logging)

        # Sevice initialization
        self.__services: List[Tuple[AbstractService, Process]] = []

        self.web = Web(
            logger=self.logging,
            port=constants.STATIC_WEB_PORT,
            relative_directory=constants.STATIC_WEB_PATH,
        )
        web_process = Process(target=self.web.main, daemon=True)
        web_process.start()

        self.settings: Settings = self.service_factory(service=Settings)
        self.bluetooth: Bluetooth = self.service_factory(service=Bluetooth)
        self.media: Media = self.service_factory(service=Media)

        if self.settings.get_setting("phone")["enabled"]:
            self.phone: Phone = self.service_factory(
                service=Phone, settings=self.settings
            )

        if self.settings.get_setting("vehicle")["enabled"]:
            obd_port = self.settings.get_setting("vehicle")["port"]
            self.vehicle: Vehicle = self.service_factory(
                service=Vehicle, obd_port=obd_port
            )

        if self.settings.get_setting("camera")["enabled"]:
            btn_pin = self.settings.get_setting("camera")["buttonPin"]
            self.camera: Camera = self.service_factory(service=Camera, btn_pin=btn_pin)

        # Set message handlers for your services, ie. if there is a new "settings" type recieved
        # from the websocket, pass it to settings.set_web_settings as it is a settings change event.
        self.service_msg_handlers = {
            EventType.SETTINGS: self.settings.set_web_settings,
            EventType.MEDIA: self.media.track_control,
        }

    T = TypeVar("T", bound=AbstractService)

    # pylint: disable=anomalous-backslash-in-string
    def service_factory(self, service: Generic[T], **kwargs) -> AbstractService:
        """
        Creates a new service, and automatically passes master queue, event type, and logger. Takes
            arguments of the service class, followed by all of the specified service's keyword
            arguments.

        :param service: a service class that has a base of AbstractService
        :param \**kwargs: extra keyword arguments to be passed to the given service
        :return: an instance of the service class
        :raises: FailedToCreateServiceException: if service isn't in the EventType enum
        :raises: FailedToCreateServiceException: if the service creation returns a TypeError,
            possibly if the keyword arguments are wrong
        """
        # pylint: enable=anomalous-backslash-in-string
        try:
            event_type = EventType(service.__name__.lower())
            new_service = service(
                master_event_queue=self.master_queue,
                service_type=event_type,
                logger=self.logging,
                **kwargs,
            )

            service_process = Process(target=new_service.main, daemon=True)
            service_process.start()

            self.__services.append((new_service, service_process))

            return new_service

        except ValueError as exc:
            raise FailedToCreateServiceException(
                f'Invalid service: "{service.__name__}" not found in EventType Enum!'
            ) from exc
        except TypeError as exc:
            raise FailedToCreateServiceException(
                f"""Failed to create service: "{service.__name__}",
                are the accessory arguments correct?"""
            ) from exc

    def refresh(self) -> None:
        """
        Called when the webpage refreshes or reconnects to the WebSocket - used to recall data
            like settings
        """
        self.settings.refresh()
        self.bluetooth.refresh()

    def handle_message(self, message: str) -> None:
        """
        The handler for when a new WebSocket event recieved from the UI client

        :params message: the event in from the UI, recieved as a JSON string to be converted to a
            dict
        """
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
                        msg=f"""Failed to find a service handler for message of type:
                        {message_in["type"]}"""
                    )
            except json.JSONDecodeError as err:
                self.logging.error(
                    msg=f"Failed to decode recieved websocket message: {err.msg} {message_in}"
                )

    async def consumer(self, websocket) -> None:
        """
        The consumer to be used when new WebSocket messages come in from the UI

        :param websocket: the WebSocket the UI is connected to
        """
        while True:
            try:
                message = await websocket.recv()
                self.handle_message(message=message)
            except websockets.exceptions.ConnectionClosedOK:
                break

    async def producer(self, websocket) -> None:
        """
        The producer used when new events need to be pushed to the UI via WebSocket

        :param websocket: the WebSocket the UI is connected to
        """
        self.refresh()  # When the app is started/UI is refreshed, send a settings event on the bus
        while True:
            try:
                if self.master_queue.is_new_event:
                    event = self.master_queue.get()
                    await websocket.send(json.dumps(event))
                await asyncio.sleep(0.05)
            except websockets.exceptions.ConnectionClosedOK:
                break

    async def handler(self, websocket) -> None:
        """
        The handler used for the WebSocket connection, creates consumer and producer tasks

        :param websocket: the WebSocket the UI is connected to
        """
        await asyncio.gather(
            self.consumer(websocket=websocket), self.producer(websocket=websocket)
        )

    async def main(self) -> None:
        """
        The main method to be run, handles the WebSocket connection to the UI
        """
        try:
            self.logging.info(msg="Initializing PILOT Drive main loop!")
            # pylint: disable=no-member
            async with websockets.serve(self.handler, "", constants.WS_PORT):
                self.logging.info(msg="Starting WebSocket server!")
                await asyncio.Future()  # run forever
        except asyncio.CancelledError:
            self.logging.info(
                msg="SIGINT/SIGTERM recieved, terminating websocket server!"
            )

    def terminate(self, signum, frame):
        """
        Cleanly terminates each process and calls it's cleanup method
        """
        self.logging.info(
            msg=f'Recieved signal: "{signum}" with frame "{frame}", terminating!'
        )

        for service in self.__services:
            service_obj, process = service
            self.logging.debug(msg=f"Terminating: {service_obj} process")
            process.terminate()
            process.join()

        self.logger_proc.terminate()
        self.logger_proc.join()
