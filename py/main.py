#!/usr/bin/env python3

import sys
import requests
from math import pi
u = 'http://192.168.1.10:5000/api/Rover05'
#u = 'http://192.168.1.11:5000/api/elcaduck'

L = 10
WHITE, GREY, BLACK = 0, 1, 2
g_n = 10
g_step = 0.1
g = [ ]
for i in range(g_n):
    g.append(g_n * [WHITE])
g_spacing = 2.0*L/g_n

def xy2grid(x, y):
    n = g_n
    x = n*x/(2.0*L) + n/2.0
    y = n*y/(2.0*L) + n/2.0
    x = int(x)
    y = int(y)
    if x < 0 or x >= n:
        return None, None
    if y < 0 or y >= n:
        return None, None
    return int(x), int(y)

def g_update(x, y, ang, lat):
    print(ang, lat)

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
    r = requests.get(s, p)
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

x, y = 0, 0
print(gps())
rotate(1, 'right', 1)
#g_update(x, y, ang)
#print(inc)
#print(inten)
#print(g)
