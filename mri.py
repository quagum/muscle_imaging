import cv2 as cv
import numpy as np
import os

def convert_64_8(image_64): #converts input image of type CV_64F to CV_8U
    image_8 = image_64 - image_64.min() 
    image_8 = image_64 / image_64.max() * 255
    return np.uint8(image_8)

def image_preprocessing(image): #takes image and returns cropped processed image and cropped grayscale image 
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

def draw_line(canvas_image, points, color): #takes canvas_image, points, and color (#,#,#) and returns canvas_image with lines from points
    for x in range(0, len(points)):
        for x1,y1,x2,y2 in points[x]:
            pts = np.array([[x1, y1], [x2, y2]], np.int32)
            cv.polylines(canvas_image, [pts], True, color, 1)
    return canvas_image

def priori(previous_image, current_image): #work in progress
    previous_image = cv.imread(previous_image)
    current_image = cv.imread(current_image)
    pre_pre, prev_scaled = image_preprocessing(previous_image)
    prev_coordinates_2D = generate_data(pre_pre)

    pre_current, curr_scaled = image_preprocessing(current_image)
    te, temp = image_preprocessing(current_image)
    adapted = draw_line(curr_scaled, prev_coordinates_2D, (200, 200, 200))\

    gray = cv.cvtColor(adapted, cv.COLOR_BGR2GRAY)
    sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
    blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
    T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
    convert = convert_64_8(thresh)

    priori_coords = generate_data(convert)
    priori_final = draw_line(temp, priori_coords, (0, 0, 255))

    #priori_coordinates = generate_data('test.jpg')
    #adapted = draw_line(original_pre, priori_coordinates)
 
    cv.imshow("priori_final", priori_final)
    cv.waitKey()

def draw_blank_lines(input_image, canvas, z): #retired
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

def multi_image(scans_folder_name, main_dir, drawn_dir): #takes all scans in scans_folder_name and outputs draw images in drawn_dir which is subdir of main_dir
    dir = scans_folder_name
    for file in os.listdir(dir):
        #os.chdir(r'C:\Users\charl\njit\muscle_imaging')
        os.chdir(main_dir)
        f = os.path.join(dir, file)
        z = int(file[10:len(file)-4])
        try:
            image = cv.imread(f)
            print(f)
            cropped = image[100:600, 0:951]
            scaled = cv.pyrDown(cropped)  
            gray = cv.cvtColor(scaled, cv.COLOR_BGR2GRAY)
            sobel = cv.Sobel(gray, cv.CV_64F, dx=0, dy=1, ksize=3)
            blurred = cv.GaussianBlur(sobel, (31, 31), 0, 1)
            T, thresh = cv.threshold(blurred, 1, 255, cv.THRESH_BINARY)
            convert = convert_64_8(thresh)
            final, coordinates = draw_blank_lines(convert, scaled, z)

            #os.chdir(r'C:\Users\charl\njit\muscle_imaging\drawn')
            os.chdir(drawn_dir)
            if cv.imwrite(file, final):
                print('done!')
        except Exception as e:
            print(str(e))

def multi_point(starting_slice, number_of_scans, interval): #takes all scans in folder and returns array with data points of lines
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

priori('cIMG-0007-00058.jpg', 'cIMG-0007-00059.jpg')
#cropped image dimensions: x=476 y=200

