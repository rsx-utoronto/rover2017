import requests
import time


IP = 'localhost:8080'

class Rover:
    def __init__(self, ip):
        self.ip = ip

    def drive(speed):
        r = requests.put('http://%s/drive/speed/%f' % (self.ip, speed))

    def pivot(speed):
        r = requests.put('http://%s/drive/pivot/%f' % (self.ip, speed))


class TestRoverWheels:
    def __init__(self, serial):
        self.rover = Rover(IP)

    def forwards(drive_time):
        rover.drive(1)
        time.sleep(drive_time)
        rover.drive(0)

    def backwards(drive_time):
        rover.drive(-1)
        time.sleep(drive_time)
        rover.drive(0)

if __name__ == '__main__':
    rover = Rover(IP)
    rover.drive(1)
    time.sleep(1)
    rover.drive(0)