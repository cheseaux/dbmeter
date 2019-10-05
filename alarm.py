#!/usr/bin/python

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
p = GPIO.PWM(27, 100)


def alarm():
    for x in range(0, 3):
        GPIO.output(27, True)
        time.sleep(0.1)
        GPIO.output(27, False)
        time.sleep(0.1)
    for x in range(0, 3):
        GPIO.output(27, True)
        time.sleep(0.05)
        GPIO.output(27, False)
        time.sleep(0.05)
    GPIO.output(27, False)


def ring_alarm():
    alarm()
