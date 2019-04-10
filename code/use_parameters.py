import cv2.cv as cv
import numpy as np
import cv2
import os

ellipse_morph_x = 50
ellipse_morph_y = 50
threshold_binary = 0.2
crop = [100,558, 0,1916]
border_size = 150
gap = 100
radius = 30

#experiment code
code = '5611'

#input: two images, one of the experiment and one of the average with erased beads
#outputs experimetn image with mars of the identified beads
#how to use: modify parameters until adequate set is found

#image where the beads will be identified
path_of_images = '/home/marcos/Documents/reverse_micelles/analyzed/MVI_'+code+'/'


# print path_of_images
#image background 
average_path = '/home/marcos/Documents/reverse_micelles/analyzed/averages/erased/'+code+'.jpg'

#opens image and converts image format
def image_to_float(path):
	a = cv2.imread(path,0)
	a = 1.*np.array(a)
	return a/np.amax(a)

average = cv2.imread(average_path,0)
average = 1.*np.array(average)
average = average/np.amax(average)

def finds_center_beads(im_path, b, g):

	borderSize = b

	gap = g
	print im_path

	im = cv2.imread(im_path)

	
	image = np.zeros((im.shape[0], im.shape[1], 3), np.uint8)

	
	hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
	
	th, bw = cv2.threshold(hsv[:, :, 2], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ellipse_morph_x, ellipse_morph_y))
	morph = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
	dist = cv2.distanceTransform(morph, cv2.cv.CV_DIST_L2, cv2.cv.CV_DIST_MASK_PRECISE)

	distborder = cv2.copyMakeBorder(dist, borderSize, borderSize, borderSize, borderSize, 
		                        cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)
		                       
	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*(borderSize-gap)+1, 2*(borderSize-gap)+1))
	kernel2 = cv2.copyMakeBorder(kernel2, gap, gap, gap, gap, 
		                        cv2.BORDER_CONSTANT | cv2.BORDER_ISOLATED, 0)
	distTempl = cv2.distanceTransform(kernel2, cv2.cv.CV_DIST_L2, cv2.cv.CV_DIST_MASK_PRECISE)
	nxcor = cv2.matchTemplate(distborder, distTempl, cv2.TM_CCOEFF_NORMED)
	mn, mx, _, _ = cv2.minMaxLoc(nxcor)
	th, peaks = cv2.threshold(nxcor, mx*threshold_binary, 255, cv2.THRESH_BINARY)
	peaks8u = cv2.convertScaleAbs(peaks)
	contours, hierarchy = cv2.findContours(peaks8u, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	peaks8u = cv2.convertScaleAbs(peaks)    # to use as mask
	for i in range(len(contours)):
	    x, y, w, h = cv2.boundingRect(contours[i])
	    _, mx, _, mxloc = cv2.minMaxLoc(dist[y:y+h, x:x+w], peaks8u[y:y+h, x:x+w])
	    #cv2.circle(im, (int(mxloc[0]+x), int(mxloc[1]+y)), int(mx), (255, 0, 0), 4)
	    cv2.circle(image, (int(mxloc[0]+x), int(mxloc[1]+y)), int(2), (255, 255, 255), 4)
	    #cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 255), 2)
	    #cv2.drawContours(im, contours, i, (0, 0, 255),2)

	return image


for filename in sorted(os.listdir(path_of_images)):

	img_buffer = image_to_float(path_of_images+filename)

	

	difference = img_buffer-average

	crop_img = difference[crop[0]:crop[1], crop[2]:crop[3]]


	laplacian = cv2.Laplacian(crop_img,cv2.CV_64F)

	cv2.imwrite('buffer.png', difference*255)

#cv2.imshow("diff", crop_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

	#cv2.imwrite(filename+'.png', crop_img*255)

	marked_center_img = finds_center_beads('buffer.png', border_size, gap)

	if not os.path.exists(path_of_images+'black_canvas/'):
		os.makedirs(path_of_images+'black_canvas/')

	cv2.imwrite(path_of_images+'black_canvas/'+filename, marked_center_img)


	#cv2.imshow("hsv", cv2.resize(marked_center_img, (0,0), fx=0.5, fy=0.5)  )
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()


	
	




