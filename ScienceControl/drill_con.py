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


def process_keyboard():
    global sendSpeeds
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sendSpeeds[0] += 255
            if event.key == pygame.K_DOWN:
                sendSpeeds[1] += 255
            if event.key == pygame.K_RIGHT:
                sendSpeeds[2] += 255
            if event.key == pygame.K_LEFT:
                sendSpeeds[3] += 255
            if event.key == pygame.K_SPACE:
                sendSpeeds = [0, 0, 0, 0, 0, 0, 0]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                sendSpeeds[0] -= 255
            if event.key == pygame.K_DOWN:
                sendSpeeds[2] -= 255
            if event.key == pygame.K_RIGHT:
                sendSpeeds[1] -= 255
            if event.key == pygame.K_LEFT:
                sendSpeeds[3] -= 255
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
