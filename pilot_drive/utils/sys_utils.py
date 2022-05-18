# General utilities

import socket
import os
import sys
import psutil

# Get the CPU usage percentage
def get_cpu_state():
    return str(psutil.cpu_percent())

def get_hostname():
    return os.uname()[1]

def get_network_connection():
    try:
        # If the connection attempt doesn't error out, everything should be alright
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        # No connection
        return False

def restart_pilot():
    # Restarts PILOT when called
    os.execl(sys.executable, sys.executable, * sys.argv)

