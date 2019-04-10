
import numpy as np
import cv2
import os
from scipy.ndimage import gaussian_filter
from skimage.morphology import reconstruction

#parameters
ellipse_morph_x = 50
ellipse_morph_y = 50
threshold_binary = 0.1
#crop = [100,558, 0,1916]
border_size = 60
gap = 60
radius = 60

#power_filter: an image**power is an enhancement factor, dimming darker pixels and brigthening brighter pixels
power_filter = 2

#multiplies the values of an image by a constant
brighten_factor = 2000


#input: two images, one of the experiment and one of the average with erased beads
#outputs experimetn image with mars of the identified beads
#how to use: modify parameters until adequate set is found

path_of_image = '/home/marcos/Documents/reverse_micelles/paper/2_fig1/New_tracking/158/image-292.jpg'
average_path = '/home/marcos/Documents/reverse_micelles/paper/2_fig1/New_tracking/158_erased.JPG'

#opens image and converts image format
def image_to_float(path):
	a = cv2.imread(path,0)
	a = 1.*np.array(a)
	return cv2.normalize(a, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
	#return a

average = cv2.imread(average_path,0)
average = 1.*np.array(average)
average = cv2.normalize(average, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

def finds_center_beads(im_path, b, g):

	borderSize = b

	gap = g

	im = cv2.imread(im_path)
	
	image = np.zeros((im.shape[0], im.shape[1], 3), np.uint8)

	
	hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
	
	th, bw = cv2.threshold(hsv[:, :, 2], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ellipse_morph_x, ellipse_morph_y))
	morph = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
	dist = cv2.distanceTransform(morph, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

	distborder = cv2.copyMakeBorder(dist, borderSize, borderSize, borderSize, borderSize, 
		                        cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)
		                       
	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*(borderSize-gap)+1, 2*(borderSize-gap)+1))
	kernel2 = cv2.copyMakeBorder(kernel2, gap, gap, gap, gap, 
		                        cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)
	distTempl = cv2.distanceTransform(kernel2, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
	nxcor = cv2.matchTemplate(distborder, distTempl, cv2.TM_CCOEFF_NORMED)
	mn, mx, _, _ = cv2.minMaxLoc(nxcor)
	th, peaks = cv2.threshold(nxcor, mx*threshold_binary, 255, cv2.THRESH_BINARY)
	peaks8u = cv2.convertScaleAbs(peaks)
	contours, hierarchy = cv2.findContours(peaks8u, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	peaks8u = cv2.convertScaleAbs(peaks)    # to use as mask
	for i in range(len(contours)):
	    x, y, w, h = cv2.boundingRect(contours[i])
	    _, mx, _, mxloc = cv2.minMaxLoc(dist[y:y+h, x:x+w], peaks8u[y:y+h, x:x+w])
	    cv2.circle(im, (int(mxloc[0]+x), int(mxloc[1]+y)), int(2), (255, 0, 0), radius)
	    #cv2.circle(im, (int(mxloc[0]+x), int(mxloc[1]+y)), int(2), (255, 0, 0), radius)
	    #cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 255), 2)
	    #cv2.drawContours(im, contours, i, (0, 0, 255),2)

	return im



img_buffer = image_to_float(path_of_image)

	
difference = (img_buffer-average)**power_filter

####
image = gaussian_filter(difference, 1)
seed = np.copy(image)
seed[1:-1, 1:-1] = image.min()
mask = image
dilated = reconstruction(seed, mask, method='dilation')
subtract = image-dilated

#crop_img = difference[crop[0]:crop[1], crop[2]:crop[3]]
#crop_img = difference

#ddepth = cv2.CV_8UC1


cv2.imwrite('laplacian.png', subtract*brighten_factor)

#cv2.imshow("diff", crop_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

	#cv2.imwrite(filename+'.png', crop_img*255)

marked_center_img = finds_center_beads('laplacian.png', border_size, gap)

cv2.imwrite('marked.png', marked_center_img)

#cv2.imshow("hsv", marked_center_img )
#cv2.waitKey(0)
#cv2.destroyAllWindows()


	
	




