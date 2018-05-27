import http.client
import time
from datetime import datetime
import json
import math
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from distance_calc_cv import find_distance_given_diameter
from angle_calc_cv import angle_cal
from ball_trackingrw import *
from autonomousrover import *

def move_towards_the_ball(server, destination_markers):

    xError = 0.00005
    yError = 0.00005
    headError = 10

    rover = AutonomousRover(datetime.now(), xError, yError, server)
    marker_number = 0
    for marker in destination_markers:
        time.sleep(5)
        marker_number += 1
        print("marker: " + str(marker_number))
        #arrived_at_destination = False
        #while (not arrived_at_destination):
        #    arrived_at_destination = rover.move_towards_gps_Location(marker)

        print("Arrived at the GPS Destination")
        # Start searching for the ball.

        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
                        help="max buffer size")
        args = vars(ap.parse_args())

        # if a video path was not supplied, grab the reference to the webcam
        if not args.get("video", False):
            # camera = cv2.VideoCapture(0)
            camera = cv2.VideoCapture(
                'http://192.168.0.101:15213/videostream.cgi?loginuse=admin&loginpas=wavesharespotpear')

        # otherwise, grab a reference to the video file
        else:
            camera = cv2.VideoCapture(args["video"])

        # ------- camera matrix comes from calibration algorithm from distance_calc_cv.py (find_intrinsic_matrix function)
        # or found in camera's doc ------------------
        # kmtx = np.load('C:/Users/rache/PycharmProjects/rsx/k_matrix.npy') #reading in the camera matrix from sally's iphone
        kmtx = np.load('v_matrix.npy')  # reading in the camera matrix, from the vesky camera
        calib_list = kmtx[0, 0], kmtx[1, 1], kmtx[0, 2], kmtx[1, 2]

        dis = 10000
        while(dis > DIST_FROM_TENNISBALL):
            print("Closing on the distance")
            while(True):
                (dis, ang, ball_found) = BallTrack(camera, args,calib_list)
                #Angle is from 0 to 53 degrees
                if (not ball_found):
                    print("looking for the rover")
                    left_speed = rover.speed
                    right_speed = 0
                else:
                    print("angle from the right edge: " + str(ang))
                    #desired angle reached
                    if (abs(ang - 30) < 15):
                        break
                    #Move towards the desired angle (Not completely necessary)
                    if ((ang - 30) > 0):
                        #Turn right
                        left_speed = rover.speed
                        right_speed = 0
                    else:
                        #Turn left
                        left_speed = 0
                        right_speed = rover.speed
                # Turn the rover until angle from the rover is oriented towards the tennis ball
                # conn = http.client.HTTPConnection(server)
                # conn.request("PUT", "/drive/speed/" + str(right_speed) + "/" + str(left_speed))
            print("distance to the ball: " + str(dis))

            #Drive the rover forward towards the ball
            #conn = http.client.HTTPConnection(server)
            #conn.request("PUT", "/drive/speed/" + str(rover.speed) + "/" + str(rover.speed))

        print("Arrived at the destination")

        #Stop the rover, onto the next gps_coordinates
        #conn = http.client.HTTPConnection(server)
        #conn.request("PUT", "/drive/stop")
    print("task finished")
    # cleanup the camera and close any open windows
    camera.release()
    # out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Server location of the laptop on the rover. Alternative location: "100.64.104.140:8080"
    server = "192.168.0.3:8080"
    DIST_FROM_TENNISBALL = 300

    # First Destination
    longitude = -79.403739
    latitude = 43.664809

    # The Destinations: (longitude, latitude)
    # You can add more markers onto the destination_markers array.
    destination_markers = [( longitude,  latitude), (1,1)]

    move_towards_the_ball(server, destination_markers)

    conn = http.client.HTTPConnection(server)
    conn.request("PUT", "/drive/stop")



