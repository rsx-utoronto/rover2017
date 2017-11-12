
# method ref: https://stackoverflow.com/questions/14038002/opencv-how-to-calculate-distance-between-camera-and-object-using-image


import numpy as np
import cv2
import glob

#focal lengthe of this camera
FOCAL_LENGTH = 4.3 # mm, for testing purpose with a phone rn.

# find native resolution of photos taken - only for comparing photo at diff resolution from native

# size of obj in real world in mm, diameter in this case
ball_diameter_real = ""

# take about 2 dozen photos,
CALIB_IMGSET = glob.glob('C:/git/rover/cv/calib_img/*.jpg')

#input image to find distance, frame past by ball_tracking.py or newly taken
FRAME = ""



def find_distance(focal_lenth,ball_diameter_real,calib_imgset,frame):

    # feed into opencv calibration, get intrinsic cam matrix -> fx,fy, px,py
    [fx, fy, px, py] = find_intrinsic_matrix(calib_imgset)

    # find px/mm on image sensor -> m=(fx+fy)/2/f
    px_mm_sensor = (fx + fy) / 2 / focal_lenth

    # find size of object s in px
    ball_diameter = find_ball_diameter(frame)

    # s px/(m px/mm) -> size of object on image sensor im mm
    ball_diameter_sensor = ball_diameter / px_mm_sensor

    # distance_mm = object_real_world_mm * focal-length_mm / object_image_sensor_mm
    distance = ball_diameter_real * focal_lenth / ball_diameter_sensor

    return distance

# detect and find diameter of ball
def find_ball_diameter(frame):

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=800)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    cv2.imshow("mask before de-noise", mask)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("mask", mask)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    print('contour length %d', len(cnts))
    print(cnts)
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print('centre')
        print(center)
        # only proceed if the radius meets a minimum size

        return radius*2
    else:
        return -1


def find_intrinsic_matrix(images):
    # ref: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)  # to unspecified value x 2

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.



    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7, 7), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)

    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print(mtx)

    fx,fy,px,py = mtx[0,0],mtx[1,1],mtx[0,2],mtx[1,2]
    return  [fx,fy,px,py]