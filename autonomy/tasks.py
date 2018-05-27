import http.client
import time
from datetime import datetime
import json
import math

class Task:

    def __init__(self):
        pass

    def taskone(self):
        '''
        No CV, just maneuvers the rover to the destination using the gps coordinates.
        Teleoperation is allowed
        :return:
        '''
        # The Destination
        markers = [(-79.46504954954956, 43.78235045045045)]
        x = 0.00005
        y = 0.00005
        # Server location. Alternative location: "100.64.104.140:8080"

        server = "localhost:8080"
        rover = AutonomousRover(datetime.now(), x, y, server)
        for marker in markers:
            arrived_at_destination = False
            while (not arrived_at_destination):
                arrived_at_destination = rover.move_towards_gps_Location(marker)
                if rover.timeOut == True:
                    for i in range(10):
                        print("Timout occured")
                    break

            if not rover.timeOut:
                for i in range(10):
                    print("Arrived at the Destination")
            else:
                break

            conn = http.client.HTTPConnection(server)
            conn.request("PUT", "/drive/stop")

        conn = http.client.HTTPConnection(server)
        conn.request("PUT", "/drive/stop")

    def tasktwo(self):
        '''
        GPS Maneuver to begin with and then use CV to detect the tennis ball.
        Teleoperation is allowed
        :return:
        '''
        taskone()
