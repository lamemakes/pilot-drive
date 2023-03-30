import subprocess
import itertools
import re
import json
import os
import typing

from pilot_drive.MasterLogger import MasterLogger
from .abstract_manager import AbstractManager
from .phone_constants import (
    SETTINGS_PATH,
    ADB_PACKAGE_NAMES,
    ADB_COMMANDS,
    ADB_NOTIFICATION_ATTRIBUTES,
    ADB_STATE,
    PHONE_STATES,
    Notification,
)


class AdbDependenciesMissingException(Exception):
    def __init__(self, missing_dep: str, return_str: str) -> None:
        message = (
            "Missing dependency: "
            + missing_dep
            + ", bash output returned: "
            + return_str
        )
        super().__init__(message)


class AdbCommandFailedException(Exception):
    pass


class AdbFailedToFindPackageException(Exception):
    pass


class AdbFailedToGetDeviceNameException(Exception):
    pass


class AndroidManager(AbstractManager):
    def __init__(self, logger: MasterLogger) -> None:
        self.logger = logger
        self.__validate_dependencies()  # Confirm all dependencies are there

        try:
            with open(SETTINGS_PATH + ADB_PACKAGE_NAMES, "r") as package_file:
                self.__saved_package_names = json.load(fp=package_file)
        except FileNotFoundError:
            self.logger.error(msg="Package names file does not exist.")
            self.__saved_package_names = {}
        except json.JSONDecodeError:
            self.logger.error(msg="Failed to decode ADB package names path!")
            self.__saved_package_names = {}

    def __validate_dependencies(self) -> None:
        adb_status_code, adb_return_str = subprocess.getstatusoutput(ADB_COMMANDS.ADB)
        aapt_status_code, aapt_return_str = subprocess.getstatusoutput(
            ADB_COMMANDS.AAPT_HELP
        )

        sucess_codes = [0, 1]

        if not adb_status_code in sucess_codes:
            raise AdbDependenciesMissingException(
                missing_dep="ADB", return_str=adb_return_str
            )

        if not aapt_status_code in sucess_codes:
            raise AdbDependenciesMissingException(
                missing_dep="AAPT2", return_str=aapt_return_str
            )

    def __add_package_name(self, package_id: str, package_name: str) -> None:
        self.__saved_package_names[package_id] = package_name
        with open(SETTINGS_PATH + ADB_PACKAGE_NAMES, "w") as package_file:
            json.dump(fp=package_file, obj=self.__saved_package_names)

    def __get_package_name(self, package_id: str) -> str:
        try:
            package_label = self.__saved_package_names[package_id]
            if package_label == None:
                raise AdbFailedToFindPackageException(
                    f'Specified package "{package_id}" has previously failed, ignoring query.'
                )

            return package_label
        except KeyError:
            package_path = self.__execute_adb_command(
                ADB_COMMANDS.ADB_GET_PACKAGE_PATH + package_id
            )
            if package_path == "" or not package_path:
                # self.__add_package_name(package_id=package_id, package_name=None)
                raise AdbFailedToFindPackageException(
                    f'Specified package ID "{package_id}" was not found!'
                )

            if len(package_path.split("\n")) > 1:
                for path in package_path.split("\n"):
                    if package_id in path and "base.apk" in path:
                        package_path = path

            package_path = package_path.replace("package:", "").replace(
                "=" + package_id, ""
            )
            package_name = package_path.split("/")[-1]

            self.__execute_adb_command(
                ADB_COMMANDS.ADB_PULL_PACKAGE + package_path + " /tmp/"
            )
            aapt_out = self.__execute_adb_command(
                ADB_COMMANDS.AAPT_DUMP_BADGING + "/tmp/" + package_name
            )
            try:
                package_label = (
                    re.compile("application-label:'(.*)'").search(aapt_out).group(1)
                )
            except AttributeError:  # Failed to find the regex string
                self.__add_package_name(package_id=package_id, package_name=None)
                raise AdbFailedToFindPackageException(
                    f'Failed to parse aapt package return on package ID "{package_id}"!'
                )

            self.__add_package_name(package_id=package_id, package_name=package_label)

            os.remove("/tmp/" + package_name)

            return package_label

    def __map_adb_attrs(self, adb_attr: ADB_NOTIFICATION_ATTRIBUTES) -> str:
        if not isinstance(
            adb_attr, ADB_NOTIFICATION_ATTRIBUTES
        ):  # If an attribute like 'device' or 'app_name', leave it.
            return adb_attr

        ADB_MAP = {
            ADB_NOTIFICATION_ATTRIBUTES.UID: "id",
            ADB_NOTIFICATION_ATTRIBUTES.TEXT: "body",
            ADB_NOTIFICATION_ATTRIBUTES.OP_PACKAGE: "app_id",
            ADB_NOTIFICATION_ATTRIBUTES.TITLE: "title",
            ADB_NOTIFICATION_ATTRIBUTES.TIME: "time",
        }

        return ADB_MAP[adb_attr]

    @property
    def state(self) -> PHONE_STATES:
        state = self.__execute_adb_command(ADB_COMMANDS.ADB_GET_STATE).split("\n")[0]
        match state:
            case ADB_STATE.ADB_DEVICE:
                return PHONE_STATES.CONNECTED
            case ADB_STATE.ADB_NOT_CONNECTED:
                return PHONE_STATES.DISCONNECTED
            case ADB_STATE.ADB_NO_PERMISSIONS:
                return PHONE_STATES.LOCKED
            case ADB_STATE.ADB_NOT_TRUSTED:
                return PHONE_STATES.UNTRUSTED
            case _:
                self.logger.error(
                    msg='Failed to detect ADB state, falling back to "Not Connected"!'
                )
                return PHONE_STATES.DISCONNECTED

    @property
    def notifications(self) -> list:
        if self.state == PHONE_STATES.CONNECTED:
            notif_dump = self.__execute_adb_command(ADB_COMMANDS.ADB_DUMP_NOTIFICATIONS)
            return self.__parse_notifications(notif_dump)
        else:
            self.logger.error(msg=f"Invalid state: {self.state.value}")
            return []

    @property
    def device_name(self) -> str:
        re_string = "name: (.*)"
        adb_name = self.__execute_adb_command(ADB_COMMANDS.ADB_DEVICE_NAME)
        try:
            return re.compile(re_string).search(adb_name).group(1)
        except AttributeError as err:
            raise AdbFailedToGetDeviceNameException(err)

    def __get_notification_attr_type(self, attr: str):
        result_type = Notification.__annotations__[self.__map_adb_attrs(attr)]
        if (
            typing.get_origin(result_type) == typing.Union
        ):  # The typing library gets a little weird, this ensures it pulls the correct type out of typing.Optional type
            return typing.get_args(result_type)[0]

        return result_type

    def __parse_notifications(self, notifications: str) -> list:
        parsed_notifs = []

        notifs_list = notifications.split("NotificationRecord")
        for notif in notifs_list:
            formatted_notif = {}
            notif_lines = notif.split("\n")
            for line, notif_attr in itertools.product(
                notif_lines, ADB_NOTIFICATION_ATTRIBUTES
            ):
                if re.match(notif_attr.value, line):
                    re_string = (
                        f"{notif_attr.value}(.\S*)"
                        if (
                            not "String (" in line and not "SpannableString (" in line
                        )  # Title & body can be Strings or SpannableStrings
                        else f"{notif_attr.value}.*String \((.*)\)"
                    )
                    try:
                        result = (
                            re.compile(re_string).search(line).group(1)
                        )  # Pull the result based on the regex string
                        result_type = self.__get_notification_attr_type(notif_attr)
                        result = result_type(
                            result
                        )  # Ensure that the result is of the proper type (str, int, etc)
                        formatted_notif[
                            self.__map_adb_attrs(adb_attr=notif_attr)
                        ] = result
                    except AttributeError:  # Failed to find the regex string
                        self.logger.error(
                            msg=f'Failed to find regex string "{re_string}" in "{line}"'
                        )
                        continue

            if len(formatted_notif.keys()) > 0:
                try:
                    # Add the package name
                    name = self.__get_package_name(package_id=formatted_notif["app_id"])
                    formatted_notif["app_name"] = name

                    # Add the device
                    try:
                        formatted_notif["device"] = self.device_name
                    except (
                        AdbFailedToGetDeviceNameException
                    ):  # Normally occurs when the device is disconnected.
                        self.logger.error(msg="Failed to get device name!")
                        formatted_notif["device"] = None

                except (KeyError, AdbFailedToFindPackageException) as err:
                    self.logger.error(
                        msg=f'Failed to find package on notification "{formatted_notif}": {err}'
                    )
                    continue

                try:
                    notif_obj = Notification(**formatted_notif)
                    parsed_notifs.append(notif_obj)
                except (
                    TypeError
                ) as err:  # All the needed values didn't exist, don't create the notification object
                    self.logger.debug(
                        msg=f'Failed to create notification from: "{formatted_notif}": {err}'
                    )
                    continue

        return parsed_notifs

    def __execute_adb_command(self, command: ADB_COMMANDS):
        try:
            return subprocess.getoutput(command)
        except Exception as err:
            raise AdbCommandFailedException(
                f'Failed to execute ADB command "{command}": {err}'
            )
