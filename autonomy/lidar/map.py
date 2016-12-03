from octomap import *
import numpy as np

RESOLUTION = 0.1


def main():
    tree = OcTree(RESOLTUION)

    while True:
        # 'lidar' is placeholder name for file containing python functions to
        # interface with arduino
        # expecting a numpy array of points in format [theta, phi, distance]
        pointcloud = lidar.get_point_buffer()
        # 'localization' is a placeholder name for file containing python
        # functions that keep track of rover position through some combination
        # of GPS, wheel encoders and whatever else - fomation [x, y, z] in world
        # coordinates
        rover_pos = localization.get_rover_position()
        # 'transforms' is a placeholder name for file containing python
        # functions to transform points between different frames
        origin = transforms.base_to_sensor(rover_pos)
        pointcloud = transforms.sensor_to_world()

        tree.insertPointCloud(pointcloud, origin)