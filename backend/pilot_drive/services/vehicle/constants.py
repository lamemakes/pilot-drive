"""
Constants for the vehicle service
"""

# Validator for ODB/ELM reader serial port path
PORT_PATH_VALIDATOR = r"^\/(.+)\/([^\/]+)$"

# Fields that are queried and pushed to the frontend.
# In the format of:
# {"name": "<name>", "command": "<python OBD command>", "interval": <int second query interval>}

# command fields pulled from python-OBD docs:
# https://python-obd.readthedocs.io/en/latest/Command%20Tables/
QUERIED_FIELDS = (
    {"name": "Speed", "command": "SPEED", "interval": 0.5},
    {"name": "RPM", "command": "RPM", "interval": 0.5},
    {"name": "Fuel Level", "command": "FUEL_LEVEL", "interval": 10},
    {"name": "Voltage", "command": "CONTROL_MODULE_VOLTAGE", "interval": 3},
    {"name": "Short Fuel Trim", "command": "SHORT_FUEL_TRIM_1", "interval": 1},
    {"name": "Long Fuel Trim", "command": "LONG_FUEL_TRIM_1", "interval": 3}
)
