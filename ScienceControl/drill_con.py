#! /usr/bin/env python
# imports
import time
import pygame
import math
import httplib
import sys

BLACK = (0, 0, 0)

pygame.init()
size = [200, 200]
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(0)
screen.fill(BLACK)


def send_movement(speeds):
    message = 'm'
    for speed in speeds:
        message += "%20" + str(int(speed))
    print message
    sendMessage(message)


def sendMessage(message):
    global conn
    conn.request("PUT", "/arm/" + message + "/")
    conn.close()


sendSpeeds = [0, 0, 0, 0, 0, 0, 0]
speed = 50

def process_keyboard():
    global sendSpeeds
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sendSpeeds[3] += speed
            if event.key == pygame.K_DOWN:
                sendSpeeds[3] -= speed
            if event.key == pygame.K_RIGHT:
                sendSpeeds[1] -= speed
            if event.key == pygame.K_LEFT:
                sendSpeeds[1] += speed
            if event.key == pygame.K_1:
                speed = 25
            if event.key == pygame.K_2:
                speed = 50
            if event.key == pygame.K_3:
                speed = 75
            if event.key == pygame.K_4:
                speed = 100
            if event.key == pygame.K_5:
                speed = 125
            if event.key == pygame.K_6:
                speed = 150
            if event.key == pygame.K_7:
                speed = 175
            if event.key == pygame.K_8:
                speed = 200
            if event.key == pygame.K_9:
                speed = 225
            if event.key == pygame.K_0:
                speed = 255
            if event.key == pygame.K_SPACE:
                sendSpeeds = [0, 0, 0, 0, 0, 0, 0]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                sendSpeeds[3] -= speed
            if event.key == pygame.K_DOWN:
                sendSpeeds[3] += speed
            if event.key == pygame.K_RIGHT:
                sendSpeeds[1] += speed
            if event.key == pygame.K_LEFT:
                sendSpeeds[1] -= speed
    send_movement(sendSpeeds)


def main():
    global conn
    serverIP = '192.168.0.3'
    serverHttpPort = '8080'
    conn = httplib.HTTPConnection(serverIP+":"+serverHttpPort)
    while True:
        process_keyboard()
        time.sleep(0.02)


if __name__ == "__main__":
    main()
