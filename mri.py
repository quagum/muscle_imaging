from concurrent.futures import process
import cv2 as cv
from cv2 import ellipse
from matplotlib.pyplot import draw, gray
import numpy as np
image = cv.imread(r"C:\Users\charl\njit\muscle_imaging\MRI\MVC0-3\cIMG-0007-00098.jpg")
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

def convert_64_6(image_64):
    return 0

def fill_noise(processed_image, out_image):
    params = cv.SimpleBlobDetector_Params()

    params.filterByCircularity = True
    params.minArea = 1
    params.maxArea = 10

    params.filterByConvexity = True
    params.minConvexity = 0.2

    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    detector = cv.SimpleBlobDetector_create(params)

    keypoints = detector.detect(processed_image)
    blank = np.zeros((1, 1))
    blobs = cv.drawKeypoints(out_image, keypoints, blank, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
    # Show blobs
    cv.imshow("Filtering Circular Blobs Only", blobs)
    cv.waitKey(0)

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
fill_noise(convert, convert)
cv.waitKey(0)
