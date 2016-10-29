import numpy as np
import cv2
import matplotlib.pyplot as plt


def main():
    # full colour image loaded only so user can see output on top
    img = cv2.imread('img/desert.jpg')
    imgGrey = cv2.imread('img/desert.jpg', 0)

    imgGrey = cv2.blur(imgGrey, (3, 3))
    # detect sharp edges only, so high threshold
    imgEdge = cv2.Canny(imgGrey, 150, 250)

    
    # find length of edges, remove short ones
    edge_list = get_edge_list(imgEdge)
    edge_list = remove_short_edges(edge_list, 30)
    edge_list = remove_circular_edges(edge_list, 20)
    
    # flatten list and make black image with edges highlighted (so user can see)
    edge_list_flat = [item for sublist in edge_list for item in sublist]
    imgEdge[:] = 0
    for point in edge_list_flat:
        imgEdge[point[1], point[0]] = 255

    # draw edges on original image
    for edge in edge_list:
        for i in range(len(edge) - 1):
            cv2.line(img, edge[i], edge[i + 1], (255, 0, 0), 4)

    # display image
    # press any key to destroy window and view next image
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.imshow('img', imgEdge)
    cv2.waitKey(0)
    cv2.imshow('img', imgGrey)
    cv2.waitKey(0)


def get_edge_list(img):
    ''' Find and return list of edges in img, where img is assumed to be
        the output of a Canny filter. An 'edge' in edge_list is a list of points
        that comprise the edge. '''
    edges = [[]]
    visited = []

    img_width  = img.shape[1] - 1
    img_height = img.shape[0] - 1

    for i in range(img_width):
        for j in range(img_height):
            if img.item(j, i) == 255 and (i, j) not in visited:
                edges[-1].append((i, j))
                visited.append((i, j))

                point_stack = [(i, j)]

                while len(point_stack) > 0:
                    curr_point = point_stack.pop()
                    next_points = get_adjacent_edge_points(curr_point, visited, img)

                    for point in next_points:
                        point_stack.append(point)

                    edges[-1].append(curr_point)
                    visited.append(curr_point)

                edges.append([])

    # in case there is an empty list left at the end
    edges.remove([])

    return edges


def get_adjacent_edge_points(point, visited, img):
    ''' Return list of points adjacent to point that have not been visited
        and that are part of an edge (white). Diagonal adjacency is counted. '''
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


def remove_short_edges(edge_list, threshold):
    ''' Remove edges in image that are shorter than threshold. These edges
        are assumed to represent noise or irrelevant features such as an
        obstacle that the rover could easily traverse. '''

    return [a for a in edge_list if len(a) >= threshold]


def remove_circular_edges(edge_list, threshold):
    ''' Remove edges in image that are contained entirely by a box of side
        length threshold. Short straight edges have already been removed
        so the point of this function is to remove edges with a long enough
        length to escape the first filter but that are compact in the image and
        therefore likely represent an irrelevant feature e.g. a pebble. '''

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