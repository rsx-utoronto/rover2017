from octomap import *
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def convert_to_heightmap(tree):
    x_min, y_min, z_min = tree.getMetricMin()
    x_max, y_max, z_max = tree.getMetricMax()
    resolution = tree.getResolution()
    
    # holds surface points (no higher node at same x and y) format [x, y, z]
    surface = []

    min_key = tree.coordToKey(np.array([x_min, y_min, z_min]))
    max_key = tree.coordToKey(np.array([x_max, y_max, z_max]))
    key = min_key

    x = 0
    while min_key[0] + x <= max_key[0]:
        y = 0
        while min_key[1] + y <= max_key[1]:
            # look for highest occupied node height at given x and y
            z = 0        # amount to add to original z
            highest = None
            while min_key[2] + z <= max_key[2]:
                key[0] = min_key[0] + x
                key[1] = min_key[1] + y
                key[2] = min_key[2] + z
                node = tree.search(key)
                print(key[0], key[1], key[2])

                try:
                    if tree.isNodeOccupied(node):
                        highest = tree.keyToCoord(key)
                except NullPointerException:
                    # node does not exist
                    pass

                z += 1
            if highest is not None:
                point = highest
                surface.append([point[0], point[1], point[2]])
            else:
                pass

            y += 1
        x += 1

    return surface

def get_gradient(tree, x, y, z):
    node = tree.search((x, y, z))

    # if node not occupied, invalid request; occupancy given as probability
    if node is None or not tree.isNodeOccupied(node):
        return None

    key = node.getKey()
    # get neighbouring nodes
    above = tree.search((key[0], key[1], key[2]+1))
    below = tree.search((key[0], key[1], key[2]-1))

    gradient = []

    for i in range(2):
        for j in range(-1, 2, 2):
            curr_key = list(key)
            curr_key[i] += j

            heights = []

            for k in range(-1, 2, 1):
                highest_node = tree.search((curr_key[0], curr_key[1], \
                    curr_key[2]+k))
                if tree.isNodeOccupied(highest_node):
                    continue
                else:
                    # highest node was actually the one below
                    k -= 1
                    break

            # so that height index starts at 0
            heights.append(k+2)
        gradient.append(np.mean(heights) / 2)

    return gradient




if __name__ == '__main__':
    tree = OcTree(0.1)
    tree.insertPointCloud(np.array([[ 1.0, 0.0 , 0.0],
                                    [ 0.0, 0.0,  1.0],
                                    [-1.0, 0.0,  0.0],
                                    [ 0.0, 0.0, -1.0]]),
                          np.array( [ 0.0, 1.0,  0.0]))
    points = convert_to_heightmap(tree)
    print(points)

    x = [point[0] for point in points]
    y = [point[1] for point in points]
    z = [point[2] for point in points]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.show()