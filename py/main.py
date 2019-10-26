#!/usr/bin/env python3

import sys
import requests
u = 'http://192.168.1.11:5000/api/Rover05'

def msg(s):
    sys.stderr.write(s)

def err(s):
    sys.stderr.write(s)
    exit(2)

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

#backward(0.5, 0.4)
#forward(0.5, 0.4)
#status = led()
# rotate(1, 'left', 0.1)
stop()
