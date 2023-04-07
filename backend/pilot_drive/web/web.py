"""
Module contains the static web file server
"""

import http.server
import socketserver

from pilot_drive.constants import absolute_path
from pilot_drive.master_logging.master_logger import MasterLogger


class Web:
    """
    The class that serves the static web assets (the Vue frontend)
    """

    def __init__(self, logger: MasterLogger, port: int, relative_directory: str):
        """
        Constructor for the Web class
        :param port: The port that the server will be ran at (ie. http://localhost:<port>)
        :param relative_directory: The directory that the server will be serving from
        """
        self.__port = port
        self.__directory = f"{absolute_path}{relative_directory}"
        self.__logger = logger
        self.__logger.info(msg="Initializing the static web server!")

    def handler(self, request, client_address, server) -> None:
        """
        The handler that passes the request params to the SimpleHttpRequestHandler,
        along with the directory path

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

    def main(self) -> None:
        """
        starts the server, serving static assets
        """
        with socketserver.TCPServer(("", self.__port), self.handler) as httpd:
            httpd.serve_forever()
