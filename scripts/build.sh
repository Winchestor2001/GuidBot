#!/bin/bash

R='\033[0;31m'
G='\033[0;32m'
NOCOLOR='\033[0m'

cd /srv/project/guid_bot || exit 1

sleep 1

if sudo docker compose down; then
    echo -e "${G}docker compose down success${NOCOLOR}"
    if sudo docker compose up -d; then
        echo -e "${G}docker compose up -d success${NOCOLOR}"
    else
        echo -e "${R}error docker compose up -d.${NOCOLOR}"
        exit 130
    fi
else
    echo -e "${R}error sudo docker compose down${NOCOLOR}"
    exit 130
fi
