import http.server
import socketserver

from pilot_drive.constants import absolute_path
from pilot_drive.master_logging.MasterLogger import MasterLogger
from pilot_drive.master_queue.MasterEventQueue import MasterEventQueue, EventType


class Web:
    """
    The class that serves the static web assets (the Vue frontend)
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
        port: int,
        relative_directory: str,
    ):
        """
        Constructor for the Web class
        :param port: The port that the server will be ran at (ie. http://localhost:<port>)
        :param relative_directory: The directory that the server will be serving from (containing index.html)
        """
        self.__port = port
        self.__directory = f"{absolute_path}{relative_directory}"
        self.__logger = logger
        self.__logger.info(msg="Initializing the static web server!")

    def __handler(self, request, client_address, server):
        """
        The handler that passes the request params to the SimpleHttpRequestHandler, along with the directory path
        :param request: The socket request object
        :param client_address: The client address object
        :param server: The socketserver.TCPServer object
        """
        http.server.SimpleHTTPRequestHandler(
            request=request,
            client_address=client_address,
            server=server,
            directory=self.__directory,
        )

    def main(self):
        """
        starts the server, serving static assets
        """
        try:
            with socketserver.TCPServer(("", self.__port), self.__handler) as httpd:
                httpd.serve_forever()
        except Exception as err:
            self.__logger.error(msg=f"Error while serve static web files: {err}")
