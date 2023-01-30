# PILOT Drive

## **NOTE (01/30/2023)**: 🚧 PILOT Drive is in the middle of a UI transition to React. The current method of a sloppy, untested UI was a quick solution for a while, but is not long term for obvious reasons. Lots of changes may come in the next few months. 🚧 

Tired of your vehicle's closed-source, boring, non-customizable proprietary headunit? Want something a little smarter that you can hack around your own needs? Look no further than PILOT Drive.

PILOT Drive is an open source software/hardware carPC based on the Raspberry Pi and built on Python 3. The objective was to make something that was cheap, reasonably easy to implement, and gave the user a plethora of additional functionality that their vehicle had not prevous offered. 

Currently, PILOT Drive provides support for Bluetooth playback & control, a user interface to the vehicle's OBDII data allowing for more advanced vehicle diagnostics, support for a backup camera, support for displaying Android notifications via ADB, and the ability to remotely update - allowing the user to not pull the whole unit out whenever a new version comes around. All of this presented to the end user (in my build) via a 7" HDMI touchscreen.

In terms of grand vision, these features are just the tip of the iceberg. Things like SDR radio implementation for radio listening of all kinds, GPS for navigation, a more heavily customizable UI, and greater, universal smart phone interfacing to allow for sending of SMSs, more effective notification management, etc. are all on the horizon as PILOT Drive matures as a project.


## Installation + Configuration

PILOT Drive can either be installed & configured using the install script, or manually. If it's an option, the former is heavily suggested.

### Using the install script

1. Pull the install script & run it via: ```su -c 'bash <(curl -s https://raw.githubusercontent.com/lamemakes/pilot-drive/master/install.sh)'```
2. If using a USB soundcard or the [PILOT Drive HAT](https://github.com/lamemakes/pilot-drive-hardware)/DS3231-based RTC, you will need to follow #6 & #8 of [Manual installation](#manual-installation)
3. **Reboot!:** ```sudo reboot now```


### Manual installation

1. Install the project with pip via: ```sudo python3 -m pip install pilot-drive```
2. _[If using Pi-Camera]_ Enable camera in raspi-config
3. Install Firefox ESR via ```sudo apt install firefox-esr```
4. in ```/etc/xdg/lxsession/LXDE-pi/autostart``` append the command ```firefox -kiosk localhost:5000``` to autostart the browser in kiosk mode on boot
5. Install [lukasjapan's bt-speaker](https://github.com/lukasjapan/bt-speaker) via: ```bash <(curl -s https://raw.githubusercontent.com/lukasjapan/bt-speaker/master/install.sh)```
6. _[If using USB soundcard]_ Configure USB soundcard:
    1. Disable 3.5mm jack via "sudo raspi-config"
    2. Confifure USB soundcards via alsa:
        - https://raspberrypi.stackexchange.com/questions/80072/how-can-i-use-an-external-usb-sound-card-and-set-it-as-default
        - https://raspberrypi.stackexchange.com/questions/95193/setting-up-config-for-alsa-at-etc-asound-conf
    3. Edit ```/etc/bt_speaker/config.ini```, set ```cardindex = ``` to reflect the USB sound card index
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
    2. **NOTE:** It is critical that **each** argument is given and in order, enabled or not. This will be more simplistic in versions to come. Enable arguments expect booleans, either in 1/0 format or true/false. If disabling a feature with another parameter, the value of the parameter really doesn't matter, but should probably be 0/false.
    3. Example execution, where the camera is disabled, but ADB & OBD are both enabled:
        - ```python3 -m pilot_drive.config false false true true /dev/pts/1``` <-- Notice the 5 arguments, in order.
12. **Reboot!:** ```sudo reboot now```


When the machine reboots, you should see...

## The UI

In an attempt to keep the UI dynamic, customizable, and have a low barrier to entry in terms of hackability, I opted for a web based UI. So far this has worked pretty well, using Flask as the Python backend, serving data to the ((vanilla)) HTML & JavaScript in real time via ((mostly)) RESTful API calls. 

The interface has 4 main "views":
- **Media**: Bluetooth track data & controls, eventually SDR audio, etc. When nothing is connected, shows a screen instructing the user on how to connect.
- **Car Info**: Displays the OBD feed, showing things like speed, gas, battery voltage, etc.
- **Android Notifications**: Displays ADB notifications, pulling app icons from the connect device. Looking to move into iPhone support soon as well.
- **Settings**: Basic settings tab. Alter time display format, units, and check for updates.

In the top left, the connected bluetooth device shows up, while the time is shown in the center, and the system-wide CPU utilization is shown in the top right.


![2022-10-07-132901_1024x600_scrot](https://user-images.githubusercontent.com/83597346/194638006-a1814312-4ecd-4406-9dc1-3575267e7f11.png)
_Instructional screen, pulling the hostname of the Pi to display_


![2022-10-07-133709_1024x600_scrot](https://user-images.githubusercontent.com/83597346/194638036-15805f4a-e3fe-4c4d-a024-dea50e3fdf7e.png)
_A connected device playing Sweatpants by Gambino. Classic._


![2022-10-07-145356_1024x600_scrot](https://user-images.githubusercontent.com/83597346/194638057-c801d017-4b28-49c8-acab-7d15fe56ba94.png)
_The temporarily ugly OBDII interface. Looking to add more diagnostics and visuals moving forward_


![2022-10-07-144358_1024x600_scrot](https://user-images.githubusercontent.com/83597346/194638077-2f73111b-4a69-4b18-86fb-53e3f89ac685.png)
_The ADB notification interface. This is scrollable, and pulls app icons from connected device_


![2022-10-07-144411_1024x600_scrot](https://user-images.githubusercontent.com/83597346/194638102-b87fb9d9-7990-44bc-acca-b66ffe8951eb.png)
_The settings page, more settings will also come, like UI customization_


![2022-10-07-144429_1024x600_scrot](https://user-images.githubusercontent.com/83597346/194638106-9afb39ba-be57-40d8-b943-16a0784c959e.png)
_An (at the time) up to date PILOT Drive!_


## Notes

- I started PILOT Drive years ago as a very novice & young developer, thus it's (at times) built on some not-so-great code. I'm working to refine and clean up the existing code base though. The real major issue is the sloppy vanilla HTML & JS, but I'm looking to migrate to Vue3 very soon. 
- PILOT Drive is a major WIP. I've put a lot of time into already, but a lot more is planned to hopefully make it the full extent of what it could be, because I do believe in it's potential. 
- This is fully open source o if you seen anything that could be improved feel free to reach out/contribute! All is much appreciated. 
