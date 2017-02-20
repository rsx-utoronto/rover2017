from math import *


# Distance from rover base origin to sensor origin in meters.
X_DIST = 0
Y_DIST = 0
Z_DIST = 0


def base_to_sensor(points):
    '''
    Transform points from base coordinates to sensor coordinates.

    Arguments:
        points: list of points in (rectangular) base coordinates, format
            [[x, y, z], ...]
    Returns:
        new_points: list of points in (spherical) sensor coordinates, format
            [[rho, theta, phi], ...]
    '''
    new_points = []

    for point in points:
        new_point = []
        # Add distance from base to sensor
        point[0] += X_DIST
        point[1] += Y_DIST
        point[2] += Z_DIST
        # Transform to spherical
        new_point.append((point[0]**2 + point[1]**2 + point[2]**2)**0.5)
        new_point.append(math.atan(point[1] / point[0]))
        new_point.append(math.acos(point[2] / new_point[0]))
        
        new_points.append(new_point)

    return new_points

def sensor_to_base(points, orientation):
    # points: [[dist, theta, phi], ...]
    # orientation: [x, y, z] vector in direction rover is pointing
    # return: [[x, y, z], ...]
    new_points = []

    # only works for 2D, i.e. flat ground
    rover_rotation = atan2(orientation[1], orientation[0])

    for point in points:
        r, t, p = point
        t -= 124       # since it nominally rotates 0-180, center on 90 (actually middle is 124)
        t += rover_rotation
        x = r*cos(t)*sin(p) - X_DIST
        y = r*sin(t)*sin(p) - Y_DIST
        z = r*cos(p) - Z_DIST
        new_points.append([x, y, z])

    return new_points

def base_to_world(points, position):
    for point in points:
        point[0] += position[0]
        point[1] += position[1]
        point[2] += position[2]

    return points

def world_to_base(points):
    pass

def sensor_to_world(points):
    pass

def world_to_sensor(points):
    pass