#!/usr/bin/python
from imgs import *
from settings import *

import time
import math
import subprocess

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
    print "setting intensity %d" % intensity
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

'''
while True:
  #Probe room sound level
  cmd = "arecord -q -d 1 -D hw:1,0 -r 44100 -f S16_LE | sox -t .wav - -n stats 2>&1 | awk '/RMS lev dB/{print 100 + $4}'"
  output = subprocess.check_output(cmd, shell=True)
  print "room sound level : ", output
  level = int(map_range((minDB,maxDB),(0,N-1), float(output)))
  print "range : ", level
  print_stacks(level)
'''
