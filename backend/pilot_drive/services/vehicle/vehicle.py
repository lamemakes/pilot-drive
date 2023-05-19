"""
The module that manages the connected vehicle
"""
import os
import time
import obd

from pilot_drive.constants import QUERIED_FIELDS
from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue.master_event_queue import MasterEventQueue, EventType

from ..abstract_service import AbstractService


class InvalidPortException(Exception):
    """
    Exception raised when an invalid connection is detected, either from an invalid port string, or
    a Python OBD connection failure.
    """


class InvalidQueryException(Exception):
    """
    Exception raised when an query field is detected as specified in the QUERIED_FIELDS
    constants.py.
    """


class Vehicle(AbstractService):
    """
    The vehicle service that interfaces with the connected vehicle
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
        obd_port: str = None,
    ):
        """
        Initialize the Vehicle service

        :param event: the dict that will be converted to json & passed to the queue, and in turn
        to the UI.
        :param event_type: the event type that will go on the queue. If no argument is specified,
        it defaults to the calling services type
        :param obd_port: the port to attempt a connection to an OBD port. If unspecified, python
        OBD will attempt to detect a connection.
        """
        super().__init__(master_event_queue, service_type, logger)

        self.__connected = False
        self.__failed = False
        self.__connection = None
        self.__max_interval = 0

        self.__obd_port = obd_port

        self.stats = []

    def __is_connected(self):
        """
        Check if the OBD adapter is connected via python-OBD's status() method.

        :returns: a boolean of True if connected, False if not.
        """
        if self.__connection and self.__connection.status() in [
            obd.OBDStatus.ELM_CONNECTED,
            obd.OBDStatus.OBD_CONNECTED,
            obd.OBDStatus.CAR_CONNECTED,
        ]:
            self.__connected = True
            return True

        self.__connected = False
        return False

    def __handle_connect(self):
        """
        Initialize the connection to the OBD serial port.
        """
        if self.__obd_port:
            if os.path.exists(self.__obd_port):
                connection = obd.OBD(self.__obd_port)
                self.__failed = False
                if connection != self.__connection:
                    self.__push_info()
                self.__connection = connection
                self.logger.info(f"OBD connection made to {self.__obd_port}.")
            else:
                if not self.__failed:
                    self.__push_info()
                    self.__failed = True

                raise InvalidPortException(
                    f'Specified path: "{self.__obd_port}" does not exist!'
                )
        else:
            self.__connection = obd.OBD()

        self.__push_info()

    def __push_info(self):
        """
        Push the current vehicle data to the frontend
        """
        vehicle_info = {"connected": self.__connected,
                        "failures": self.__failed, "stats": self.stats}
        self.push_to_queue(vehicle_info)

    def __query_fields(self, queries_made: int):
        """
        Query the fields that are input.
        Expects a list of dicts in the form of:
        {"name": "<name>", "command": "<python OBD command>", "interval": <int query interval>}

        In
        """
        if self.__connection and len(QUERIED_FIELDS) > 0:
            field_index = 0
            for field in QUERIED_FIELDS:
                field_name = field["name"]
                field_command = field["command"]
                field_interval = field["interval"]
                if not obd.commands.has_name(field_command):
                    raise InvalidQueryException(
                        f'OBD command: "{field_name}" is not valid!'
                    )

                # If the the current field's interval is greater than the global max, up the max
                if not self.__max_interval and field_interval > self.__max_interval:
                    self.__max_interval = field_interval

                if queries_made % field_interval == 0:
                    # Make the query
                    resp = self.__connection.query(obd.commands[field_command])
                    if resp.value:
                        # Convert to a tuple to get units & magnitude
                        resp_tuple = resp.value.to_tuple()
                        # pint converts tuples a little odd,
                        # values come back as"(<quantity>, (('<unit>', <magnitude>),))"
                        value = {
                            "quantity": resp_tuple[0],
                            "units": resp_tuple[1][0][0],
                            "magnitude": resp_tuple[1][0][1],
                        }
                        if len(self.stats) == field_index:
                            self.stats.append(
                                {"name": field_name, "value": value})
                        else:
                            self.stats[field_index] = {
                                "name": field_name,
                                "value": value,
                            }

                        field_index += 1
                    else:
                        self.logger.error(
                            msg=f'Failed to query for "{field_name}"')
                        continue

            if self.stats:
                self.__push_info()

    def main(self):
        queries_made = 0
        connection_error_logged = False
        while True:
            if not self.__is_connected():
                try:
                    self.__handle_connect()
                except InvalidPortException as err:
                    if not connection_error_logged:  # Don't spam the log
                        self.logger.error(
                            msg=f"""Invalid serial port specified: "{err}",
                             will continue to attempt a connection."""
                        )
                        connection_error_logged = True
                    time.sleep(
                        0.5
                    )  # Busy wait then continue to try and connect in case it happens to show up

            if self.__is_connected():
                self.__query_fields(queries_made=queries_made)
                time.sleep(0.5)
                queries_made = (
                    0 if queries_made == self.__max_interval else queries_made + 0.5
                )

    def refresh(self):
        self.__push_info()
