#!/usr/bin/python
from imgs import *
from alarm import *
from multiprocessing import Process
from numpy import mean

import time
import os
import math
import subprocess
import collections

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

N=8 # 8x8 led matrix
maxConsecutiveWarnings=2
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

dbThreshold=47
historyFilePath = "/home/pi/sound-meter-project/sound-level.csv"


def map_range( a, b, s):
  (a1, a2), (b1, b2) = a, b
  mapped = b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
  return min(max(mapped, 0), b2)

def db_to_lin(db):
  return math.pow(db/10.0,10)

def map_range_db( a, b, s):
  (a0,a1) = a
  a0Lin = db_to_lin(a0)
  a1Lin = db_to_lin(a1)
  return map_range((a0Lin,a1Lin), b, db_to_lin(s))

def print_stacks(cnt):
  if (cnt == 0):
    device.clear()
    return
  with canvas(device) as draw:
    draw.rectangle((0,N-cnt,N-1,N-1), outline="white", fill="white")    
    intensity=map_range((0,N-1),(0,255), cnt)
    device.contrast(intensity)

def print_img(img):
  mat=zip(*img) #Rotate 90 degrees
  with canvas(device) as draw:
    for i in range(len(mat)):
      for j in range(len(mat[i])):
        if mat[i][j] == 1:
            draw.point((i,j), fill="white")

def blink(fun, arg, times=1, delay=2.0, intensity=255):
  for i in range(times):
    device.contrast(intensity)
    fun(arg)
    time.sleep(delay)
    device.clear()
    time.sleep(delay)

def alarm():
  p_ring = Process(target=ring_alarm)
  p_blink = Process(target=blink, args=(print_img, cross_8x8, 15, 0.1, 255))
  p_blink.start()
  p_ring.start()
  p_ring.join()
  p_blink.join()

def delete_history_file():
  open(historyFilePath, 'w').close()
  if os.path.exists(historyFilePath):
    os.remove(historyFilePath)

def save_to_csv(level):
  with open(historyFilePath, "a") as f:
    f.write(str(int(time.time())) + "," + str(level) + "\n")


def is_currently_loud():
    print "Probing..."
    cmd = "arecord -q -d 1 -D hw:1,0 -r 44100 -f S16_LE | sox -t .wav - -n stats 2>&1 | awk '/RMS lev dB/{print 100 + $4}'"
    measuredDB = float(subprocess.check_output(cmd, shell=True))
    save_to_csv(measuredDB)
    print "Room current dB : %f" % measuredDB
    return measuredDB > dbThreshold

def main():
  loudnessCountThreshold=30
  loudnessCount=0
  silenceCount=0

  blink(print_img, boot_8x8, 3, 0.5, 255)
  delete_history_file()
  warning = False
  consecutiveWarnings = 0
  while True:
    if is_currently_loud():
      loudnessCount += 1 
    else:
      silenceCount += 1
      if silenceCount > 5:
        loudnessCount = max(loudnessCount-1, 0)
        silenceCount = 0

    level = map_range((0, N-1), (0, loudnessCountThreshold), loudnessCount)

    print "Loudness : %f, Silence : %f, level : %f" % (loudnessCount, silenceCount, level)

    if not warning: 
      print_stacks(level)

    if loudnessCount >= loudnessCountThreshold:
      warning = True
      blink(print_img, warn_8x8, 10, 0.1, 255)
      consecutiveWarnings += 1
      print "consecutive warnings %d" % consecutiveWarnings 
      if consecutiveWarnings >= maxConsecutiveWarnings: 
        alarm()
        consecutiveWarnings=0
        warning = False
    else:
      warning = False
      consecutiveWarnings = 0

if __name__ == "__main__":
    main()
