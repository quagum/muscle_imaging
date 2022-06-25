from concurrent.futures import process
import cv2 as cv
from cv2 import ellipse
from cv2 import split
from matplotlib.pyplot import draw, gray
import numpy as np

image = cv.imread(r"C:\Users\charl\njit\muscle_imaging\MRI\MVC0-3\cIMG-0007-00083.jpg")

def convert_64_8(image_64):
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

def image_preprocessing(input_image):
    gray = cv.cvtColor(input_image, cv.COLOR_BGR2GRAY)
    cropped = gray[100:500, 0:951]
    scaled = cv.pyrDown(cropped) 
    blurred = cv.GaussianBlur(scaled, (7, 7), 0)
    return blurred 

def image_preprocessing_2(input_image):
    gray = cv.cvtColor(input_image, cv.COLOR_BGR2GRAY)
    cropped = gray[100:500, 0:951]
    scaled = cv.pyrDown(cropped) 
    blurred = cv.GaussianBlur(scaled, (0,11), 9)
    return blurred     

def sobel_processing(input_image):
    sobel = cv.Sobel(input_image, cv.CV_64F, dx=0, dy=1, ksize=9)
    image = cv.GaussianBlur(sobel, (0,11), 9)
    #is this not the same as thresholding? redundant code? 
    binary = np.zeros_like(image)
    binary[(image >= 30000) & (image <= 2000000)] = 1
    return binary

def image_processing(input_image):
    processed = sobel_processing(input_image)
    convert = convert_64_8(processed)
    gray = cv.cvtColor(convert, cv.COLOR_BGR2GRAY)
    return gray

def draw_blank_lines(input_image):
    blank = np.zeros(input_image.shape)
    blank.fill(0)
    minLineLength = 200
    maxLineGap = 0
    lines = cv.HoughLinesP(input_image, cv.HOUGH_PROBABILISTIC, np.pi/180, 280, minLineLength, maxLineGap)
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
            cv.polylines(blank, [pts], True, (255, 255, 255), 5)
    return blank
    
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

blurred = image_preprocessing(image)
blurred_2 = image_preprocessing_2(image)

ret, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
cv.imshow("otsu thresh", thresh)
ret, thresh_2= cv.threshold(blurred_2, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
cv.imshow("otsu thresh 2", thresh_2)

sobel = sobel_processing(thresh)
cv.imshow("sobel", sobel)
sobel_2 = sobel_processing(thresh_2)
cv.imshow("sobel_2", sobel_2)

cv.waitKey(0)

#test on other images
#take the lines closer to the center to differentiate random lines from target --> split picture into lower and upper half =? does it make it easier to read?
#when picture is split find the lower line in the top half and the upper line in the lower half 
#generate the points of this line
#merge image_processing and sobel

#contours? https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html --> curve joining all cont points hving the same color 
