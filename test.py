from tkinter import Image
import cv2 as cv
from numpy import average
image = cv.imread("cIMG-0007-00001.jpg")

first_x = image.shape[0]+1
first_y = image.shape[1]+1
for x in range(image.shape[0]):
    for y in range(image.shape[1]):
        b,r,g = image[x,y]
        if r == 0 and b == 0 and g == 0: 
            first_x = min(x,first_x)
            first_y = min(y,first_y) 
            last_x = x
            last_y = y
print("horizontal span: {} to {}".format(str(first_x), str(last_x)))
print("vertical span: {} to {}".format(str(first_y), str(last_y)))
print("center coordinates: ({}, {})".format(str((last_x+first_x)/2), str((last_y+first_y)/2)))

#find the center and plot point?
#make multiple points by moving the image window? 
#which white line to look for?
    #the brightness and width of white line
    #make an outline of all white lines (with brightness threshold)
    #from the outlines take the thickest bands of white and the bands properties like length, width, and position