#!/usr/bin/python
from imgs import *
from settings import *

import time
import math
import subprocess
import collections

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

N=8 # 8x8 matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

def map_range( a, b, s):
  (a1, a2), (b1, b2) = a, b
  mapped = b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
  return min(max(mapped, 0), b2)

def print_stacks(cnt):
  if (cnt == 0):
    device.clear()
    return
  with canvas(device) as draw:
    draw.rectangle((0,N-cnt,N-1,N-1), outline="white", fill="white")    
    intensity=map_range((0,N-1),(0,255), cnt)
    device.contrast(intensity)

def print_matrix(img):
  mat=zip(*img) #Rotate 90 degrees
  with canvas(device) as draw:
    for i in range(len(mat)):
      for j in range(len(mat[i])):
        if mat[i][j] == 1:
            draw.point((i,j), fill="white")

def blink(fun, arg, times=1, delay=2.0):
  for i in range(times):
    fun(arg)
    time.sleep(delay)
    device.clear()
    time.sleep(delay)

def ring_alarm():
  print "ALARM ! ALARM ! ALARM !" 

def main():
  historyLength = 5 
  history = collections.deque(maxlen=historyLength)
  warning = False
  consecutiveWarnings = 0
  while True:
    #Probe room sound level
    print "Probing..."
    cmd = "arecord -q -d 1 -D hw:1,0 -r 44100 -f S16_LE | sox -t .wav - -n stats 2>&1 | awk '/RMS lev dB/{print 100 + $4}'"
    measuredDB = float(subprocess.check_output(cmd, shell=True))
    history.append(measuredDB)
    averageDB = sum(history) * 1.0 / len(history)
    level = int(map_range((min_db(),max_db()),(0,N-1), averageDB))

    print "Room current dB : %f, avg since %d samples : %f, level : %d" % (measuredDB, historyLength, averageDB, level)
    if not warning: 
      print_stacks(level)

    #Warning
    print "Average DB : %f, maxDB : %f" % (averageDB, max_db())
    if len(history) == historyLength and averageDB > max_db():
      warning = True
      if warn_is_enabled():
        blink(print_matrix, warn_8x8, 10, 0.1)
      consecutiveWarnings += 1
      if consecutiveWarnings > 5 and alarm_is_enabled:
        ring_alarm()
    else:
      warning = False
      consecutiveWarnings = 0
      time.sleep(1)

if __name__ == "__main__":
    main()
