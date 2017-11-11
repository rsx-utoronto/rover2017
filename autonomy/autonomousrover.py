import http.client
import time
from datetime import datetime
import json
import math

class AutonomousRover:
# '''
#         North
#         |
#        ---
#         |
# ^
# |   : lat, y (+)
#
# <-  : long, x (+)
#
# '''
    def __init__(self, tick, x, y, server):
        #The time at the start
        self.tick = tick
        #Time when the operation is stopped
        self.stopTime = 300
        #Server location. Alternative location: "100.64.104.140:8080"
        self.serverLocation = server

        self.xError = x

        self.yError = y

        self.speed = 100

        self.timeOut = False

    def move_towards_gps_Location(self, coordinate):
        '''
        Move towards the goal GPS location
        :return: whether the rover arrived at a location or not.
        '''

        #If time expired, quit.
        tock = datetime.now()
        diff = tock - self.tick
        if diff.total_seconds() > self.stopTime:
            self.timeOut = True
            return False

        #Get current GPS coordinate
        conn = http.client.HTTPConnection(self.serverLocation)
        conn.request("GET", "/gps")
        r_gps = conn.getresponse()
        gps_string = r_gps.read().decode('utf-8')
        json_gps = json.loads(gps_string)
        head = float(json_gps["heading"])  # CW positive

        targetX = coordinate[0]
        targetY = coordinate[1]

        #Longitude increases towards the west. For easy calculation, it should increase towards the east.
        x = (targetY - json_gps["longitude"]) * -1
        y = targetX - json_gps["latitude"]

        print (json_gps["longitude"])
        print (json_gps["latitude"])

        if (abs(x) < self.xError and abs(y) < self.yError):
            print ("Destination reached")
            return True

        target_angle = -math.degrees(math.atan2(x,y))

        angle_from_rover = target_angle - head

        #For angles to destination higher than 180, turn the other way
        if (angle_from_rover >= 180):
            angle_from_rover = -1*(360 - angle_from_rover)
        elif (angle_from_rover <= -180):
            angle_from_rover = (360 - abs(angle_from_rover))

        print("Head: ")
        print(head)
        print("target_angle: ")
        print(target_angle)
        print("angle from rover")
        print(angle_from_rover)

        if angle_from_rover >= 0:
            #move right
            if angle_from_rover <= 90:
                #Turn appropriately: higher the angle, bigger the turn (left speed increases)
                left_speed = self.speed
                right_speed = self.speed * abs(math.cos(math.radians(abs(angle_from_rover))))
            elif angle_from_rover <= 180:
                left_speed = self.speed
                right_speed = 0
            else:
            #Just in case
                left_speed = 0
                right_speed = 0
        else:
            #move left
            if abs(angle_from_rover) <= 90:
                left_speed = self.speed * abs(math.cos(math.radians(abs(angle_from_rover))))
                right_speed = self.speed
            elif abs(angle_from_rover) <= 180:
                left_speed = 0
                right_speed = self.speed
            else:
                left_speed = 0
                right_speed = 0

        #print("Left speed")
        print(left_speed)
        #print("Right speed")
        print(right_speed)

        conn = http.client.HTTPConnection(self.serverLocation)
        conn.request("PUT", "/drive/speed/" + str(left_speed) + "/" + str(right_speed))
        time.sleep(1/self.speed)

        return False

