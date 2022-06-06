from concurrent.futures import process
import cv2 as cv
from matplotlib.pyplot import gray
import numpy as np
image = cv.imread("cIMG-0007-00001.jpg")
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

def canny_processing(image):
    cropped = image[100:500, 0:951]
    scaled = cv.pyrDown(cropped) 
    image = cv.Canny(scaled, 180, 255)
    #cv.imshow("Processed", image)
    return image 

def draw_lines(image):
    lines = cv.HoughLinesP(image, 1, np.pi/180, 400)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

processed = sobel_processing(image)
image = processed - processed.min() # Now between 0 and 8674
image = processed / processed.max() * 255
convert = np.uint8(image)
#cv.imshow("convert", convert)

gray = cv.cvtColor(convert, cv.COLOR_BGR2GRAY)
cv.imshow("gray", gray)


lines = cv.HoughLinesP(gray, 1, np.pi/180, 400)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(processed, (x1, y1), (x2, y2), (0, 255, 0), 1)
cv.imshow("processed", processed)

cv.waitKey(0)
