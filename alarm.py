#!/usr/bin/python

import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
p = GPIO.PWM(27, 100)

def whooze():
  GPIO.output(27, True) 
  p.start(10) 
  speed = 0.001
  for hz in range(440, 1000):
    p.ChangeFrequency(hz)
    time.sleep(speed)

  for hz in range(1000, 440, -1):
    p.ChangeFrequency(hz)
    time.sleep(speed)

  p.stop()

def ring_alarm(numtimes=3):
  for i in range(0, numtimes):
    whooze()
