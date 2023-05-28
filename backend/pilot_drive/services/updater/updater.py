"""
Module doing the managing of the PILOT Drive settings
"""
import json
import re
import sys
import os
import subprocess
from typing import List, Tuple
import requests

from pilot_drive import __version__ as pd_version
from pilot_drive.master_logging.master_logger import MasterLogger
from pilot_drive.master_queue import MasterEventQueue, EventType

from .constants import UpdateCommands, PipRegex, UPDATE_RECORD_PATH
from ..abstract_service import AbstractService
from ..settings import Settings


class JsonPullFailedException(Exception):
    """
    Exception raised when a PYPI JSON pull fails
    """


class Updater(AbstractService):
    """
    The service that manages the settings of PILOT Drive, both web and overarching app wise.
    """

    def __init__(
        self,
        master_event_queue: MasterEventQueue,
        service_type: EventType,
        logger: MasterLogger,
        settings: Settings,
    ):
        """
        Initialize the settings service, and create a new settings file/load in a current one.

        :param master_event_queue: the master event queue (message bus) that handles new events
        :param service_type: the EvenType enum that indicated what the service will appear as on
            the event queue
        """
        super().__init__(master_event_queue, service_type, logger)

        self.__update_settings = settings.get_setting("updates")
        self.__pilot_url = self.__update_settings["projectUrl"]
        self.current_version = pd_version

    def handler(self, command):
        """
        Method used to handle incoming update commands

        :param command: the incoming comand to be handled
        """
        match command:
            case UpdateCommands.UPDATE:
                latest_version = self.__get_latest_version()[0]
                self.update_pilot(latest_version)
            case UpdateCommands.CHECK:
                self.__check_for_updates()
            case _:
                self.logger.warning(
                    f'Unrecognized UpdateCommand from UI: "{command}"')

    def get_json(self) -> dict:
        """
        Pull the PyPi JSON info on PILOT Drive

        :raises: requests.exceptions.HTTPError if an invalid HTTP status is presented
        :raises: requests.exceptions.ConnectionError if a network error occurs
        :raises: requests.exceptions.Timeout if the request times out
        """
        self.logger.debug(
            f'Attempting to pull PILOT Drive JSON from "{self.__pilot_url}"...'
        )
        json_req = requests.get(self.__pilot_url, timeout=2000)
        json_req.raise_for_status()

        json_dict = json.loads(json_req.text)
        return json_dict

    def __sort_semver(self, semver: str) -> List[int]:
        """
        Creates a list of ints based on the semver input ie. "1.4.0" -> [1, 4, 0]

        :param semver: the semantic version to be converted to a list
        """
        return [int(y) for y in semver.split(".")]

    def __get_latest_version(self) -> Tuple[str, List]:
        """
        Pulls the latest version & release info from PyPi

        :return: A tuple of (<lastest version>, <latest release info>)
        """
        releases: dict = self.get_json()["releases"]
        versions = list(releases.keys())
        versions.sort(key=self.__sort_semver)
        return versions[-1], releases[versions[-1]]

    def __check_for_updates(self) -> None:
        """
        Check for an available update of PILOT Drive
        """
        try:
            latest_version, _ = self.__get_latest_version()
        except KeyError:
            self.logger.warning("Attempt to get PILOT Drive releases failed!")
            self.push_to_queue(event={"error": "pulling releases failed"})
            return
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as exc:
            self.logger.warning(
                (
                    "Attempt to get PILOT Drive releases failed due to network"
                    f"issues: {exc}"
                )
            )
            self.push_to_queue(
                event={"error": "network error getting update info"})
            return
        except json.JSONDecodeError as exc:
            self.logger.warning(
                (
                    "Attempt to get PILOT Drive releases failed due to a JSON decode "
                    f"error: {exc}"
                )
            )
            self.push_to_queue(event={"error": "error reading release page"})
            return

        if latest_version != self.current_version:
            version_compare = [latest_version, self.current_version]
            version_compare.sort(key=self.__sort_semver)
            if version_compare[-1] == self.current_version:
                self.push_to_queue(
                    event={
                        "error": (
                            f'current version "{self.current_version}" is larger than '
                            f'remote version "{latest_version}"'
                        )
                    }
                )
                return
            self.push_to_queue(
                event={"update": {"version": latest_version, "completed": False}}
            )
        else:
            self.push_to_queue(
                event={
                    "error": f'current version "{self.current_version}" is the latest'
                }
            )

    def update_pilot(self, version: str):
        """
        Update PILOT Drive to a specific version

        :param version: the version to upgrade to
        """
        self.logger.info(f'Attempting to update PILOT Drive to "{version}"...')

        index_url = self.__update_settings["indexUrl"]
        update = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--index-url",
                index_url,
                f"pilot-drive=={version}",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        print()
        print("STDOUT:")
        print(update.stdout)
        print("STDERR:")
        print(update.stderr)
        print()
        if update.stderr:
            if re.search(PipRegex.PIP_UPDATE_REGEX, update.stderr):
                # Just pip saying an update is available, can safely be ignored.
                pass
            elif re.search(PipRegex.NETWORK_ERROR_REGEX, update.stderr):
                self.logger.error(
                    (
                        "Failed to update PILOT Drive due to a network error:"
                        f"{update.stderr}"
                    )
                )
                self.push_to_queue(
                    event={
                        "error": "a network error occured trying to update PILOT Drive"
                    }
                )
                return
            elif re.search(PipRegex.PACKAGE_ERROR_REGEX, update.stderr):
                self.logger.error(
                    (
                        "Failed to update PILOT Drive due to a pip error: "
                        f"{update.stderr}"
                    )
                )
                return

        self.logger.info(
            f'Attempting to restart PILOT Drive after "{version}" install...'
        )

        # Create a record of the update to notify the user that the update was preformed.
        with open(UPDATE_RECORD_PATH, "w", encoding="utf-8") as pd_update_record:
            json.dump(
                obj={"oldVersion": self.current_version, "newVersion": version},
                fp=pd_update_record,
            )

        os.execl(sys.executable, sys.executable, *sys.argv)

    def main(self) -> None:
        """
        The main updater method, checks if an update was previous preformed,
            pushes an event if so, then returns
        """

        if os.path.exists(UPDATE_RECORD_PATH):
            update_record = {}
            with open(UPDATE_RECORD_PATH, "r", encoding="utf-8") as pd_update_record:
                try:
                    update_record = json.load(fp=pd_update_record)
                except json.JSONDecodeError:
                    self.logger.error(
                        "Failed to decode the update record JSON!")
            if not update_record:
                self.logger.error("Failed to read the update record!")
                return

            if update_record["newVersion"] == self.current_version:
                self.push_to_queue(
                    event={
                        "update": {
                            "version": update_record["newVersion"],
                            "completed": True,
                        }
                    }
                )
            else:
                rec_ver = update_record["newVersion"]
                self.logger.warning(
                    f"Update record found, but current version ({self.current_version}) is not "
                    f"the same as the record ({rec_ver}) - possible failed update?"
                )
            os.remove(UPDATE_RECORD_PATH)

    def refresh(self) -> None:
        self.main()
