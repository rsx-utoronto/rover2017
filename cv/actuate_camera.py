from urllib.request import urlopen
import time

class KaicongOutput():

    def __init__(self, domain, uri_format, user="admin", pwd="wavesharespotpear"):
        """ domain:   Camera IP address or web domain
                      (e.g. 385345.kaicong.info)
        """
        self.running = False
        self.uri = uri_format.format(domain, user, pwd)

class KaicongMotor(KaicongOutput):
    # These are the original state commands to send to the Kaicong camera.
    CMDLIST = {
        "PTZ_UP": 0,
        "PTZ_UP_STOP": 1,
        "PTZ_DOWN": 2,
        "PTZ_DOWN_STOP": 3,
        "PTZ_LEFT": 4,
        "PTZ_LEFT_STOP": 5,
        "PTZ_RIGHT": 6,
        "PTZ_RIGHT_STOP": 7,
        "PTZ_LEFT_UP": 90,
        "PTZ_RIGHT_UP": 91,
        "PTZ_LEFT_DOWN": 92,
        "PTZ_RIGHT_DOWN": 93,
        "PTZ_STOP": 1,
        "PTZ_CENTER": 25,
        "PTZ_VPATROL": 26,
        "PTZ_VPATROL_STOP": 27,
        "PTZ_HPATROL": 28,
        "PTZ_HPATROL_STOP": 29,
        "IO_ON": 94,  # TODO: What does this do?
        "IO_OFF": 95,  # and this one?
    }

    # This table converts a vector-style direction to its command
    MOVELIST = {
        "00": "PTZ_STOP",

        "0+": "PTZ_UP",
        "0-": "PTZ_DOWN",

        "+0": "PTZ_RIGHT",
        "-0": "PTZ_LEFT",

        "++": "PTZ_RIGHT_UP",
        "+-": "PTZ_RIGHT_DOWN",
        "-+": "PTZ_LEFT_UP",
        "--": "PTZ_LEFT_DOWN",
    }

    URI = "http://{0}:15213/decoder_control.cgi?&loginuse={1}&loginpas={2}&command=%d&onestep=0"

    def __init__(self, domain, user="admin", pwd="wavesharespotpear"):
        KaicongOutput.__init__(
            self,
            domain,
            KaicongMotor.URI,
            user,
            pwd
        )

        self.state = '00'

    def _to_symbol(self, v):
        if v > 0:
            return '+'
        if v < 0:
            return '-'
        else:
            return '0'

    def send_command(self, cmdstr):
        stream = urlopen(self.uri % (KaicongMotor.CMDLIST[cmdstr]), None, 1)
        print("Opening URL")
        result = stream.read()
        print("Finished reading stream")
        assert b"ok" in result
        stream.close()

    def move(self, xy):
        move_symbol = self._to_symbol(xy[0]) + self._to_symbol(xy[1])
        cmdstr = KaicongMotor.MOVELIST[move_symbol]
        if cmdstr != self.state:
            self.send_command(cmdstr)
        self.state = cmdstr


if __name__ == "__main__":
    import pygame
    import sys

    pygame.init()
    screen = pygame.display.set_mode((320, 240))
    domain = "192.168.0.101"
    motor = KaicongMotor(domain)

    def checkKeys():
        keys = pygame.key.get_pressed()
        print(keys)
        x = 0
        y = 0
        if keys[pygame.K_a]:
            x = -1
        if keys[pygame.K_s]:
            y = -1
        if keys[pygame.K_d]:
            x = 1
        if keys[pygame.K_w]:
            y = 1

        motor.move([x, y])

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        checkKeys()
