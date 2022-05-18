import os
import json
import logging

log = logging.getLogger()

# LUT for the logging config option.
LOGGING_LUT = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL}


config_file = "config.json"

def generate_config():
    log.info("Attemping to create config file at: " + config_file)
    with open(config_file, "w") as cfg:
        # Populate the config with a skeleton of the config
        config_contents = {"pilot-drive" : {
                                    "obd" : {"enabled" : True, "port" : ""},
                                    "logging" : {"logLevel" : "INFO", "logToFile" : False, "logPath" : ""},
                                    "camera" : {"enabled" : False, "buttonPin" : 16}
                                    }}
        
        cfg.writelines(json.dumps(config_contents, indent=2))

def read_config():
    log.info("Attempting to read config file: " + config_file)
    with open(config_file, "r") as cfg:
        pilot_cfg = json.loads(cfg.read())
    
    return pilot_cfg

def write_config(pilot_cfg):
    log.info("Attempting to write to config file: " + config_file)
    full_config = {"pilot-drive" : pilot_cfg}
    with open(config_file, "w") as cfg:
        cfg.write(json.dumps(full_config, indent=2))

if not os.path.isfile(config_file):
    generate_config()

# Open the JSON config file and read it
try:
    pilot_cfg = read_config()["pilot-drive"]
except KeyError:
    log.error("Invalid configuration file! \"pilot-drive\" key not found!")
    exit()


# Get the logging object associated with the provided string and set it.
if pilot_cfg.get("logging").get("logLevel") in LOGGING_LUT:
    pilot_cfg["logging"]["logLevel"] = LOGGING_LUT.get(pilot_cfg.get("logging").get("logLevel"))
    log.info("Logging level set to: " + str(pilot_cfg.get("logging").get("logLevel")))
else:
    log.info("No valid log level found in \"" + config_file + "\", defaulting to INFO.")
    pilot_cfg["logging"]["logLevel"] = LOGGING_LUT.get("INFO")

if __name__ == "__main__":
    print(pilot_cfg)
