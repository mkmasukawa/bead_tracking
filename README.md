#Tracking beads
##Tutorial to track the position of beads with difficult background

Tracking beads is a task that is often used in miniature systems, since the position and movement of beads can be used to extract information about them and their environment. Beads can de used to detect the flow of liquid, their viscosity and to measure the forces acting on the particles. A clean and uniform background makes it easier to track beads, however this is not always the case. Tracking of multiple beads is also easier when the beads are similar, but even monodisperse beads can appear different during image analisys when there is motion blur, when the lightining of the image is not uniform and when the beads are too close to each other.

This software was developed to track fast moving polysterene beads observed by brightfield against a patterned opaque background. The main part of the code was provided by this StackOverflow answer.

This tutorial was tested in Ubuntu LTS 16.04.6 using Python 3.5.2. The steps can be adapted to use different OS and software.


From the video to the position of beads in Linux.

1. **Convert the video to a series of images**

The software we are going to use is only able to analyze still images, so we need to convert it to a series of images. 

For this, you can use the ffmpeg software and the command on terminal:

`ffmpeg -i infile.avi -f image2 image-%03d.jpg`

where infile.avi is the name of your video and image-03%.jpg is the name format of the series out images generated.

2. **Make an average image**

A way to detect a moving object is to generate a background image and then subtract each frame from the image being analyzed. 

For this, use the average.py 
