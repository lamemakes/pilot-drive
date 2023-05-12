"""
The installer/setup wizard for PILOT Drive
"""
import json
import subprocess
import os
import re
import shutil
import platform
import sys
from enum import StrEnum
from typing import List, Dict, Optional
import requests

from pilot_drive.constants import (
    STATIC_WEB_PORT,
    DEFAULT_BACKEND_SETTINGS,
    SETTINGS_PATH,
    SETTINGS_FILE_NAME,
    WEB_SETTINGS_ATTRIBUTE,
    DEFAULT_WEB_SETTINGS,
)


# Executables directory
BIN_DIR = "/usr/local/bin"

OPT_DIR = "/opt"

# The full service file string for production runs
PILOT_SERVICE = """[Unit]
Description=Pilot Drive service
After=dbus-org.bluez.service
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=python3 -m pilot_drive

[Install]
WantedBy=multi-user.target"""


class Colors(StrEnum):
    """
    String enum of colors to make the terminal pretty on install
    """

    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Cmd(StrEnum):
    """
    String enum of most used bash commands
    """

    SYSTEMCTL = "/bin/systemctl"
    APT_INSTALL = "apt-get -y install"
    YUM_INSTALL = "yum --assumeyes install"
    GIT_CWD = "git -C"  # Using git and changing the wroking dir
    INSTALL_W_READ = "install -m 644"  # Used to install ANCS with read perms
    RASPI_CONFIG_NOINT = "raspi-config nonint"


class DistroManagers(StrEnum):
    """
    String enum of distribution managers
    """

    APT = "apt"
    YUM = "yum"


class CommonArchs(StrEnum):
    """
    String enum of common system architectures
    """

    AARCH64 = "aarch64"
    ARM64 = "arm64"
    ARMV7L = "armv7l"
    INTEL_AMD = "x86"
    INTEL_AMD_64 = "x86_64"


class FailedToExecuteCommandException(Exception):
    """
    Raised when a subprocess command fails to execute
    """


class FailedToDetectDistroManagerException(Exception):
    """
    Raised when the distribution manager could not be detected
    """


