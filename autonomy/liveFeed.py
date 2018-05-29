import http.client
import time
from datetime import datetime
import json
import math
from autonomousrover import *
#Near the door of 706:
# ( 43.66240274816083, -79.40235660050674)
#Away from the door 706:
# ( 43.6646403535148, -79.40212487711507)
#Tennis ball destination at the simulation
# ( -79.46504954954956, 43.78235045045045)

if __name__ == '__main__':
    conn = http.client.HTTPConnection("192.168.0.3:8080")
    while(True):
        # Get current GPS coordinate
        conn.request("GET", "/gps")

        r_gps = conn.getresponse()
        gps_string = r_gps.read().decode('utf-8')
        json_gps = json.loads(gps_string)
        head = json_gps["heading"]  # CW positive
        print("longitude: " + str(json_gps["longitude"]))
        print("latitude: " + str(json_gps["latitude"]))
        print("head: " + str(float(json_gps["heading"])))
        #print("pitch: " + str(float(json_gps["pitch"])))
