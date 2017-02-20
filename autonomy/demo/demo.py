import time
from LidarBuffer import LidarBuffer
from TestRoverWheels import Rover
import numpy as np
import transforms
import serial


SERIAL_PORT = '/dev/ttyUSB1'   # may need to change the port
SAFE_DISTANCE = 0.5 # meters, don't go too low b/c the lidar just reports 0 at less than ~25cm
DEBUG_MODE = True
ROVER_WIDTH = 0.3 # meters
IP = 'localhost:8080'

def main():
    ser = serial.Serial(SERIAL_PORT, 115200)  # for communicating with lidar lite
    lidar = LidarBuffer(ser)   # to get data from the lidar
    lidar.start_listening()
    # rover = Rover(IP)   # to issue drive commands through the server
    # let everything initialize (mostly scanning motor)
    time.sleep(3)

    # the position and orientation of the lidar sensor
    position = np.array([0.0, 0.0, 0.0])
    # orientation is a vector in the direction the rover is pointing, not
    # necessarily normalized
    orientation = np.array([1.0, 0.0, 0.0])

    num_close_points = 0

    state = 'drive'

    while True:
        print(state)

        if state == 'drive':
            # rover.drive(30)   # some slow speed so it doesn't crash

            points = lidar.get_buffer()
            points = np.array(transforms.sensor_to_base(points, orientation))  # sphr -> rect
            # print(points)
            for point in points:
                dist = get_distance(point, position)
                print(dist)
                if dist < SAFE_DISTANCE and dist != 0:           # could maybe remove != 0 for closer results
                    if is_in_front(position, orientation, point):
                        print('block', point)
                        num_close_points += 1

            if num_close_points >= 4:   # could change num for detected obstacle, there is some noise in the data
                # rover.drive(0)
                num_close_points = 0
                print('switching state')
                state = 'pivot'

        elif state == 'pivot':
            # pivot a bit, scan in front, then continue or switch to drive
            # depending on blocked/not blocked
            # rover.pivot(30)
            time.sleep(0.5)
            # rover.pivot(0)

            # flush points collected while turning
            points = lidar.get_buffer()
            # get the points collected while stationary
            time.sleep(1)
            points = lidar.get_buffer()
            points = np.array(transforms.sensor_to_base(points, orientation))
            # print(points)
            for point in points:
                dist = get_distance(point, position)
                print(dist)
                if dist < SAFE_DISTANCE and dist != 0:
                    if is_in_front(position, orientation, point):
                        print('block', point)
                        num_close_points += 1

            if num_close_points == 0:
                # if currently pointing in unblocked direction, proceed to drive
                print('switching state')
                state = 'drive'

            num_close_points = 0


        time.sleep(0.5)  # to allow time to collect some points




def get_distance(a, b):
    '''
    Calculate the distance between 2 points a and b in 3D space.

    Arguments:
        a and b: points in 3D space, numpy array of floats format [x, y, z]

    Returns:
        distance: float, distance between the points
    '''
    distance = np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

    return distance

def is_in_front(position, orientation, point):
    # check if a point is in front of the rover
    # normalize orientation
    orientation = unit_vector(np.array(orientation))
    # print(orientation)
    # normal in the x-y plane
    normal = np.cross(orientation, np.array([0, 0, 1]))
    # print(normal)
    edge1 = np.add(position, normal*(ROVER_WIDTH/2))
    # print('edge1', edge1)
    edge2 = np.add(position, normal*(-ROVER_WIDTH/2))
    # print('edge2', edge2)
    v1 = np.subtract(point, edge1)
    # print('v1', v1)
    v2 = np.subtract(point, edge2)
    # print('v2', v2)
    angle1 = angle_between(v1, normal*(ROVER_WIDTH/2))
    # print('angle1', angle1)
    angle2 = angle_between(v2, normal*(-ROVER_WIDTH/2))
    # print('angle2', angle2)
    if angle1 > np.pi/2 and angle2 > np.pi/2:
        return True
    else:
        return False

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



if __name__ == '__main__':
    main()
