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
# - >   : long, x (+)
#
# '''
    def __init__(self, tick, errorx, errory, server):
        #The time at the start
        self.tick = tick
        #Time when the operation is stopped
        self.stopTime = 300
        #Server location. Alternative location: "100.64.104.140:8080"
        self.serverLocation = server

        self.xError = errorx

        self.yError = errory

        self.speed = 70

        self.timeOut = False

        self.arrived = False

    def get_gps_coordinate(self):
        # Get current GPS coordinate
        conn = http.client.HTTPConnection(self.serverLocation)
        conn.request("GET", "/gps")
        r_gps = conn.getresponse()
        gps_string = r_gps.read().decode('utf-8')
        json_gps = json.loads(gps_string)
        head = float(json_gps["heading"])  # CW positive
        return (json_gps, head)

    def straight_line_path_planning(self, target, json_gps):
        targetX = target[0]
        targetY = target[1]

        x = targetX - json_gps["longitude"]
        y = targetY - json_gps["latitude"]

        print ("Longitude")
        print (json_gps["longitude"])
        print ("Latitude")
        print (json_gps["latitude"])

        if (abs(x) < self.xError and abs(y) < self.yError):
            print ("Destination reached")
            self.Arrived = True
            return 0

        target_angle = math.degrees(math.atan2(y,x))


        #Heading starts from north. Clockwise is positive and CounterClockwise is negative.
        #Make it start from east, because the target_angle starts from angle 0 (east).
        correctHeading = -1 * (head - 90)
        angle_from_rover = correctHeading - target_angle

        #For angles to destination higher than 180, turn the other way, because it's faster.
        if (angle_from_rover >= 180):
            angle_from_rover = -1*(360 - angle_from_rover)
        elif (angle_from_rover <= -180):
            angle_from_rover = (360 - abs(angle_from_rover))

        print("Head: ")
        print(correctHeading)
        print("target_angle: ")
        print(target_angle)
        print("angle from rover: ")
        print(angle_from_rover)

        return (angle_from_rover, x, y)

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

        (json_gps, head) = self.get_gps_coordinate()

        targetX = coordinate[0]
        targetY = coordinate[1]

        x = targetX - json_gps["longitude"]
        y = targetY - json_gps["latitude"]

        with open("position.kml", "w",) as pos:
            pos.write("""<kml xmlns="http://www.opengis.net/kml/2.2"
 xmlns:gx="http://www.google.com/kml/ext/2.2"><Placemark>
  <name>Live GPS from Python</name>
  <description>Live Description</description>
  <Point>
    <coordinates>%s,%s,0</coordinates>
  </Point>
</Placemark></kml>""" % (json_gps["longitude"], json_gps["latitude"]))

        print ("Longitude, latittude")
        print (json_gps["latitude"])
        print (json_gps["longitude"])

        print ("xDifferential" + str(x))
        print ("yDifferential" + str(y))

        if (abs(x) < self.xError and abs(y) < self.yError):
            print ("Destination reached")
            self.Arrived = True
            return True

        target_angle = math.degrees(math.atan2(y, x))
        if (target_angle < 0):
            target_angle = 360 + target_angle

        #Sometimes the head values are messed up.
        if(head > 180):
            head = -1 * (360 - head)
        elif(head < -180):
            head = 360 + head

        # Heading starts from north. Clockwise is positive and CounterClockwise is negative.
        # Change it to unit circle degree measurement
        if (head <= 0):
            refinedHead = abs(head) + 90
        elif(head <= 90):
            refinedHead = head - 90
        elif(head > 90):
            refinedHead = 360 - (head - 90)

        angle_from_rover = refinedHead - target_angle

        # For angles to destination higher than 180, turn the other way, because it's faster.
        if (angle_from_rover >= 180):
            angle_from_rover = -1 * (360 - angle_from_rover)
        elif (angle_from_rover <= -180):
            angle_from_rover = (360 - abs(angle_from_rover))

        print("Head: ")
        print(head)
        print("target_angle: ")
        print(target_angle)
        print("angle from rover: ")
        print(angle_from_rover)

        self.motor_controller(angle_from_rover, x, y)
        return False

    def motor_controller(self, angle_from_rover, x, y):
        if angle_from_rover >= 0:
            #Turn right
            if angle_from_rover < 85:
                #Turn appropriately: higher the angle, bigger the turn (right speed decreases)
                left_speed = self.speed
                right_speed = self.speed * abs(math.cos(math.radians(abs(angle_from_rover))))
            elif angle_from_rover > 95:
                #Backwards
                angle_from_rover = 180 - angle_from_rover
                left_speed = -self.speed
                right_speed = -self.speed * abs(math.cos(math.radians(abs(angle_from_rover))))
            else:
                left_speed = self.speed
                right_speed = 0
        else:
            #Turn left
            if abs(angle_from_rover) < 85:
                left_speed = self.speed * abs(math.cos(math.radians(abs(angle_from_rover))))
                right_speed = self.speed
            elif abs(angle_from_rover) > 95:
                #Backwards
                angle_from_rover = 180 - abs(angle_from_rover)
                left_speed = -self.speed * abs(math.cos(math.radians(abs(angle_from_rover))))
                right_speed = -self.speed
            else:
                left_speed = 0
                right_speed = self.speed

        #print("Left speed")
        print(left_speed)
        #print("Right speed")
        print(right_speed)

        conn = http.client.HTTPConnection(self.serverLocation)
        #conn.request("PUT", "/drive/stop")

        conn.request("PUT", "/drive/speed/" + str(left_speed) + "/" + str(right_speed))
        #time.sleep()

