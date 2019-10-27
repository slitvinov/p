#!/usr/bin/env python3

from simple_pid import PID

import time
import sys
import cv2
import numpy as np
import requests
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('WX')


from math import pi, cos, sin, atan2, sqrt
#u = 'http://192.168.1.10:5000/api/Rover05'
u = 'http://192.168.1.164:5000/api/elcaduck'

L = 5
WHITE, GREY, BLACK, VISITED = 0, 1, 2, 3
def g_str(e):
    g_dict = {WHITE : 'white',
              GREY : 'grey',
              BLACK : 'black',
              VISITED : 'visited'}
    return g_dict[e]
g_n = 100
g_step = 0.1
g = [ ]
for i in range(g_n):
    g.append(g_n * [GREY])
g_spacing = 2.0*L/g_n

def g_clear():
    for i in range(g_n):
        for j in range(g_n):
            g[i][j] = GREY

def rad2deg(x):
    return 180*x/pi

def deg2rad(x):
    return pi*x/180

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

def g_write(path):
    with open(path, 'w') as f:
        for i in range(g_n):
            for j in range(g_n):
                if g[i][j] != GREY:
                    f.write("%d %d %s\n" % (i, j, g_str(g[i][j])))
def g_visit():
    x, y = xy()
    i, j = xy2grid(x, y)
    if i != None:
        g[i][j] = VISITED
    
def g_scan():
    x0, y0, rad0 = gps()
    inc, ran = lidar()
    ang = -pi - 0.5*inc
    sp = 0.01
    for r in ran:
        ang += inc
        if r == None:
            continue
        rad = rad0 + ang
        dx = sp*cos(rad)
        dy = sp*sin(rad)
        x, y, d = x0, y0, 0
        while True:
            i, j = xy2grid(x, y)
            if i == None:
                break
            elif d > r:
                g[i][j] = BLACK
                break
            elif g[i][j] != VISITED:
                g[i][j] = WHITE
                d += sp
                x += dx
                y += dy

def image2xy(path):
    r = cv2.imread(path)
    N = r.shape[0]
    M = r.shape[1]
    x = y = n = 0
    for i in range(N):
        for j in range(M):
            blue = r[i, j, 0]            
            red = r[i, j, 1]
            green = r[i, j, 2]
            if red > 180 and green > 180 and blue < 100:
                r[i, j, :] = 0
                x += j
                y += i
                n += 1
    cv2.imwrite("o.jpeg", r)
    return x/n, y/n

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

def image(path):
    s = u + '/' + 'image'
    r = requests.get(s)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)

def xy():
    x, y, rad = gps()
    return x, y

def lidar():
    s = u + '/' + 'lidar'
    r = requests.get(s)
    stat = r.status_code
    r = r.json()
    i = r['angle_increment']
    r = r['ranges']
    return i, r

def pbc(a, b):
    if abs(b + 2*pi - a) < abs(b - a):
        b += 2*pi
    if abs(b - 2*pi - a) < abs(b - a):
        b -= 2*pi
    return b - a

def rotate_to(b):
    for n in range(20):
        a = angle()
        d = pbc(a, b)
        if abs(d) < deg2rad(5):
            break
        elif abs(d) > deg2rad(90):
            control = 0.4
        elif abs(d) > deg2rad(10):
            control = 0.10
        else:
            control = 0.075
        direction = 'left' if d > 0 else 'right'
        rotate(control, direction, power = 1)
        time.sleep(0.5)

def a2b_angle(x, y, u, v):
    a = atan2(v - y, u - x)
    if a > pi:
        a -= 2*pi
    if a < -pi:
        a += 2*pi
    return a

def dist(x, y, u, v):
    dx = x - u
    dy = y - v
    return sqrt(dx*dx + dy*dy)

def forward_to(u, v):
    for n in range(100):
        x, y = xy()
        if dist(x, y, u, v) < 0.25:
            break
        ang = a2b_angle(x, y, u, v)
        rotate_to(ang)
        forward(0.5, power = 1)
        time.sleep(0.5)

#g_scan(); g_visit()
#plt.imshow(g)
#plt.show()

#print(image2xy("j.jpeg"))
#g_scan()
#g_write("p.txt")
#x, y = 0, 0
#print(gps())
#rotate(1, 'right', 1)
#g_update(x, y, ang)
#print(inc)
#print(inten)
#print(g)
