#!/bin/bash

SETUP_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo $SETUP_DIR

BIN_FILE="$SETUP_DIR/appBIN_FILE=$SETUP_DIR/app"
WORK_DIRECTORY="/etc/mercapi"


DEFAULT_USER="admin"
echo "Enter user name [Default $DEFAULT_USER]: "
read USER

if [ -d "/etc/mercapi" ]; then
    echo "[-] There is already a mercapi installation, do you want to overwrite it (y/n)?"
    read op
    if [ $op = "y" ] || [ $op = "Y"]; then
        rm -rf /etc/mercapi
        mkdir -p /etc/mercapi
    
    else 
        echo "Leaving the installation ..."
        exit 0
    fi
fi

mkdir -p /etc/mercapi

if [ -z "$USER" ]
then
    USER=$DEFAULT_USER
fi

echo "Enter password for user $USER: "
read -s PASSWORD1

echo "Confirm password for user $USER: "
read -s PASSWORD2

if [ "$PASSWORD1" = "$PASSWORD2" ]; then
    ./app setup $USER $PASSWORD1
else
    echo "[-] Password does not match "
    exit 1
fi


if [ -f "data" ]; then
    echo "[+] Data created"
else 
    echo "[-] It is not possible to create the app data, validate permissions"
    exit 1
fi


cp "$SETUP_DIR/app" "$WORK_DIRECTORY"
cp "$SETUP_DIR/data" "$WORK_DIRECTORY"

echo "[Unit]" >> service_file
echo "Description=Daemon mercado api" >> service_file
echo "After=network.target" >> service_file
echo "" >> service_file
echo "[Service]" >> service_file
echo "User=root" >> service_file
echo "WorkingDirectory=$WORK_DIRECTORY" >> service_file
echo "Type=simple" >> service_file
echo "ExecStart=$WORK_DIRECTORY/app" >> service_file
echo "GuessMainPID=no" >> service_file
echo "" >> service_file
echo "[Install]" >> service_file
echo "WantedBy=multi-user.target" >> service_file

cp "$SETUP_DIR/service_file" "/lib/systemd/system/mercapi.service"

rm service_file

systemctl daemon-reload

systemctl enable mercapi.service

systemctl start mercapi.service
