#!/bin/bash

arecord -d 10 -D hw:1,0 -r 44100 -f S16_LE sample.wav
