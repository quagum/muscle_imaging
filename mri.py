from concurrent.futures import process
import cv2 as cv
from matplotlib.pyplot import draw, gray
import numpy as np
image = cv.imread("cIMG-0007-00207.jpg")
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

def convert_64_8(image_64):
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

def draw_lines(processed_image, output_image):
    lines = cv.HoughLinesP(processed_image, 1, np.pi/180, 320)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(output_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
    return output_image

processed = sobel_processing(image)
convert = convert_64_8(processed)
gray = cv.cvtColor(convert, cv.COLOR_BGR2GRAY)
final = draw_lines(gray, processed)


#use houghcircles to find ellipses and remove the small blemishes in the processed image
#this would leave only long lines left on the image and so the houghlines could be more fine tuned and not draw lines on the blemishes 
cv.imshow("processed", final)
cv.waitKey(0)
