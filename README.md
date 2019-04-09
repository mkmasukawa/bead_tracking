This tutorial was tested in Ubuntu LTS 16.04.6 using Python 3.5.2. The steps can be adapted to use different OS and software.

Software used:
ffmpeg


From the video to the position of beads in Linux.

1) Convert the video to a series of images
The software we are going to use is only able to analyze still images, so we need to convert it to a series of images. 

For this, you can use the ffmpeg software and the command on terminal:

ffmpeg -i infile.avi -f image2 image-%03d.jpg

where infile.avi is the name of your video and image-03%.jpg is the name format of the series out images generated.

2) Make an average image

A way to detect a moving object is to generate a background image and then subtract each frame from the image being analyzed.

For this, use the software