class Installer:
    """
    The installer used to install and configure PILOT Drive
    """

    def __init__(self, use_default: bool = True) -> None:
        """
        Initialize the PILOT Drive installer

        :param use_default: use all the preset default values to allow for a non-interactive setup
        """
        # Requried to know sys architecture for certain operations (ie. installing AAPT2)
        try:
            self.current_arch = CommonArchs(platform.uname().machine)
        except ValueError:
            sys.exit(
                f'Failed to detect system architecture, "{platform.uname().machine}"'
                f"is not recognized by the installer at this time."
            )

        self.distro_manager = self.detect_distro_manager()
        self.is_production = False
        self.is_rpi = False
        self.use_default = use_default

    def exec_cmd(self, command: str) -> str:
        """
        Used to execute bash commands via subprocess

        :param command: the command to be executed
        :raises: FailedToExecuteCommandException when the executed command returns and error
        """

        bash_result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=False
        )
        if bash_result.stderr:
            raise FailedToExecuteCommandException(
                f'Execution of command: "{command}" returned and error of: "{bash_result.stderr}"'
            )

        if bash_result.stdout and bash_result.stdout[-1] == "\n":
            return bash_result.stdout[:-1]  # Remove the last newline

        return bash_result.stdout

    def prompt_yes_no(self, prompt: str, default_in: str) -> bool:
        """
        Handle y/n prompts in terminal as the user configures PILOT Drive

        :param prompt: the message/question to prompt the user with
        :param default_in: the default option ("y" or "n")
        :return: True if user input matches the default
        """
        options = ["Y", "N"]

        default = default_in.upper()
        if default not in options:
            raise ValueError(f'Invalid yes/no prompt default: "{default}"')

        opts_str = "[y/N]" if default == "N" else "[Y/n]"

        user_in: str = ""

        while user_in not in options:
            user_in = input(
                f"{Colors.BLUE}{Colors.BOLD}{prompt} {opts_str}: {Colors.ENDC}"
            ).upper()
            if user_in == "":
                user_in = default

            if user_in not in options:
                print(
                    f'{Colors.FAIL}{Colors.BOLD}Invalid input "{user_in}"!{Colors.ENDC}'
                )

        return user_in == default_in.upper()

    def prompt_list(self, prompt: str, options: List[str], default_in: int) -> int:
        """
        Handle list prompts in terminal

        :param prompt: the prompt for the user
        :param options: the list of options to present to the user
        :return: the index of the user's selected option
        """

        disp_options = []
        print(f"{Colors.BLUE}{Colors.BOLD}{prompt}: {Colors.ENDC}")
        for count, option in enumerate(options):
            option_str = f"[ {count} ] {option}"
            print(f"{Colors.CYAN}{Colors.BOLD}{option_str}{Colors.ENDC}")
            disp_options.append(str(count))

        user_in = ""
        while user_in not in disp_options:
            user_in = input(
                f"{Colors.BLUE}{Colors.BOLD}Make a selection "
                f"[0-{len(options) - 1}], or press enter for the default [{default_in}]: "
                f"{Colors.ENDC}"
            )

            if user_in == "":
                user_in = str(default_in)

            if user_in not in disp_options:
                print(
                    f'{Colors.FAIL}{Colors.BOLD}Invalid input "{user_in}"!{Colors.ENDC}'
                )

        return int(user_in)

    def prompt_input(
        self, prompt: str, regex_validator: str, example: Optional[str] = None
    ) -> str:
        """
        Handle general string prompts in terminal

        :param prompt: the prompt for the user
        :param regex_validator: the regex string to validate the user input
        :param example: an optional example string to be provided to the user
        :return: the user's input string
        """
        prompt_str = f'{prompt} (ie. "{example}")' if example is not None else prompt

        user_in = ""
        while re.search(regex_validator, user_in) is None:
            user_in = input(f"{Colors.BLUE}{Colors.BOLD}{prompt_str}: {Colors.ENDC}")

            if re.search(regex_validator, user_in) is None:
                print(
                    f'{Colors.FAIL}{Colors.BOLD}Invalid input "{user_in}"!{Colors.ENDC}'
                )

        return user_in

    def detect_distro_manager(self) -> DistroManagers:
        """
        Detect the distribution manager used by the host

        :return: DistroManager Enum item with the detected distribution manager
        :raise: FailedToDetectDistroManagerException if distribution manager could not be detected
        """
        manager = None

        try:
            self.exec_cmd(DistroManagers.APT)
            manager = DistroManagers.APT
        except FailedToExecuteCommandException:
            pass

        try:
            self.exec_cmd(DistroManagers.YUM)
            manager = DistroManagers.YUM
        except FailedToExecuteCommandException:
            pass

        if manager is None:
            raise FailedToDetectDistroManagerException(
                "Distribution manager could not be detected!"
            )

        return manager

    def install_from_distro_manager(self, packages: List[str]) -> None:
        """
        Installs a specified package from the distribution manager depending on the OS/manager used
        """
        # Mappings for apt packages -> yum
        apt_to_yum: Dict[str, str] = {
            "python3-gi": "python36-gobject",
            "firefox-esr": "firefox",
        }

        # Reverse the apt_to_yum mappings to allow for mapping of yum -> map
        yum_to_apt: Dict[str, str] = {v: k for k, v in apt_to_yum.items()}

        for count, package in enumerate(packages):
            if self.distro_manager == DistroManagers.YUM and package in apt_to_yum:
                packages[count] = apt_to_yum[package]
            elif self.distro_manager == DistroManagers.APT and package in yum_to_apt:
                packages[count] = yum_to_apt[package]

        packages_str = " ".join(packages)

        match self.distro_manager:
            case DistroManagers.APT:
                self.exec_cmd(f"{Cmd.APT_INSTALL} {packages_str}")
            case DistroManagers.YUM:
                self.exec_cmd(f"{Cmd.YUM_INSTALL} {packages_str}")
            case _:
                sys.exit(
                    f"{Colors.FAIL}{Colors.BOLD}Package manger: "
                    f'{self.distro_manager}" not recognized, exiting!'
                )

    def install_bt_speaker(self) -> None:
        """
        Install bt-speaker by lukasjapan. For the time being, this is debian specific.

        bt-speaker install is based off the sh installer, here:
        https://github.com/lukasjapan/bt-speaker/blob/master/install.sh
        """

        print(
            rf"{Colors.GREEN}{Colors.BOLD}Attempting to install"
            rf"\e]8;;https://github.com/lukasjapan/bt-speaker\alukasjapan\'s bt-speaker\e]8;;\a..."
            rf"{Colors.ENDC}"
        )
        bt_speaker_dir = f"{OPT_DIR}/bt-speaker"
        bt_speaker_url = "https://github.com/lukasjapan/bt-speaker.git"
        bt_speaker_hook_dir = "/etc/bt_speaker/hooks"

        # Install dependencies
        subprocess.check_output(
            f"{Cmd.APT_INSTALL} git bluez python3 libasound2-dev python3-gi"
            "python3-gi-cairo python3-cffi python3-dbus python3-alsaaudio"
            "sound-theme-freedesktop vorbis-tools",
            shell=True,
        )
        self.exec_cmd("python3 -m pip install cffi pyalsaaudio")

        # Create user groups
        subprocess.check_output(
            (
                "id -u btspeaker &>/dev/null || "
                "useradd btspeaker -G audio -d {OPT_DIR}/bt_speaker"
            ),
            shell=True,
        )
        subprocess.check_output(
            "getent group bluetooth &>/dev/null && usermod -a -G bluetooth btspeaker",
            shell=True,
        )

        # Update repo if it exists, clone it if not
        if os.path.exists(f"{bt_speaker_dir}"):
            self.exec_cmd(f"{Cmd.GIT_CWD} {bt_speaker_dir} pull")
            self.exec_cmd(f"{Cmd.GIT_CWD} {bt_speaker_dir} checkout master")
        else:
            self.exec_cmd(f"{Cmd.GIT_CWD} {OPT_DIR}/ clone {bt_speaker_url}")
            self.exec_cmd(f"{Cmd.GIT_CWD} {bt_speaker_dir} checkout master")

        # Copy hooks into proper directory
        os.makedirs(bt_speaker_hook_dir, exist_ok=True)
        shutil.copy(
            f"{bt_speaker_dir}/config.ini.default", "/etc/bt_speaker/config.ini"
        )
        shutil.copy(
            f"{bt_speaker_dir}/hooks.default/connect", f"{bt_speaker_hook_dir}/connect"
        )
        shutil.copy(
            f"{bt_speaker_dir}/hooks.default/disconnect",
            f"{bt_speaker_hook_dir}/disconnect",
        )
        shutil.copy(
            f"{bt_speaker_dir}/hooks.default/startup", f"{bt_speaker_hook_dir}/startup"
        )
        shutil.copy(
            f"{bt_speaker_dir}/hooks.default/track", f"{bt_speaker_hook_dir}/track"
        )

        # Create the service
        subprocess.check_output(
            f"{Cmd.SYSTEMCTL} enable {bt_speaker_dir}/bt_speaker.service", shell=True
        )
        self.exec_cmd(f"{Cmd.SYSTEMCTL} restart bt_speaker")
        print(f"{Colors.GREEN}Completed bt-speaker install!{Colors.ENDC}")

    def install_firefox(self) -> None:
        """
        Install Firefox
        """
        print(
            f"{Colors.GREEN}{Colors.BOLD}Attempting to install Firefox...{Colors.ENDC}"
        )

        # Install Firefox ESR
        self.install_from_distro_manager(["firefox"])

        print(f"{Colors.GREEN}{Colors.BOLD}Completed Firefox install!{Colors.ENDC}")

    def install_adb(self) -> None:
        """
        Install ADB and it's needed dependencies
        """
        appt2_url = (
            "https://raw.githubusercontent.com/lamemakes/pilot-drive/master/bin/aapt2"
        )

        # Check if ADB is already accessible to subprocess
        try:
            self.exec_cmd("adb")
        except FailedToExecuteCommandException:
            print(
                f"{Colors.GREEN}{Colors.BOLD}Attempting to install "
                f"Android Debug Bridge...{Colors.ENDC}"
            )

            self.install_from_distro_manager(["adb"])

            print(f"{Colors.GREEN}Completed ADB install!{Colors.ENDC}")

        # Check is AAPT2 is already accessible to subprocess
        try:
            self.exec_cmd("aapt2")
        except FailedToExecuteCommandException:
            print(
                f"{Colors.GREEN}{Colors.BOLD}Attempting to pull and install AAPT2...{Colors.ENDC}"
            )
            match self.current_arch:
                case CommonArchs.AARCH64 | CommonArchs.ARM64:
                    aapt2_arch = "arm64-v8a"
                case CommonArchs.ARMV7L:
                    aapt2_arch = "armeabi-v7a"
                case _:
                    # If the arch didn't match the above,
                    # it SHOULD agree with the URL structure on it's own.
                    aapt2_arch = self.current_arch

            aapt2_bin = requests.get(
                f"{appt2_url}/{aapt2_arch}/aapt2", timeout=3000
            ).content
            with open(f"{BIN_DIR}/aapt2", "wb") as aapt2_file:
                aapt2_file.write(aapt2_bin)

            print(f"{Colors.GREEN}Completed AAPT2 install!{Colors.ENDC}")

    def install_ancs(self) -> None:
        """
        Install ANCS4Linux to get iOS/iPadOS notifications

        Based off of the shell script here:
        https://github.com/pzmarzly/ancs4linux/blob/master/autorun/install.sh
        """
        ancs_repo = "https://github.com/pzmarzly/ancs4linux"
        ancs_dir = f"{OPT_DIR}/ancs4linux"

        print(f"{Colors.GREEN}Attempting ANCS4Linux install...{Colors.ENDC}")

        # Clone the repo & install dependencies
        self.install_from_distro_manager(["python3-gi"])
        self.exec_cmd(f"{Cmd.GIT_CWD} {OPT_DIR}/ clone {ancs_repo}")

        # Create ancs4linux user
        self.exec_cmd("groupadd -f ancs4linux")
        root_user = self.exec_cmd("${SUDO_USER:-root}")
        self.exec_cmd(f'usermod -a -G ancs4linux "{root_user}"')

        # Install as a service
        self.exec_cmd(
            f"{Cmd.INSTALL_W_READ} {ancs_dir}/autorun/ancs4linux-observer.service"
            f"/usr/lib/systemd/system/ancs4linux-observer.service"
        )
        self.exec_cmd(
            f"{Cmd.INSTALL_W_READ} {ancs_dir}/autorun/ancs4linux-observer.xml"
            f"/etc/dbus-1/system.d/ancs4linux-observer.conf"
        )
        self.exec_cmd(
            f"""{Cmd.INSTALL_W_READ} {ancs_dir}/autorun/ancs4linux-advertising.service
             /usr/lib/systemd/system/ancs4linux-advertising.service"""
        )
        self.exec_cmd(
            f"{Cmd.INSTALL_W_READ} {ancs_dir}/autorun/ancs4linux-advertising.xml"
            f"/etc/dbus-1/system.d/ancs4linux-advertising.conf"
        )
        self.exec_cmd(
            f"{Cmd.INSTALL_W_READ} {ancs_dir}/autorun/ancs4linux-desktop-integration.service"
            f"/etc/dbus-1/system.d/ancs4linux-desktop-integration.service"
        )  # Maybe not needed?

        self.exec_cmd(f"cd {ancs_dir} && pip3 install .")

        self.exec_cmd(f"{Cmd.SYSTEMCTL} daemon-reload")

        # Enable & start the ANCS service
        self.exec_cmd(f"{Cmd.SYSTEMCTL} enable ancs4linux-observer.service")
        self.exec_cmd(f"{Cmd.SYSTEMCTL} enable ancs4linux-advertising.service")
        self.exec_cmd(
            f"{Cmd.SYSTEMCTL} --global enable ancs4linux-desktop-integration.service"
        )  # Maybe not needed?

        self.exec_cmd(f"{Cmd.SYSTEMCTL} restart ancs4linux-observer.service")
        self.exec_cmd(f"{Cmd.SYSTEMCTL} restart ancs4linux-advertising.service")

        print(f"{Colors.GREEN}Completed ANCS4Linux install!{Colors.ENDC}")

    def for_production(self):
        """
        Run PILOT Drive for production, configure the systemctl service, auto-start mozilla, etc.
        """

        pilot_service_path = "/etc/systemd/system/pilot-drive.service"
        print(
            f"{Colors.GREEN}Attempting to configure PILOT Drive for production...{Colors.ENDC}"
        )

        print(
            f"{Colors.GREEN}Attempting to configure the PILOT Drive service...{Colors.ENDC}"
        )

        # Create and enable the PILOT Drive systemctl service
        with open(pilot_service_path, "w", encoding="utf-8") as pilot_service:
            pilot_service.write(PILOT_SERVICE)

        try:
            self.exec_cmd(f"{Cmd.SYSTEMCTL} enable pilot-drive")
        except FailedToExecuteCommandException:
            # systemctl doesn't conform to Unix "standards" and outputs to stderr for some reason.
            pass

        # Configure firefox kiosk mode
        configure_firefox = False
        try:
            firefox_ver = self.exec_cmd("firefox --version")
            if "Mozilla Firefox" in firefox_ver:
                configure_firefox = True
            else:
                print(
                    f"{Colors.WARNING}{Colors.BOLD}Firefox was not detected, "
                    f"autostart in kiosk mode will not be configured!{Colors.ENDC}"
                )
        except FailedToExecuteCommandException:
            print(
                f"{Colors.WARNING}{Colors.BOLD}Firefox was not detected, "
                f"autostart in kiosk mode will not be configured!{Colors.ENDC}"
            )

        if configure_firefox:
            autostart_path = "/etc/xdg/lxsession/LXDE-pi/autostart"
            autostart_string = f"firefox -kiosk localhost:{STATIC_WEB_PORT}"

            # Configure Firefox to launch in kiosk mode on boot
            print(
                f"{Colors.GREEN}{Colors.BOLD}Attempting to configure LXDE "
                f"to auto-launch Firefox on boot...{Colors.ENDC}"
            )

            lxde_contents = ""
            with open(autostart_path, "r", encoding="utf-8") as lxde_file:
                lxde_contents = lxde_file.read()

            if not lxde_contents or lxde_contents == "":
                print(
                    f"{Colors.WARNING}{Colors.BOLD}Failed to read LXDE file, "
                    f"Firefox ESR autostart will not be set!{Colors.ENDC}"
                )

            write_contents = False
            new_lxde_contents: List[str] = []

            if autostart_string in lxde_contents:
                if f"{autostart_string}{STATIC_WEB_PORT}" not in lxde_contents:
                    for line in lxde_contents.split("\n"):
                        if autostart_string in line:
                            line = f"{autostart_string}{STATIC_WEB_PORT}"
                        new_lxde_contents.append(line)
                    write_contents = True
            else:
                new_lxde_contents = lxde_contents.split("\n") + [f"{autostart_string}"]
                write_contents = True

            if write_contents and len(new_lxde_contents) > 0:
                with open(autostart_path, "w", encoding="utf-8") as lxde_file:
                    lxde_file.write("\n".join(new_lxde_contents))

    def rpi_setup(self):
        """
        Configuration specific to a Raspberry Pi running in production
        """

        # Disable RPi blanking
        print(f"{Colors.GREEN}Attempting to disable RPi blanking...{Colors.ENDC}")
        try:
            self.exec_cmd(f"{Cmd.RASPI_CONFIG_NOINT} do_blanking 1")
        except FailedToExecuteCommandException as exc:
            print(
                f'{Colors.WARNING}{Colors.BOLD}Failed to execute raspi-config: "{exc}", '
                f"skipping Raspberry Pi configuration!{Colors.ENDC}"
            )
            return

        # Disable RPi overscan
        print(f"{Colors.GREEN}Attempting to disable RPi overscan...{Colors.ENDC}")
        try:
            self.exec_cmd(f"{Cmd.RASPI_CONFIG_NOINT} do_overscan 1")
        except FailedToExecuteCommandException as exc:
            print(
                f'{Colors.WARNING}{Colors.BOLD}Failed to execute raspi-config: "{exc}", '
                f"skipping Raspberry Pi configuration!{Colors.ENDC}"
            )
            return

        # Remove the piwiz file to prevent allowing GUI prompts
        pi_desktop_wizard = "/etc/xdg/autostart/piwiz.desktop"

        if os.path.exists(pi_desktop_wizard):
            print(
                f"{Colors.GREEN}Attempting to disable RPi setup wizard prompts...{Colors.ENDC}"
            )
            os.remove(pi_desktop_wizard)

    def install_rpi_camera(self) -> int:
        """
        Setup the Raspberry Pi camera along with it's button trigger pin

        :return: camera pin integer
        """
        valid_gpios = {
            3,
            5,
            7,
            8,
            10,
            11,
            12,
            13,
            15,
            16,
            18,
            19,
            21,
            22,
            23,
            24,
            26,
            27,
            28,
            29,
            31,
            32,
            33,
            35,
            36,
            37,
            38,
            40,
        }
        pd_hat_default = 16  # PILOT Drive HAT uses pin 16

        user_in: int = 0
        while user_in not in valid_gpios:
            pin = input(
                f"{Colors.BLUE}{Colors.BOLD}Input a camera button GPIO pin (board format) or "
                f"press enter for the PILOT Drive HAT default [{pd_hat_default}]: {Colors.ENDC}"
            )
            try:
                user_in = int(pin) if pin != "" else pd_hat_default
                if user_in not in valid_gpios:
                    print(
                        f'{Colors.FAIL}{Colors.BOLD}Invalid input "{user_in}",'
                        f"not a valid Raspberry Pi board GPIO pin!{Colors.ENDC}"
                    )
            except ValueError:
                print(
                    f'{Colors.FAIL}{Colors.BOLD}Invalid input "{pin}", '
                    f"was expecting an integer!{Colors.ENDC}"
                )

        self.exec_cmd(f"{Cmd.RASPI_CONFIG_NOINT} nonint do_camera 0")

        return user_in

    def main(self) -> None:  # pylint: disable=too-many-statements
        """
        Run the PILOT Drive installer/config
        """
        settings = {
            **DEFAULT_BACKEND_SETTINGS,
            WEB_SETTINGS_ATTRIBUTE: {**DEFAULT_WEB_SETTINGS},
        }

        self.is_production = self.prompt_yes_no(
            prompt=(
                "Setup for production (create system process "
                "auto-start firefox in kiosk mode, etc)?"
            ),
            default_in="y",
        )
        print()

        # Architecture prompt
        if self.current_arch in [
            CommonArchs.ARM64,
            CommonArchs.ARMV7L,
            CommonArchs.AARCH64,
        ]:
            self.is_rpi = self.prompt_yes_no(
                prompt="Detected ARM architecture, setup as Raspberry Pi?",
                default_in="y",
            )

        # Distro manager prompt
        distro_list = list(DistroManagers)

        try:
            manager_guess = self.detect_distro_manager()
            default = distro_list.index(manager_guess)
        except FailedToDetectDistroManagerException:
            manager_guess = None
            default = 0  # Default the first item if guess fails

        if manager_guess is not None:
            prompt_str = (
                f"Detected distribution manager of {Colors.GREEN}{manager_guess}{Colors.BLUE}! "
                "Press enter to use the detected, or select another"
            )
        else:
            prompt_str = "Failed to detect distribution manager, select one"

        selection = self.prompt_list(
            prompt=prompt_str, options=distro_list, default_in=default
        )
        self.distro_manager = DistroManagers(distro_list[selection])
        print(
            f"{Colors.GREEN}{Colors.BOLD}Distribution manager "
            f"set to {self.distro_manager}{Colors.ENDC}"
        )
        print()

        # Firefox prompt
        if self.prompt_yes_no(prompt="Attempt Firefox install?", default_in="y"):
            self.install_firefox()
        print()

        # Phone prompt
        phone_list = ["None/Disable", "iOS", "Android"]
        phone_prompt = self.prompt_list(
            prompt="Use a phone with PILOT Drive?", options=phone_list, default_in=0
        )
        match phone_prompt:
            case 0:
                pass  # Don't configure the phone
            case 1:
                settings["phone"]["enabled"] = True
                settings["phone"]["type"] = phone_list[phone_prompt].lower()
                self.install_ancs()
            case 2:
                settings["phone"]["enabled"] = True
                settings["phone"]["type"] = phone_list[phone_prompt].lower()
                self.install_adb()
            case _:
                print(
                    f"""{Colors.WARNING}{Colors.BOLD}Selection not recognized,
                     phone will not be configured.{Colors.ENDC}"""
                )
        print()

        # Vehicle/OBDII prompt
        vehicle_prompt = self.prompt_yes_no(
            prompt="Enable OBDII functionality?", default_in="n"
        )
        if not vehicle_prompt:
            port = self.prompt_input(
                prompt="Enter the path to the OBDII serial port",
                regex_validator=r"^\/(.+)\/([^\/]+)$",
                example="/dev/ttyUSB0",
            )
            settings["vehicle"]["enabled"] = True
            settings["vehicle"]["port"] = port
            print(
                f"{Colors.GREEN}{Colors.BOLD}OBDII functionality enabled, "
                f'and port set to "{port}"{Colors.ENDC}'
            )

        if self.is_rpi:
            camera_prompt = self.prompt_yes_no(
                prompt="Enable Raspberry Pi Camera functionality?", default_in="n"
            )
            if not camera_prompt:
                try:
                    settings["camera"]["buttonPin"] = self.install_rpi_camera()
                    settings["camera"]["enabled"] = True
                except KeyboardInterrupt:
                    print(
                        f"{Colors.FAIL}{Colors.BOLD}Cancelling RPi Camera Setup!{Colors.ENDC}"
                    )

        print()
        print(
            f"{Colors.BLUE}{Colors.BOLD}Attempting to setup for production...{Colors.ENDC}"
        )
        if self.is_production:
            if self.is_rpi:
                self.rpi_setup()

            self.for_production()

        print()
        print(
            f"{Colors.BLUE}{Colors.BOLD}Attempting to writing PILOT Drive settings to "
            f'"{SETTINGS_PATH}{SETTINGS_FILE_NAME}"...{Colors.ENDC}'
        )
        os.makedirs(name=SETTINGS_PATH, exist_ok=True)
        with open(
            f"{SETTINGS_PATH}{SETTINGS_FILE_NAME}", "w", encoding="utf-8"
        ) as config:
            json.dump(obj=settings, fp=config, indent=2)

        print()
        print(
            f"{Colors.GREEN}{Colors.BOLD}PILOT Drive install has been completed!{Colors.ENDC}"
        )
