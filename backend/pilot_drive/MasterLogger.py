import inspect
from multiprocessing import Manager
from typing import Callable
from pilot_drive.constants import DEFAULT_LOG_SETTINGS, LOG_FILE_NAME, absolute_path
import logging
import os
import time


logging.CRITICAL

class MasterLogger:
    '''
    The class that handles the logger for the entire application, allowing for logging across multiple processes via the queue
    '''
    def __init__(self, log_settings: dict) -> None:
        '''
        Initialize the logger

        :param log_settings: a dict of logger settings, ie. {"logLevel": <0-50>, "logToFile": <bool>, "logPath": <LOG PATH>"}. the :func: `~pilot_drive.services.Settings.get_raw_settings` can be used to supply this
        '''
        manager = Manager()
        self.__logging_queue = manager.Queue()
        self.__new_log = manager.Value("i", 0)
        self.logger: logging.Logger = self.__initialize_logger(log_settings)

    def __initialize_logger(self, log_settings) -> logging.Logger:
        '''
        Initialized the logger and its configurations based on the log_settings dict

        :param log_settings: a dict of logger settings, ie. {"logLevel": <0-50>, "logToFile": <bool>, "logPath": <LOG PATH>"}. the :func: `~pilot_drive.services.Settings.get_raw_settings` can be used to supply this
        :return: an instance of logging.Logger
        '''
        init_errors = (
            []
        )  # Append any errors to a list to be logged after logger initialization

        try:
            log_level = log_settings["logLevel"]
            log_to_file = log_settings["logToFile"]
            if log_to_file == True:
                log_path = log_settings["logPath"]
        except KeyError as err:
            init_errors.append(
                "Failed to retrieve logging value from settings: " + str(err)
            )
            log_level = DEFAULT_LOG_SETTINGS["logLevel"]
            log_to_file = DEFAULT_LOG_SETTINGS["logToFile"]
            if log_to_file == True:
                log_path = log_settings["logPath"]

        if log_to_file == True:
            # checks if the user specified the log path with file specified (ie. /etc/pilot-drive/yeet.log) or just a directory path (ie. /etc/pilot-drive/)
            if log_path == "":
                log_path = DEFAULT_LOG_SETTINGS["logPath"]

            if log_path[-1] == "/":
                log_path = f"{log_path}{LOG_FILE_NAME}"

            dir_path = log_path.split("/")[:-1]
            dir_path = "/".join(dir_path)
            os.makedirs(name=dir_path, exist_ok=True)

        logging.basicConfig(
            filename=log_path,
            format="%(asctime)s:%(levelname)s:%(message)s",
            datefmt="%m/%d/%Y-%H:%M:%S",
            level=log_level,
        )

        # Disable the loggers of unintended services liek websocket & asyncio...
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        logging.getLogger("asyncio.coroutines").setLevel(logging.ERROR)
        logging.getLogger("websockets.server").setLevel(logging.ERROR)
        logging.getLogger("websockets.protocol").setLevel(logging.ERROR)
        logger = logging.getLogger(__name__)
        return logger

    '''
    Logic/APIs for services. Goal was to make it close to the feel of the logging module. Just needs origin.
    '''

    def __add_to_queue(self, level: int, origin: str, msg: str) -> None:
        '''
        Add the logging event to the multiprocessing queue

        :param level: the logging level of the event ie. (0-50)
        :param origin: the origin of the logging event
        :param msg: the logging event
        '''
        log_dict = {"level": level, "origin": origin, "message": msg}
        self.__logging_queue.put(item=log_dict)
        self.__new_log.value = 1  # Indicate there is a new log value in the queue

    def __log_handler(level: int) -> Callable:
        '''
        Handles the incoming logging event and adds it to the queue. Intended to be used as a decorator to error handling methods.

        :param level: the intended log level ie. (0-50)
        '''
        def inner(func):
            def wrapper(self, msg: str):
                # Get the calling origin and format it to look like the typical logger call.
                origin = (
                    inspect.stack()[1]
                    .filename.replace("/main.py", "/__main__")
                    .replace(absolute_path, "")
                    .replace("/", ".")
                    .replace(".py", "")
                )  # Daisy chaining replace statements sucks. TODO: Use RegEx here.
                self.__add_to_queue(level=level, origin=origin, msg=msg)
                return
            
            return wrapper
        
        return inner


    # Attempt to make the logging feel as close to the stock library as possible
    @__log_handler(logging.CRITICAL)
    def critical(self, msg: str) -> None:
        '''
        Log 'msg' with severity 'CRITICAL'.

        :param msg: The message to be logged
        '''
        pass

    @__log_handler(logging.ERROR)
    def error(self, msg: str) -> None:
        '''
        Log 'msg' with severity 'ERROR'.

        :param msg: The message to be logged
        '''
        pass

    @__log_handler(logging.WARNING)
    def warning(self, msg: str) -> None:
        '''
        Log 'msg' with severity 'WARNING'.

        :param msg: The message to be logged
        '''
        pass

    @__log_handler(logging.INFO)
    def info(self, msg: str) -> None:
        '''
        Log 'msg' with severity 'INFO'.

        :param msg: The message to be logged
        '''
        pass

    @__log_handler(logging.DEBUG)
    def debug(self, msg: str) -> None:
        '''
        Log 'msg' with severity 'DEBUG'.

        :param msg: The message to be logged
        '''
        pass

    """
    Logic for actually logging.
    """

    def __log(self, level: int, origin: str, message: str) -> None:
        '''
        Output the log with the :func:`~logging.Logger.log` method

        :param level: the logging level of the event ie. (0-50)
        :param origin: the origin of the logging event
        :param message: the logging event
        '''
        full_message = f"{origin}: {message}"
        self.logger.log(level=level, msg=full_message)

    def main(self) -> None:
        '''
        The main loop for the logger, reads from the queue and when theres is a new logging event, output it
        '''
        while True:
            if not (self.__new_log.value == 0):
                self.__log(**self.__logging_queue.get())

                if self.__logging_queue.empty():
                    self.__new_log.value = 0

            time.sleep(0.1)
