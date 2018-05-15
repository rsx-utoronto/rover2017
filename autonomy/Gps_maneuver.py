import http.client
import time
from datetime import datetime
import json
import math
from autonomousrover import *


def get_gps_coordinate(server):
    # The Destinations: (longitude, latitude)
    destination_markers = [(-79.403573, 43.664939)]
    #near the fence: -79.403450, 43.664741

    xError = 0.00005
    yError = 0.00005

    rover = AutonomousRover(datetime.now(), xError, yError, server)
    for marker in destination_markers:
        arrived_at_destination = False
        while (not arrived_at_destination):
            arrived_at_destination = rover.move_towards_gps_Location(marker)
            if rover.timeOut == True:
                for i in range(10):
                    print ("Timout occured")
                break

        if not rover.timeOut:
            for i in range(10):
                print("Arrived at the Destination")

                # Start searching for the ball.

        else:
            break

        conn = http.client.HTTPConnection(server)
        conn.request("PUT", "/drive/stop")


if __name__ == '__main__':
    # 0.000020 -> 10 metre, 0.000005 -> 2 metre,
    # 0.000375 -> 40 metre, 0.000094 -> 10metre, 0.000019 -> 2metre,
    # Server location. Alternative location: "100.64.104.140:8080"
    server = "192.168.0.3:8080"

    get_gps_coordinate(server)

    conn = http.client.HTTPConnection(server)
    conn.request("PUT", "/drive/stop")



