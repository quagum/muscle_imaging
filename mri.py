from concurrent.futures import process
import cv2 as cv
from cv2 import ellipse
from cv2 import split
from cv2 import CAP_PROP_SPEED
from matplotlib.pyplot import draw, gray
import numpy as np
import os

def convert_64_8(image_64):
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

def image_preprocessing(input_image):
    cropped = input_image[100:600, 0:951]
    scaled = cv.pyrDown(cropped) 
    blurred = cv.GaussianBlur(scaled, (7, 7), 0)
    return blurred  

def sobel_processing(input_image):
    sobel = cv.Sobel(input_image, cv.CV_64F, dx=0, dy=1, ksize=9)
    image = cv.GaussianBlur(sobel, (0,11), 9)
    binary = np.zeros_like(image)
    binary[(image >= 30000) & (image <= 2000000)] = 1
    return binary

def image_processing(input_image):
    processed = sobel_processing(input_image)
    convert = convert_64_8(processed)
    return convert

def draw_blank_lines(input_image, canvas):
    minLineLength = 150
    maxLineGap = 0
    lines = cv.HoughLinesP(input_image, cv.HOUGH_PROBABILISTIC, np.pi/180, 200, maxLineGap, minLineLength)
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
            cv.polylines(canvas, [pts], True, (0, 255, 255), 3)
    return canvas
    
#x=476 y=200
#not all MRI scans will have the same middle --> how to find the middle?  
def automatic_crop(input_image):
    ret, thresh = cv.threshold(input_image, 127, 255, cv.THRESH_BINARY) #no idea why it forces another variable to be stored 
    cv.imshow('threshold', thresh)
    white_pt_coords = np.argwhere(thresh)
    min_y = min(white_pt_coords[:,0])
    min_x = min(white_pt_coords[:,1])
    max_y = max(white_pt_coords[:,0])
    max_x = max(white_pt_coords[:,1])
    crop = input_image[min_y:max_y,min_x:max_x]
    return crop 

def multi(): 
    dir = 'scans'
    for file in os.listdir(dir):
        f = os.path.join(dir, file)
        image = cv.imread(f)

        cropped = image[100:600, 0:951]
        scaled = cv.pyrDown(cropped)  
        gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
        sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
        #cv.imshow('sobel', sobel)
        blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
        T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
        #cv.imshow('thresh', thresh)

        convert = convert_64_8(thresh)
        cv.imshow(f, draw_blank_lines(convert, scaled))
        cv.waitKey(0)

def single():
    image = cv.imread(r"C:\Users\charl\njit\muscle_imaging\scans\cIMG-0007-00001.jpg")
    cropped = image[100:600, 0:951]
    scaled = cv.pyrDown(cropped)  
    gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
    sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=9)
    cv.imshow('sobel', sobel)
    blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
    T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
    cv.imshow('thresh', thresh)

    convert = convert_64_8(thresh)
    cv.imshow('final', draw_blank_lines(convert, scaled))
    cv.waitKey(0)

multi()