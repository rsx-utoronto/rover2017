import numpy as np
import cv2
import matplotlib.pyplot as plt


def main():
    img = cv2.imread('img/d0.jpg')
    imgGrey = cv2.imread('img/d0.jpg', 0)

    # imgGrey = cv2.bilateralFilter(imgGrey, 9, 30, 30)   # blur slightly to remove noise
    imgGrey = cv2.blur(imgGrey, (3, 3))
    imgEdge = cv2.Canny(imgGrey, 150, 250)   # detect sharp edges only

    imWidth  = imgEdge.shape[1] - 1
    imHeight = imgEdge.shape[0] - 1

    # find length of edges, remove short ones
    edge_list = get_edge_list(imgEdge, imWidth, imHeight)
    edge_list = [a for a in edge_list if len(a) > 30]

    # flatten list
    edge_list = [item for sublist in edge_list for item in sublist]
    imgEdge[:] = 0
    for point in edge_list:
        imgEdge[point[1], point[0]] = 255

    stepSize = 8
    edgeArray = []

    for i in range (0, imWidth, stepSize):
        for j in range(imHeight - 5, (2*imHeight)//3, -1):
            if imgEdge.item(j, i) == 255:
                edgeArray.append((i, j))
                break
            else:
                pass

    # remove edges in top 2/3 of image
    # edgeArray = [a for a in edgeArray if a[1] > (2*imHeight)//3]

    xThreshold = 8
    yThreshold = 8
    obstacleArray = []
    toRemove = []
    toSplit = []

    # remove edge points that are not within the given threshold
    # TODO: split points into separate lists if they are adjacent but
    # one direction is greater than a threshold
    for i, point in enumerate(edgeArray):
        xRemoveFlag = 0
        yRemoveFlag = 0

        if i > 0:
            # check x distance to left neighbour
            if abs(point[0] - edgeArray[i-1][0]) > xThreshold:
                xRemoveFlag += 1
                # split before index
                toSplit.append(i)
                toRemove.append((-i, -i))
     
            # check y distance to left neighbour
            if abs(point[1] - edgeArray[i-1][1]) > yThreshold:
                yRemoveFlag += 1
                toSplit.append(i)
                toRemove.append((-i, -i))

        if i < len(edgeArray) - 1:
            # check x distance to right neighbour
            if abs(point[0] - edgeArray[i+1][0]) > xThreshold:
                xRemoveFlag += 1
                toSplit.append(i + 1)
                toRemove.append((-(i + 1), -(i + 1)))

            # check y distance to right neighbour
            if abs(point[1] - edgeArray[i+1][1]) > yThreshold:
                yRemoveFlag += 1
                toSplit.append(i + 1)
                toRemove.append((-(i + 1), -(i + 1)))

        if i == 0 or i == len(edgeArray) - 1:
            if xRemoveFlag or yRemoveFlag:
                toRemove.append(point)
        else:
            if xRemoveFlag == 2 or yRemoveFlag == 2:
                toRemove.append(point)

    for index, i in enumerate(toSplit):
        obstacleArray.insert(index, (-i, -i))
        

    for point in toRemove:
        obstacleArray.append(edgeArray[:edgeArray.index(point)])
        del edgeArray[:edgeArray.index(point) + 1]
    obstacleArray.append(edgeArray)   # add any last obstacle that may have been missed
    obstacleArray = [a for a in obstacleArray if a != []]

    # remove short edges
    obstacleArray = [a for a in obstacleArray if len(a) > 7]

    for y in range(len(obstacleArray)):
        for x in range(len(obstacleArray[y]) - 1):
            cv2.line(img, obstacleArray[y][x], obstacleArray[y][x + 1], (255, 0, 0), 4)

    # display image
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.imshow('img', imgEdge)
    cv2.waitKey(0)
    cv2.imshow('img', imgGrey)
    cv2.waitKey(0)


def get_next_edge_points(point, visited, img):
    points = []

    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if (i, j) != (0, 0):
                try:
                    if img.item(point[1] + j, point[0] + i) == 255:
                        if (point[0] + i , point[1] + j) not in visited:
                            points.append((point[0] + i, point[1] + j))
                except(IndexError):
                    pass

    return points

def get_edge_list(img, img_width, img_height):
    edges = [[]]
    visited = []

    for i in range(img_width):
        for j in range(img_height):
            if img.item(j, i) == 255 and (i, j) not in visited:
                edges[-1].append((i, j))
                visited.append((i, j))

                point_stack = [(i, j)]

                while len(point_stack) > 0:
                    curr_point = point_stack.pop()
                    next_points = get_next_edge_points(curr_point, visited, img)

                    for point in next_points:
                        point_stack.append(point)

                    edges[-1].append(curr_point)
                    visited.append(curr_point)

                edges.append([])

    # in case there is an empty list left at the end
    edges.remove([])

    return edges

def remove_circular_edges(edge_list, threshold):
    ''' Remove edges in image that are contained entirely by a box of side
        length threshold. Short straight edges have already been removed
        so the point of this function is to remove edges with a long enough
        length to escape the first filter but that are compact in the image and
        likely represent an irrelevant feature e.g. a pebble. '''

    edges_to_remove = []

    for edge in edge_list:
        max_height = max([a[1] for a in edge])
        min_height = min([a[1] for a in edge])

        max_width = max([a[0] for a in edge])
        min_width = min([a[0] for a in edge])

        height = abs(max_height - min_height)
        width = abs(max_width - min_width)

        if height < threshold and width < threshold:
            edges_to_remove.append(edge)

    for edge in edges_to_remove:
        edge_list.remove(edge)

    return edge_list





if __name__ == '__main__':
    main()