import pygame
import time


def initializeJoystick():
    pygame.init()
    global joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print('Initialized joystick: %s' % joystick.get_name())


def getJoystickAxes():
    out = [0,0,0,0,0,0]
    it = 0 # iterator
    pygame.event.pump()
    #Read input from the joystick       
    for i in range(0, joystick.get_numaxes()):
        out[i] = joystick.get_axis(i)
    return out


if __name__ == "__main__":
    initializeJoystick()

    while True:
        print( getJoystickAxes() )
    
