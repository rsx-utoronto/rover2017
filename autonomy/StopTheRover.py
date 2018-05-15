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
    #The Destinations: (longitude, latitude)
    destination_markers = [(- 79.4035726, 43.66493943)]
    #43.637139, -79.404111
    #43.664758, -79.403821

    xError = 0.00005
    yError = 0.00005
    #0.000020 -> 10 metre, 0.000005 -> 2 metre,
    #0.000375 -> 40 metre, 0.000094 -> 10metre, 0.000019 -> 2metre,
    # Server location. Alternative location: "100.64.104.140:8080"
    server = "192.168.0.3:8080"

    conn = http.client.HTTPConnection(server)
    #conn.request("PUT", "/drive/speed/" + "50" + "/" + "50")
    #conn.request("PUT", "/drive/stop")
    conn.request("PUT", "/drive/speed/" + str(0) + "/" + str(50))
