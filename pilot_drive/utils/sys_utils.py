# General utilities

import os
import psutil

# Get the CPU usage percentage
def get_cpu_state():
    return str(psutil.cpu_percent())

def get_hostname():
    return os.uname()[1]