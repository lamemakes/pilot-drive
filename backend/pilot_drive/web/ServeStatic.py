import http.server
import socketserver
from multiprocessing import Process


class ServeStatic:
    """
    The class that serves the static web assets (the Vue frontend)
    """

    def __init__(self, port: int, relative_directory: str):
        """
        Constructor for the ServeStatic class

        :param port: The port that the server will be ran at (ie. http://localhost:<port>)
        :param relative_directory: The directory that the server will be serving from (containing index.html)
        """
        self.port = port
        self.directory = relative_directory

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
            directory=self.directory,
        )

    def main(self):
        """
        starts the server, serving static assets
        """
        with socketserver.TCPServer(("", self.port), self.__handler) as httpd:
            print("serving! port:", self.port)  # WA DEBUG
            httpd.serve_forever()
