#software that makes averages of images


import numpy as np
import cv2
import os



#name of the folder containing images
path = '/home/marcos/Documents/reverse_micelles/paper/2_fig1/New_tracking/'

name = '158/'



#desired location and name od the output folder (all the picture will be put together)
output_path = '/home/marcos/Documents/reverse_micelles/paper/2_fig1/New_tracking/'

#opens image and converts image format
def image_to_float(path):
	print(path)
	a = cv2.imread(path,0)
	a = 1.*np.array(a)
	return a/np.amax(a)

def average_from_folder(path_of_images):
	list_of_img = sorted(os.listdir(path_of_images))
	total = image_to_float(path_of_images+list_of_img[0])/len(list_of_img)

	for filename in list_of_img:
		img_buffer = image_to_float(path_of_images+filename)
		total = total + img_buffer/len(list_of_img)

	return total

cv2.imwrite(output_path+name+ '_average.png', average_from_folder(path+'/'+name)*255)

