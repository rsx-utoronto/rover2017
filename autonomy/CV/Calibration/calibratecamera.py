import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.bmp')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,7), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

#perform the calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

#perform the undistortion on the single image
img = cv2.imread('20180525_213800_365.bmp')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
print(newcameramtx)
np.save("v_matrix.npy", newcameramtx);

#convert the focal length in pxs to focal length in mm
#http://answers.opencv.org/question/17076/conversion-focal-distance-from-mm-to-pixels/
#focal_pixel = (focal_mm / sensor_width_mm) * image_width_in_pixels
#focal_mm  = (focal_pixel./image_width)*sensor_width_mm

#list of camera parameters here: https://www.gearbest.com/ip-cameras/pp_577788.html for the vesky camera
focal_pixel = newcameramtx[0,0];
image_width_px = 1280; # camera = 1280x960
sensor_width_mm = 6.35; #sensor width = 1/4 inches

focal_mm = (focal_pixel/image_width_px)*sensor_width_mm
print(focal_mm)


# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult_veskycam.png',dst)