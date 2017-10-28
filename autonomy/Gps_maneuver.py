import http.client
import time
from datetime import datetime
import json
import math
from autonomousrover import *


if __name__ == '__main__':
    markers = [( -79.40268609235008, 43.665374242896135),(-79.40313654280052, 43.664923792445684), (-79.40283789434407, 43.664950484257666)]
    x = 0.00001
    y = 0.00001
    # Server location. Alternative location: "100.64.104.140:8080"

    server = "localhost:8080"
    rover = AutonomousRover(datetime.now(), x, y, server)
    for marker in markers:
        arrived_at_destination = False
        while(not arrived_at_destination):
            arrived_at_destination = rover.move_towards_gps_Location(marker)

        for i in range(10):
            print("Arrived at the Destination")

        conn = http.client.HTTPConnection(server)
        conn.request("PUT", "/drive/stop")

# stop_time = 300
# speed = 50
# count = 0
# # targetX = -79.38721  #long
# # targetY = 43.70442   #lat
#
# # right beside the doorway
# # targetX = -79.40283789434407
# # targetY = 43.664950484257666
#
# # away from the doorway
# targetX = -79.40313654280052
# targetY = 43.664923792445684
#
# x = 0
# y = 0
# tick = datetime.now()
#

# while True:
#     tock = datetime.now()
#     diff = tock - tick
#     if diff.total_seconds() > 300:
#         break
#     #conn = http.client.HTTPConnection("100.64.104.140:8080")
#     conn = http.client.HTTPConnection("localhost:8080")
#     conn.request("GET", "/gps")
#     r_gps = conn.getresponse()
#     gps_string = r_gps.read().decode('utf-8')
#     json_gps = json.loads(gps_string)
#     head = float(json_gps["heading"])  # CW positive
#
#     x = targetX - json_gps["longitude"]
#     y = targetY - json_gps["latitude"]
#
#     if abs(x) < 0.000001 and abs(y) < 0.000001:
#         print ("Destination reached")
#         break
#     '''
#     print("Lon,Lat")
#     print(json_gps["longitude"], json_gps["latitude"])
#     print("")
#
#     print("distancex,distancey")
#     print(x,y)
#     '''
#     if x > 0 and y > 0:
#         target_angle = -math.degrees(math.atan(abs(x) / abs(y)))
#     elif x > 0 and y <= 0:
#         target_angle = -90 - math.degrees(math.atan(abs(y) / abs(x)))
#     elif x <= 0 and y > 0:
#         target_angle = math.degrees(math.atan(abs(x) / abs(y)))
#     elif x <= 0 and y <= 0:
#         target_angle = 90 + math.degrees(math.atan(abs(y) / abs(x)))
#
#     #Move to the goal
#     angle = target_angle - head
#     count += 1
#     if count == 0:
#         print("target_angle")
#         print(target_angle)
#
#     print("head:")
#     print(head)
#     print("angle:")
#     print(angle)
#     if angle >= 0:
#         #move right
#         if angle <= 90:
#             #Turn appropriately: higher the angle, bigger the turn (left speed increases)
#             left_speed = speed
#             right_speed = speed * abs(math.cos(abs(angle)))
#         elif angle < 180:
#             left_speed = speed
#             right_speed = 0
#         else:
#             left_speed = 0
#             right_speed = 0
#

#    else:
#         #move left
#         if abs(angle) <= 90:
#             left_speed = speed * abs(math.cos(abs(angle)))
#             right_speed = speed
#         elif abs(angle) < 180:
#             left_speed = 0
#             right_speed = speed
#         else:
#             left_speed = 0
#             right_speed = 0
#
#     #conn = http.client.HTTPConnection("100.64.104.140:8080")
#     #conn = http.client.HTTPConnection("localhost:8080")
#     #conn.request("PUT", "/drive/speed/" + str(left_speed) + "/" + str(right_speed))
#     time.sleep(1/speed)
#
#     print("Left speed")
#     print(left_speed)
#     print("Right speed")
#     print(right_speed)
#
# #conn = http.client.HTTPConnection("100.64.104.140:8080")
# conn = http.client.HTTPConnection("localhost:8080")
# conn.request("PUT", "/drive/stop")



