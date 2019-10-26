#!/usr/bin/env python3

import sys
import requests
from math import pi
#u = 'http://192.168.1.11:5000/api/Rover05'
u = 'http://192.168.1.11:5000/api/elcaduck'

def msg(s):
    sys.stderr.write(s)

def err(s):
    sys.stderr.write(s)
    exit(2)

def status():
    r = requests.get(u)
    return 0 if r.status_code == 200 else 1    

def backward(duration, power):
    s = u + '/' + 'backward'
    p = {'duration': duration, 'power': power}
    r = requests.get(s, p)
    return 0 if r.status_code == 200 else 1

def forward(duration, power):
    s = u + '/' + 'forward'
    p = {'duration': duration, 'power': power}
    r = requests.get(s, p)
    return 0 if r.status_code == 200 else 1

def led():
    s = u + '/' + 'led'
    r = requests.get(s)
    return 0 if r.status_code == 200 else 1

def rotate(duration, direction, power):
    if not direction in ['left', 'right']:
        msg("wrong direction '%s'" % direction)
        return 1
    s = u + '/' + 'rotate'
    p = {'duration': duration, 'direction': direction, 'power': power}
    r = requests.get(s)
    return 0 if r.status_code == 200 else 1

def stop():
    s = u + '/' + 'stop'
    r = requests.get(s)
    return 0 if r.status_code == 200 else 1

def gps():
    r = requests.get(u)
    r = r.json()
    x, y, rad = r['gps_x'], r['gps_y'], r['gps_orientation_rad']
    return x, y, rad

def angle():
    x, y, rad = gps()
    return rad

def xy():
    x, y, rad = gps()
    return x, y

def lidar():
    s = u + '/' + 'lidar'
    r = requests.get(s)
    stat = r.status_code
    r = r.json()
    i = r['angle_increment']
    r = r['intensities']
    return i, r

inc, inten = lidar()
print(inc)
print(inten)
