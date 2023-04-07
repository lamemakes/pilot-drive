#!/bin/bash +x

# Color vars
red="\e[0;91m"
green="\e[0;92m"
blue="\e[0;94m"
endc="\e[0m"
bold="\e[1m"

# Check for root
root_check () {
    if [ "$EUID" -ne 0 ]
    then 
        echo -e "${red}PILOT Drive setup requires root, please re-run as sudo!${endc}"
        echo
        exit
    fi
}

# prompt the user to input y or n, takes input of #1 display string, and #2 default value
# returns true --> y, returns false --> n
prompt_yn () {
    if [[ $skip_yn -eq 1 ]]; then
        user_prompt = $2
    else
        echo -e $1
        read user_prompt
        while [ "${user_prompt,,}" != "y" ] && [ "${user_prompt,,}" != "" ] && [ "${user_prompt,,}" != "n" ] 
        do
            echo -e "${red}Invalid option, give a valid selection!${endc}"
            read user_prompt;
        done
    fi

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

# Confirm the user is root
root_check

echo -e "${green}Starting ${bold}PILOT Drive${endc}${green} installer!${endc}"
echo

echo -e "${blue}Attemtping install of PILOT Drive...${endc}"
echo

# Install PILOT Drive
python3 -m pip install pilot-drive

prompt_yn "${blue}Install \"\e]8;;https://github.com/lukasjapan/bt-speaker\alukasjapan's bt-speaker\e]8;;\a\" for Bluetooth audio? [Y/n]:${endc}" "y"
if [ "$?" -eq 1 ]; then
    echo -e "${blue}Attemtping install of \"\e]8;;https://github.com/lukasjapan/bt-speaker\alukasjapan's bt-speaker\e]8;;\a\"...${endc}"
    echo

    # Download, install, and configure lukasjapan's bt-speaker: https://github.com/lukasjapan/bt-speaker
    bash <(curl -s https://raw.githubusercontent.com/lukasjapan/bt-speaker/master/install.sh)
fi

# Handle phone enabling
prompt_yn "${blue}Setup Android/iOS notification support? [y/N]:${endc}" "n"
if [ "$?" -eq 1 ]; then # enable picam via raspi-config non-interactive mode
    echo -e "${blue}Attemtping install of Android ADB...${endc}"
    echo

    apt install android-tools-adb
    enable_adb=1
fi