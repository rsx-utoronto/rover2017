import http.client
import time
from datetime import datetime
import json
import math

stop_time = 300
speed = 20
targetX = -79.38721  #long
targetY = 43.70442   #lat
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
while True:
    tock = datetime.now()
    diff = tock - tick
    if diff.total_seconds() > 300:
        break
    #conn = http.client.HTTPConnection("100.64.104.140:8080")
    conn = http.client.HTTPConnection("localhost:8080")
    conn.request("GET", "/gps")
    r_gps = conn.getresponse()
    gps_string = r_gps.read().decode('utf-8')
    json_gps = json.loads(gps_string)
    head = float(json_gps["heading"])  # CW positive

    x = targetX - json_gps["longitude"]
    y = targetY - json_gps["latitude"]
    
    if abs(x) < 0.001 and abs(y) < 0.001:
        print ("Destination reached")
        break
    '''
    print("Lon,Lat")
    print(json_gps["longitude"], json_gps["latitude"])
    print("")
    
    print("distancex,distancey")
    print(x,y)
    '''
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
    print("head:")
    print(head)
    print("angle:")
    print(angle)
    if angle >= 0:
        #move right
            #Turn appropriately: higher the angle, bigger the turn (left speed increases)
        left_speed = speed
        right_speed = speed * math.cos(angle)

    if angle < 0:
        #move left
        left_speed = speed * math.cos(abs(angle))
        right_speed = speed

    #conn = http.client.HTTPConnection("100.64.104.140:8080")
    conn = http.client.HTTPConnection("localhost:8080")
    conn.request("PUT", "/drive/speed/" + str(left_speed) + "/" + str(right_speed))
    time.sleep(1/speed)
    
    '''
    print(left_speed)
    print(right_speed)
    '''
#conn = http.client.HTTPConnection("100.64.104.140:8080")
conn = http.client.HTTPConnection("localhost:8080")
conn.request("PUT", "/drive/stop")



