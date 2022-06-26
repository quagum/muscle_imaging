from concurrent.futures import process
import cv2 as cv
from cv2 import ellipse
from cv2 import split
from matplotlib.pyplot import draw, gray
import numpy as np

image = cv.imread(r"C:\Users\charl\njit\muscle_imaging\MRI\MVC0-3\cIMG-0007-00198.jpg")

def convert_64_8(image_64):
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

def image_preprocessing(input_image):
    cropped = input_image[100:600, 0:951]
    scaled = cv.pyrDown(cropped) 
    blurred = cv.GaussianBlur(scaled, (7, 7), 0)
    return blurred 

def image_preprocessing_2(input_image):
    cropped = input_image[100:600, 0:951]
    scaled = cv.pyrDown(cropped) 
    blurred = cv.GaussianBlur(scaled, (0,11), 9)
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

def draw_blank_lines(input_image):
    blank = np.zeros(input_image.shape)
    blank.fill(0)
    minLineLength = 200
    maxLineGap = 0
    lines = cv.HoughLinesP(input_image, cv.HOUGH_PROBABILISTIC, np.pi/180, 200, maxLineGap, minLineLength)
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
gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU) #255
cv.imshow("thresh", thresh)
sobel = image_processing(thresh)
cv.imshow("sobel", sobel)
cv.imshow("final", draw_blank_lines(sobel))
cv.waitKey(0)
