#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Maker
===========
This program takes in all your image files and makes a video out of it.

Created on Thu Oct  1 17:02:25 2020

@author: Agnit Mukhopadhyay
"""
import cv2
import os

image_folder = './Plots/Sept2011_Event_CUSIA/'
video_name = './Plots/Sept2011_Event_CUSIA/video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort()

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 10, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))
    print(image)

cv2.destroyAllWindows()
video.release()