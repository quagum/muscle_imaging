from concurrent.futures import process
import cv2 as cv
from cv2 import ellipse
from cv2 import split
from matplotlib.pyplot import draw, gray
import numpy as np

image = cv.imread(r"C:\Users\charl\njit\muscle_imaging\MRI\MVC0-3\cIMG-0007-00082.jpg")
#cv.imshow("original", image)

def sobel_processing(image):
    cropped = image[100:500, 0:951]
    scaled = cv.pyrDown(cropped) 
    sobel = cv.Sobel(scaled, cv.CV_64F, dx=0, dy=1, ksize=9)
    image = cv.GaussianBlur(sobel, (0,11), 9)
    #cv.imshow("Processed", image)

    binary = np.zeros_like(image)
    binary[(image >= 30000) & (image <= 2000000)] = 1
    return binary

#unused
def canny_processing(image):
    cropped = image[100:500, 0:951]
    scaled = cv.pyrDown(cropped) 
    image = cv.Canny(scaled, 180, 255)
    #cv.imshow("Processed", image)
    return image 

def convert_64_8(image_64):
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

#unused --> results not as impactful? try testing and compare 
def fill_noise(input_image):
    opening = cv.morphologyEx(input_image, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)))
    cv.imshow('test', opening)

#unused --> replaced by draw_blank_lines which uses polylines to draw curved lines
def draw_lines(processed_image, output_image):
    lines = cv.HoughLinesP(processed_image, 1, np.pi/180, 320)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(output_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
    return output_image

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
#threshold image into finding min max values of white to crop? 
def split_image(input_image):
    thresh = cv.threshold(input_image, 127, 255, cv.THRESH_BINARY)
    white_pt_coords = np.argwhere(thresh)
    min_y = min(white_pt_coords[:,0])
    min_x = min(white_pt_coords[:,1])
    max_y = max(white_pt_coords[:,0])
    max_x = max(white_pt_coords[:,1])
    crop = input_image[min_y:max_y,min_x:max_x]
    return crop

def store():
    y = input_image.shape[0]
    half_y = int(y/2)
    top_half = input_image[0:half_y]
    bottom_half = input_image[half_y:y]
    return top_half, bottom_half


processed = image_processing(image)
final = draw_blank_lines(processed)
split_image(final)
cv.imshow("final", final)

cv.waitKey(0)

#test on other images
#take the lines closer to the center to differentiate random lines from target --> split picture into lower and upper half =? does it make it easier to read?
#when picture is split find the lower line in the top half and the upper line in the lower half 
#generate the points of this line

#contours? https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html --> curve joining all cont points hving the same color 
