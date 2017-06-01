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
    print(out)
    return out


def getJoystickButtons():
    pygame.event.pump()
    
    buttons = []
    for i in range(0, joystick.get_numbuttons()):
        button = joystick.get_button(i)
        buttons.append(button)
    print(buttons)
    return buttons


if __name__ == "__main__":
    initializeJoystick()

    while True:
        getJoystickAxes()
        getJoystickButtons()
        time.sleep(0.5)
    
