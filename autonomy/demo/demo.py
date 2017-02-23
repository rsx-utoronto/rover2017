import time
from LidarBuffer import LidarBuffer
from TestRoverWheels import Rover
import numpy as np
import transforms
import serial


SERIAL_PORT = 'COM3'   # may need to change the port
SAFE_DISTANCE = 1 # meters, don't go too low b/c the lidar just reports 0 at less than ~25cm
DEBUG_MODE = True
ROVER_WIDTH = 0.3 # meters
IP = 'localhost:8080'

def main():
    ser = serial.Serial(SERIAL_PORT, 115200)  # for communicating with lidar lite
    lidar = LidarBuffer(ser)   # to get data from the lidar
    lidar.start_listening()
    rover = Rover(IP)   # to issue drive commands through the server

    time.sleep(3) # let everything initialize (mostly scanning motor)

    sweep_results = np.array([100000000.] * 180)  # stores the results of the
    # lidar sensor that we haven't collected this time

    state = 'drive'

    while True:
        print("State: {}".format(state))
        update_state(sweep_results, lidar)
        print np.mean(sweep_results[75:105])


        if state == 'drive':
            rover.drive(200)    # quick ramp
            rover.drive(100) # some slow speed so it doesn't crash
            # find the minimum distance
            if np.mean(sweep_results[75:105]) < SAFE_DISTANCE:
                print('switching state')
                state = 'pivot'
        elif state == 'pivot':
            rover.pivot(100)
            time.sleep(0.5)
            rover.pivot(0)
            # flush points collected while turning
            lidar.get_buffer()
            # get the points collected while stationary
            time.sleep(1)
            points = lidar.get_buffer()

            if np.mean(sweep_results[75:105]) > SAFE_DISTANCE:
                print('switching state')
                state = 'drive'

        time.sleep(0.5)  # to allow time to collect some points

def update_state(sweep_results, lidar):
    """
    Update the state of the rover, modifying sweep_results
    """
    points = lidar.get_buffer()
    for p in points:
        dist, theta, phi = p
        print dist
        if dist > 0.05:
            sweep_results[int(round(np.rad2deg(theta)))] = dist


    # sweep_results -= 0.1 * np.sin(np.deg2rad(np.arange(180))) # assume the rover drives this far every sweep.

def smooth(array):
    """
    Applies hanning smoothing on the array.
    No particular reason why we're using hanning, but why not
    """
    return np.convolve(array, np.hanning(7), mode='same')

if __name__ == '__main__':
    main()
