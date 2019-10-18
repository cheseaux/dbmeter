#!/usr/bin/python
import errno
import os
import subprocess
from multiprocessing import Process

import RPi.GPIO as GPIO
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

from alarm import *
from imgs import *

N = 8  # 8x8 led matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

log_file_name = "logs/sound-level-{}.csv".format(int(round(time.time() * 1000)))

max_consecutive_warnings = 3

noisy_threshold = 48
super_noisy_threshold = 52

noisy_increment = 2
super_noisy_increment = 3
silence_decrement = 1

overall_max_noise_level = 24  # = 8 seconds super noisy or 24 seconds noisy

def create_log_file():
    if not os.path.exists(os.path.dirname(log_file_name)):
        try:
            os.makedirs(os.path.dirname(log_file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def boot_animation():
    for i in range(0, N / 2):
        with canvas(device) as draw:
            draw.rectangle((N - i - 1, i, i, N - i - 1), outline="white", fill="white")
        time.sleep(0.5)
    device.clear()


def print_stacks(cnt):
    if cnt <= 0:
        device.clear()
    else:
        with canvas(device) as draw:
            draw.rectangle((0, N - cnt, N - 1, N - 1), outline="white", fill="white")


def print_img(img):
    mat = zip(*img)  # Rotate 90 degrees
    with canvas(device) as draw:
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if mat[i][j] == 1:
                    draw.point((i, j), fill="white")


def blink(fun, arg, times=1, delay=2.0):
    for i in range(times):
        fun(arg)
        time.sleep(delay)
        device.clear()
        time.sleep(delay)


def alarm():
    p_ring = Process(target=ring_alarm)
    p_blink = Process(target=blink, args=(print_img, cross_8x8, 15, 0.1))
    p_blink.start()
    p_ring.start()
    p_ring.join()
    p_blink.join()


def save_to_csv(level):
    with open(log_file_name, "a") as f:
        f.write(str(int(time.time())) + "," + str(level) + "\n")


def is_super_noisy():
    return is_noisy(super_noisy_threshold)


def is_noisy(threshold=noisy_threshold):
    print "Probing..."
    cmd = "arecord -q -d 1 -D hw:1,0 -r 44100 -f S16_LE | sox -t .wav - -n stats 2>&1 | awk '/RMS lev dB/{print 100 + $4}'"
    measured_db = float(subprocess.check_output(cmd, shell=True))
    print "Current room level (db) : %f" % measured_db
    save_to_csv(measured_db)
    return measured_db > threshold


def main():
    boot_animation()
    noise_level = 0
    create_log_file()
    is_warning = False
    consecutive_warnings = 0
    while True:
        if is_super_noisy():
            print "Super noisy, increment %d" % super_noisy_increment
            noise_level = min(overall_max_noise_level, noise_level + super_noisy_increment)
        elif is_noisy():
            print "Noisy, increment %s" % noisy_increment
            noise_level = min(overall_max_noise_level, noise_level + noisy_increment)
        else:
            noise_level = max(0, noise_level - silence_decrement)

        print "Current noise level : %d/%d" % (noise_level, overall_max_noise_level)

        if not is_warning:
            stack_count = noise_level * N / overall_max_noise_level
            print "Stack to display : %d" % stack_count
            print_stacks(stack_count)

        if noise_level >= overall_max_noise_level:
            is_warning = True
            blink(print_img, warn_8x8, 10, 0.1)
            consecutive_warnings += 1
            print "consecutive warnings %d" % consecutive_warnings
            if consecutive_warnings >= max_consecutive_warnings:
                alarm()
                consecutive_warnings = 0
                is_warning = False
        else:
            is_warning = False
            consecutive_warnings = 0


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.output(27, False)  # disable buzzer in case program crash / keyboard interrupt
        GPIO.cleanup()
