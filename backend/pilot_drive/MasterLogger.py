import inspect
from multiprocessing import Manager
from constants import DEFAULT_LOG_SETTINGS, LOG_FILE_NAME
import logging
import os
import time


class MasterLogger:
    def __init__(self, log_settings: dict) -> None:
        manager = Manager()
        self.__logging_queue = manager.Queue()
        self.__new_log = manager.Value("i", 0)
        self.logger: logging.Logger = self.__initialize_logger(log_settings)
        self.__current_dir = f"{os.getcwd()}/"

    def __initialize_logger(self, log_settings) -> logging.Logger:
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

    """
    Logic/APIs for services. Goal was to make it close to the feel of the logging module. Just needs origin.
    """

    def __add_to_queue(self, level: int, origin: str, message: str) -> None:
        log_dict = {"level": level, "origin": origin, "message": message}
        self.__logging_queue.put(item=log_dict)
        self.__new_log.value = 1  # Indicate there is a new log value in the queue

    def __log_handler(level: int):
        def inner(func):
            def wrapper(self, msg: str):
                # Get the calling origin and format it to look like the typical logger call.
                origin = (
                    inspect.stack()[1]
                    .filename.replace("/main.py", "/__main__")
                    .replace(self.__current_dir, "")
                    .replace("/", ".")
                    .replace(".py", "")
                )  # Daisy chaining replace statements sucks. TODO: Use RegEx here.
                self.__add_to_queue(level=level, origin=origin, message=msg)
                return

            return wrapper

        return inner

    # Attempt to make the logging feel as close to the stock library as possible
    @__log_handler(logging.CRITICAL)
    def critical(self, msg: str) -> None:
        pass

    @__log_handler(logging.ERROR)
    def error(self, msg: str) -> None:
        pass

    @__log_handler(logging.WARNING)
    def warning(self, msg: str) -> None:
        pass

    @__log_handler(logging.INFO)
    def info(self, msg: str) -> None:
        pass

    @__log_handler(logging.DEBUG)
    def debug(self, msg: str) -> None:
        pass

    """
    Logic for actually logging.
    """

    def __log(self, level: int, origin: str, message: str):
        full_message = f"{origin}: {message}"
        self.logger.log(level=level, msg=full_message)

    def main(self) -> None:
        while True:
            if not (self.__new_log.value == 0):
                self.__log(**self.__logging_queue.get())

                if self.__logging_queue.empty():
                    self.__new_log.value = 0

            time.sleep(0.1)
