#!/bin/bash +x
# Halt script if error is detected
set -e

# Color vars
red="\e[0;91m"
green="\e[0;92m"
blue="\e[0;94m"
endc="\e[0m"
bold="\e[1m"

# Initial vars
enable_adb=0
enable_cam=0
btn_pin=0
enable_obd=0
obd_port=0

# Check for root
root_check () {
    if [ "$EUID" -ne 0 ]
    then 
        echo -e "${red}PILOT Drive setup requires root, please re-run as sudo!${endc}"
        echo
        exit
    fi
}

# pi_check() {
#     if [[ ! "$(cat /proc/cpuinfo)" =~ "Model\t\t: Raspberry Pi" ]]
#     then 
#         echo -e "${red}PILOT Drive setup needs to be run on a Raspberry Pi!${endc}"
#         echo
#         exit
#     fi
# }

# prompt the user to input y or n, takes input of #1 display string, and #2 default value
# returns true --> y, returns false --> n
prompt_yn () {
    if [[ $skip_yn -eq 1 ]]; then
        return 1
    fi
    echo -e $1
    read user_prompt
    while [ "${user_prompt,,}" != "y" ] && [ "${user_prompt,,}" != "" ] && [ "${user_prompt,,}" != "n" ] 
    do
        echo -e "${red}Invalid option, give a valid selection!${endc}"
        read user_prompt;
    done

    if [ "$user_prompt" = "" ]; then
        if [ $2 = "y" ]; then
            return 1
        elif [ $2 = "n" ]; then
            return 0
        fi
    elif [ "$user_prompt" = "y" ]; then
        return 1
    elif [ "$user_prompt" = "n" ]; then
        return 0
    fi
}

# Confirm the script is being ran as sudo or root & on a RPi
root_check
#pi_check

echo -e "${green}Starting ${bold}PILOT Drive${endc}${green} installer!${endc}"
echo

echo -e "${blue}Attemtping install of PILOT Drive...${endc}"
echo

# Install PILOT Drive
python3 -m pip install pilot-drive


echo -e "${blue}Attemtping install of lukasjapan's bt-speaker from \"https://github.com/lukasjapan/bt-speaker\"...${endc}"
echo

# Download, install, and configure lukasjapan's bt-speaker: https://github.com/lukasjapan/bt-speaker
bash <(curl -s https://raw.githubusercontent.com/lukasjapan/bt-speaker/master/install.sh)

# Handle ADB enabling
prompt_yn "${blue}Setup Android notification support? [y/N]:${endc}" "n"
if [ "$?" -eq 1 ]; then # enable picam via raspi-config non-interactive mode
    echo -e "${blue}Attemtping install of Android ADB...${endc}"
    echo

    apt install android-tools-adb
    enable_adb=1
fi

# Handle PiCamera enabling
prompt_yn "${blue}Setup RPi Camera (backup camera) with PILOT Drive? [Y/n]:${endc}" "y"
if [ "$?" -eq 1 ]; then # enable picam via raspi-config non-interactive mode
    echo -e "${blue}Enter camera trigger button GPIO pin (ie. if button is attached to pin 16, enter \"16\")${endc}"
    read user_prompt
    while [ "${user_prompt,,}" == "" ] || [ "${user_prompt,,}" == " " ] || ![[ $var =~ ^-?[0-9]{1,2}$ ]]
    do
        log "${red}Invalid option, give a valid selection!${endc}";
        read user_prompt;
    done

    raspi-config nonint do_camera 0 && return 0
    enable_cam=1
fi

# Handle OBDII enabling
prompt_yn "${blue}Setup OBDII reader with PILOT Drive? [Y/n]:${endc}" "y"
if [ "$?" -eq 1 ]; then # enable OBDII, prompt user for port
    echo -e "${blue}Enter OBDII reader port (ie. /dev/ttyUSB0), or press enter to use port detection.${endc}"
    read user_prompt
    while [ "${user_prompt,,}" == " " ]
    do
        log "${red}Invalid option, give a valid selection!${endc}";
        read user_prompt;
    done

    obd_port=user_prompt
    enable_obd=1
fi

# Install Firefox ESR (required for PILOT Drive)
echo -e "${blue}Attemtping install of Firefox ESR...${endc}"
echo
apt install firefox-esr

# Config LDXE autostart & create pilot-drive service
echo -e "${blue}Attempting to create required PILOT Drive services...${endc}"
echo

# Create the pilot-drive service
cat << EOF > /etc/systemd/system/pilot-drive.service
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

systemctl enable pilot-drive


# Configure the LXDE autostart
autostart_file="/etc/xdg/lxsession/LXDE/autostart"
autostart_string="firefox -kiosk localhost:5000"

if !(grep -q "$autostart_string" "$autostart_path"); then
  echo -e "$autostart_string" >> $autostart_file
fi

# Finally, iterface with the pilot config python module to generate the config
python3 -m pilot_drive.config enable_cam btn_pin enable_adb enable_obd obd_port

echo -e "${green}Done!${endc}"
echo 

# Handle reboot
prompt_yn "${red}A reboot is required! Preform it now or later? [Y/n]:${endc}" "y"
if [ "$?" -eq 1 ]; then # reboot 
    reboot now
fi