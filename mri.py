import cv2 as cv
import numpy as np
import os

def convert_64_8(image_64): #converts input image of type CV_64F to CV_8U
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

def image_preprocessing(image_path): #takes image path and returns cropped grayscale image and cropped processed image
    image = cv.imread(image_path)
    cropped = image[100:600, 0:951]
    scaled = cv.pyrDown(cropped)  
    gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
    sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
    blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
    T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
    convert = convert_64_8(thresh)
    return convert, scaled

def generate_data(input_image): #takes pre-processed image and generates 2D data points
    minLineLength = 150
    maxLineGap = 0
    coordinates_2D = cv.HoughLinesP(input_image, cv.HOUGH_PROBABILISTIC, np.pi/180, 200, maxLineGap, minLineLength)
    return coordinates_2D

def draw_line(image): #takes image and returns cropped/scaled image with an attempted highlight of muscle boundaries
    pre, original = image_preprocessing(image)
    lines = generate_data(pre)
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            pts = np.array([[x1, y1], [x2, y2]], np.int32)
            cv.polylines(original, [pts], True, (0, 255, 255), 1)
    return draw_line

def draw_blank_lines(input_image, canvas, z):
    minLineLength = 150
    maxLineGap = 0
    lines = cv.HoughLinesP(input_image, cv.HOUGH_PROBABILISTIC, np.pi/180, 200, maxLineGap, minLineLength)
    coordinates = []
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            line = [[x1, y1, z], [x2, y2, z]]
            pts = np.array([[x1, y1], [x2, y2]], np.int32)
            coordinates.append(line)
            cv.polylines(canvas, [pts], True, (0, 255, 255), 1)
    return canvas, coordinates

def single_image(image_path):
    scaled = cv.imread(image_path)
    z = 1
    #cropped = image[100:600, 0:951]
    #scaled = cv.pyrDown(cropped)  
    gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
    sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
    blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
    T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
    convert = convert_64_8(thresh)
    final, coordinates = draw_blank_lines(convert, scaled, z)
    cv.imshow(image_path, final)
    cv.waitKey()
    return coordinates    

def multi_image(): 
    dir = 'scans'
    for file in os.listdir(dir):
        os.chdir(r'C:\Users\charl\njit\muscle_imaging')
        f = os.path.join(dir, file)
        z = int(file[10:len(file)-4])
        try:
            image = cv.imread(f)
            print(f)
            cropped = image[100:600, 0:951]
            scaled = cv.pyrDown(cropped)  
            gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
            sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
            #cv.imshow('sobel', sobel)
            blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
            T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
            #cv.imshow('thresh', thresh)
            convert = convert_64_8(thresh)
            final, coordinates = draw_blank_lines(convert, scaled, z)

            os.chdir(r'C:\Users\charl\njit\muscle_imaging\drawn')
            if cv.imwrite(file, final):
                print('done!')
        except Exception as e:
            print(str(e))

def multi_point(starting_slice, number_of_scans, interval):
    dir = 'scans'
    all_points = []
    for file in (os.listdir(dir))[starting_slice:number_of_scans+1:interval]:
        z = int(file[10:len(file)-4])
        f = os.path.join(dir, file)
        image = cv.imread(f)
        cropped = image[100:600, 0:951]
        scaled = cv.pyrDown(cropped)  
        gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
        sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
        blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
        T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
        convert = convert_64_8(thresh)
        final, coordinates = draw_blank_lines(convert, scaled, z)
        all_points.append(coordinates)
    return all_points

def priori(previous_image, current_image):
    current_image = cv.imread(current_image)
    previous_image = cv.imread(previous_image)
    cropped = current_image[100:600, 0:951]


    scaled = cv.pyrDown(cropped)  
    z = 1
    #cropped = image[100:600, 0:951]
    #scaled = cv.pyrDown(cropped)  
    gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
    sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
    blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
    T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
    convert = convert_64_8(thresh)
    final, coordinates = draw_blank_lines(convert, scaled, z)
    cv.imshow(image_path, final)
    cv.waitKey()
    return coordinates

#cropped image dimensions: x=476 y=200


