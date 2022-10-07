# PILOT Drive

Tired of your vehicle's closed-source, boring, non-customizable proprietary headunit? Want something a little smarter that you can hack around your own needs? Look no further than PILOT Drive.

PILOT Drive is an open source software/hardware carPC based on the Raspberry Pi and built on Python 3. The objective was to make something that was cheap, reasonably easy to implement, and gave the user a plethora of additional functionality that their vehicle had not prevous offered. 

Currently, PILOT Drive provides support for Bluetooth playback & control, a user interface to the vehicle's OBDII data allowing for more advanced vehicle diagnostics, support for a backup camera, support for displaying Android notifications via ADB, and the ability to remotely update - allowing the user to not pull the whole unit out whenever a new version comes around. All of this presented to the end user (in my build) via a 7" HDMI touchscreen.

In terms of grand vision, these features are just the tip of the iceberg. Things like SDR radio implementation for radio listening of all kinds, GPS for navigation, a more heavily customizable UI, and greater, universal smart phone interfacing to allow for sending of SMSs, more effective notification management, etc. are all on the horizon as PILOT Drive matures as a project.


## Installation + Configuration

PILOT Drive can either be installed & configured using the install script, or manually. If it's an option, the former is heavily suggested.

### Using the install script

To install PILOT Drive via the install script, on newly setup & internet connected Raspberry Pi (I'm using a Pi 4 B), execute:

```su -c 'bash <(curl -s https://raw.githubusercontent.com/lamemakes/pilot-drive/master/install.sh)'```

This will pull & install the project, automating all the manual configuration steps.

**NOTE:** If using a USB soundcard or the [PILOT Drive HAT](https://github.com/lamemakes/pilot-drive-hardware)/DS3231-based RTC, you will need to follow #6 & #8 of [Manual installation](#manual-installation)

### Manual installation

1. Install the project with pip:
    1. ```sudo python3 -m pip install pilot-drive```

2. _[If using Pi-Camera]_ Enable camera in raspi-config

3. Install Firefox ESR:
    1. ```sudo apt install firefox-esr```

4. in ```/etc/xdg/lxsession/LXDE-pi/autostart``` append the command ```firefox -kiosk localhost:5000``` to autostart the browser in kiosk mode on boot

5. Install lukasjapan's bt-speaker via: 
    1. ```bash <(curl -s https://raw.githubusercontent.com/lukasjapan/bt-speaker/master/install.sh)```

6. _[If using USB soundcard]_ Configure USB soundcard:
    1. Disable 3.5mm jack via "sudo raspi-config"
    2. Confifure USB soundcards via alsa:
        - https://raspberrypi.stackexchange.com/questions/80072/how-can-i-use-an-external-usb-sound-card-and-set-it-as-default
        - https://raspberrypi.stackexchange.com/questions/95193/setting-up-config-for-alsa-at-etc-asound-conf
    3. Edit ```/etc/bt_speaker/config.ini```, set ```cardindex = ``` to reflect the usb sound card

7. _[If using Android Debug Bridge for notifications]_ Install ADB for linux:
    1. ```sudo apt install android-tools-adb```

8. _[If using DS3231 RTC]_ Follow RTC tutorial:
    - https://www.raspberrypi-spy.co.uk/2015/05/adding-a-ds3231-real-time-clock-to-the-raspberry-pi/

9. _[Display & preference dependant]_ Configure display:
    1. Enable overscan via raspi-config UI or ```sudo raspi-config nonint do_overscan 1```
    2. Disable screen blanking via raspi-config UI or ```sudo raspi-config nonint do_blanking 1```

10. Create a new service for PILOT-Drive:
    1. Create the service file ```/etc/systemd/system/pilot-drive.service``` via:
        ```
        sudo cat << EOF > /etc/systemd/system/pilot-drive.service
        [Unit]
        Description=Pilot Drive service
        After=dbus-org.bluez.service
        StartLimitIntervalSec=0

        [Service]
        Type=simple
        Restart=always
        RestartSec=1
        User=root
        ExecStart=python3 -m pilot_drive.main

        [Install]
        WantedBy=multi-user.target

        EOF
        ```
    2. Execute ```sudo systemctl enable pilot-drive.service``` to start the service on boot

11. Initialize the PILOT Drive config:
    1. ```python3 -m pilot_drive.config <enable backup camera> <camera button pin> <enable ADB> <enable OBD> <OBD port>```
    2. **NOTE:** It is critical that **each** argument is given and in order, enabled or not. This will be more simplictic in versions to come. Enable arguments expect booleans, either in 1/0 format or true/false. If disabling a feature with another parameter, the value of the parameter really doesn't matter, but should probably be 0/false.
    3. Example execution, where the camera is disabled, but ADB & OBD are both enabled:
        - ```python3 -m pilot_drive.config false false true true /dev/pts/1``` <-- Notice the 5 arguments, in order.

12. **Reboot!**
    1. ```sudo reboot now```
