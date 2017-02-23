import requests
import time

class Rover:
    def __init__(self, ip):
        self.ip = ip

    def drive(self, speed):
        r = requests.put('http://%s/drive/speed/%d' % (self.ip, speed))

    def pivot(self, speed):
        r = requests.put('http://%s/drive/pivot/%d' % (self.ip, speed))


class TestRoverWheels:
    def __init__(self, serial):
        self.rover = Rover(IP)

    def forwards(self, drive_time):
        rover.drive(1)
        time.sleep(drive_time)
        rover.drive(0)

    def backwards(self, drive_time):
        rover.drive(-1)
        time.sleep(drive_time)
        rover.drive(0)

if __name__ == '__main__':
    IP = 'localhost:8080'
    rover = Rover(IP)
    rover.drive(1)
    time.sleep(1)
    rover.drive(0)