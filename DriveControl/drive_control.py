#! /usr/bin/env python
# imports
import copy
import time
import pygame
import math
import httplib
import sys

clock = pygame.time.Clock()

done = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

speed = 50
left = 0
right = 0


def init():
    pygame.init()
    size = [300, 200]
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(0)
    pygame.display.set_caption("RSX rover drive control")
    screen.fill(WHITE)
    print("pygame started, click the window")


def getJoystickAxes():
    out = []
    pygame.event.pump()
    for i in range(0, joystick.get_numaxes()):
        out.append(joystick.get_axis(i))
    return out


def sendMessage(message):
    global conn

    conn.request("PUT", "/drive/" + message + "/")
    conn.close()


def loop():
    global left, right, speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                left += speed
                right += speed
            elif event.key == pygame.K_DOWN:
                left -= speed
                right -= speed
            elif event.key == pygame.K_LEFT:
                left -= speed
                right += speed
            elif event.key == pygame.K_RIGHT:
                right -= speed
                left += speed
            elif event.key == pygame.K_SPACE:
                right = 0
                left = 0
            elif event.key == pygame.K_1:
                speed = 25
            elif event.key == pygame.K_2:
                speed = 50
            elif event.key == pygame.K_3:
                speed = 75
            elif event.key == pygame.K_4:
                speed = 100
            elif event.key == pygame.K_5:
                speed = 125
            elif event.key == pygame.K_6:
                speed = 150
            elif event.key == pygame.K_7:
                speed = 175
            elif event.key == pygame.K_8:
                speed = 200
            elif event.key == pygame.K_9:
                speed = 225
            elif event.key == pygame.K_0:
                speed = 255
            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                left -= speed
                right -= speed
            elif event.key == pygame.K_DOWN:
                left += speed
                right += speed
            elif event.key == pygame.K_LEFT:
                left += speed
                right -= speed
            elif event.key == pygame.K_RIGHT:
                right += speed
                left -= speed
            elif event.key == pygame.K_SPACE:
                right = 0
                left = 0
    command = 'n'
    # constrain values
    if (left >= 0):
        left_string = str(int(min(left, speed)))
    else:
        left_string = str(int(max(left, -speed)))
    if (right >= 0):
        right_string = str(int(min(right, speed)))
    else:
        right_string = str(int(max(right, -speed)))
    sendMessage(command + "%20" + left_string + "%20" + right_string)
    print(command + "%20" + left_string + "%20" + right_string)

if __name__ == "__main__":
    # serverIP = '192.168.0.3'
    serverIP = '192.168.1.177'
    serverHttpPort = '8080'
    global conn
    conn = httplib.HTTPConnection(serverIP+":"+serverHttpPort)

    init()
    while True:
        loop()
        clock.tick(15)
