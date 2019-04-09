# Tracking beads
## Tutorial to track the position of beads with difficult background

Tracking beads is a task that is often used in miniature systems, since the position and movement of beads can be used to extract information about them and their environment. Beads can de used to detect the flow of liquid, its viscosity and to measure the forces acting on the particles. A clean and uniform background makes it easier to track beads, however this is not always the case. Tracking of multiple beads is also easier when the beads are similar, but even monodisperse beads can appear different during image analisys when there is motion blur, when the beads move in and out of focus, when the lightining of the image is not uniform and when the beads are too close to each other.

This software was developed to track fast moving polysterene beads observed by brightfield against a patterned opaque background. For example:


<p align="center">
  <img width="250" src="images/158.gif">
</p>

_Polysterene beads have distinct moves in liquid paraffin containing surfactant span 80 when an electric field is applied. The motion patterns depend on the voltage and surfactant concentration._

The main part of the code was provided by this StackOverflow answer.

This tutorial was tested in Ubuntu LTS 16.04.6 using Python 3.5.2. The steps can be adapted to use different OS and software.


From the video to the position of beads in Linux.

### 1. **Convert the video to a series of images**

The software we are going to use is only able to analyze still images, so we need to convert it to a series of images. 

For this, you can use the ffmpeg software and the command on terminal:

`ffmpeg -i infile.avi -f image2 image-%03d.jpg`

where infile.avi is the name of your video and image-03%.jpg is the name format of the series out images generated.

### 2. **Make an average image**

A way to detect a moving object is to generate a background image and then subtract each frame from the image being analyzed. 

For this, use the **average.py** contained in this project.

This will produce an image where the objects in motion will appear blurred. 

<p align="center">
  <img width="250" src="images/_average.png">
</p>

_Average image of 500 frames shows traces of the moving objects on the still background._

### 3. **Erase the ghost trajectories from the average image**

In an ideal average image, we obtain a clear background that can be subtracted to identify the moving subject. However, when the subject moving slowly, not moving, or moving repeatedly over the same area, we observe ghost traces. Ghost traces can trick the image analisys software.

To solve that, we have to manually clean the background image using image software. Here, we used the ipad Photoshop Fix app with the healing tool to erase the ghost traces. For example:

<p align="center">
  <img width="250" src="images/158_erased.JPG">
</p>


### 3. **Set parameters for bead identification**

We are trying to identify particles that don't have a traditional appearence, so it can be difficult for the software to identify the bead features. To solve that, parameter of the particles such as size and eccentricity are passed down to a software and the parameters have to be manually tested. 

<p align="center">
  <img width="250" src="images/158_processed.png">
</p>

_The image treatment outputs an image which, ideally, is composed of a black background with bright spots marking the position of the particles._

<p align="center">
  <img width="250" src="images/158_marked.png">
</p>

_The software correctly identified the position of the beads, even though the shape of the bright spots did not correspond to the spherical shape of the particles._

#### Overview of the detection algorithm and parameters

The parameters that have to be chosen manually are:

- ellipse_morph_x: used in case the particles are not spherical 
- ellipse_morph_y: used in case the particles are not spherical 
- radius: expected average radius of particles in pixels
- border_size: expected border of particles
- gap: minimum distance between particles
- threshold_binary: value for a threshold filter
- power_filter: the value of every pixel in an image becomes value^power_filter
- brighten_factor: the value of all pixels in am image becomes value x brighten_factor

The algorithm works by 

