#!/bin/bash -ex

[ `whoami` = root ] || { sudo "$0" "$@"; exit $?; }
cp dbwatcher.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable dbwatcher.service
