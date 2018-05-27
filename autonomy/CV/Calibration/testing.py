import numpy as np


kmtx = np.load('C:/Users/rache/PycharmProjects/rsx/k_matrix.npy')
print(kmtx)

vmtx = np.load('C:/Users/rache/PycharmProjects/rsx/v_matrix.npy')
print(vmtx)


#convert the focal length in pxs to focal length in mm
#http://answers.opencv.org/question/17076/conversion-focal-distance-from-mm-to-pixels/
#focal_pixel = (focal_mm / sensor_width_mm) * image_width_in_pixels
#focal_mm  = (focal_pixel./image_width)*sensor_width_mm

#list of camera parameters here: https://www.gearbest.com/ip-cameras/pp_577788.html for the vesky camera

#computing focal pixels using  --> focal_pixel = (image_width_in_pixels * 0.5) / tan(FOV * 0.5 * PI/180)
#http://answers.opencv.org/question/17076/conversion-focal-distance-from-mm-to-pixels/

#focal_pixel = vmtx[0,0]; from the camera matrix
focal_pixel = 640;
image_width_px = 1280; # camera = 1280x960
sensor_width_mm = 6.35; #sensor width = 1/4 inches -- converted to mm



focal_mm = (focal_pixel/image_width_px)*sensor_width_mm
print(focal_mm)