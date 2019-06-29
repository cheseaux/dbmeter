import RPi.GPIO as GPIO 
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT) 

GPIO.output(26, GPIO.HIGH)
sleep(.01)
GPIO.output(26, GPIO.LOW)
