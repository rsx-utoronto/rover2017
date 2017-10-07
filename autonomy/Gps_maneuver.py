import http.client
import time
from datetime import datetime
import json
import math

stop_time = 300
speed = 50
targetX = -78  #long
targetY = 42.5   #lat
x = 0
y = 0
tick = datetime.now()

'''
        North
        |
       ---
        |
^
|   : lat, y (+)

<-  : long, x (+)

'''
while targetX != x and targetY != y:
    tock = datetime.now()
    diff = tock - tick
    if diff.total_seconds() > 300:
        break
    conn = http.client.HTTPConnection("localhost:8080")
    conn.request("GET", "/gps")
    r_gps = conn.getresponse()
    gps_string = r_gps.read().decode('utf-8')
    json_gps = json.loads(gps_string)
    head = float(json_gps["head"])  # CW positive

    x = target_lon - json_gps["lon"]
    y = target_lat - json_gps["lat"]
    
    print("Lon,Lat")
    print(json_gps["lon"], json_gps["lat"])
    print("")
    print("distancex,distancey")
    print(x,y)

    if x > 0 and y > 0:
        target_angle = -math.degrees(math.atan(abs(x) / abs(y)))
    elif x > 0 and y <= 0:
        target_angle = -90 - math.degrees(math.atan(abs(y) / abs(x)))
    elif x <= 0 and y > 0:
        target_angle = math.degrees(math.atan(abs(x) / abs(y)))
    elif x <= 0 and y <= 0:
        target_angle = 90 + math.degrees(math.atan(abs(y) / abs(x)))

    #Move to the goal
    angle = target_angle - head
    if angle >= 0:
        #move right
        if angle <= 90:
            #Turn appropriately: higher the angle, bigger the turn (left speed increases)
            left_speed = speed * math.sin(angle)
            right_speed = speed * math.cos(angle)
        elif angle > 90:
            opp_angle = 180 - angle
            #Same thing but backwards
            left_speed = -speed * math.sin(opp_angle)
            right_speed = -speed * math.cos(opp_angle)
    if angle < 0:
        #move left
        if abs(angle) <= 90:
            left_speed = speed * math.cos(abs(angle))
            right_speed = speed * math.sin(abs(angle))
        elif abs(angle) > 90:
            opp_angle = 180 - angle
            # Same thing but backwards
            left_speed = -speed * math.cos(opp_angle)
            right_speed = -speed * math.sin(opp_angle)

    conn = http.client.HTTPConnection("localhost:8080")
    conn.request("PUT", "/drive/speed/" + str(left_speed) + "/" + str(right_speed))
    time.sleep(1/speed)

conn = http.client.HTTPConnection("localhost:8080")
conn.request("PUT", "/drive/stop")



