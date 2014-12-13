#!/usr/bin/python

import Image
import numpy as np
import time
import matplotlib.pyplot as plt #use for debugging

def get_img():
#
#     Function to get the image file name from user.
#     Image file should be in the same folder with this script file
#     User input image file name with extension.
#     Example : clock.jpg
#     returns: output = Image file
#              filename = Image filename
#
    while True :
        filename = raw_input('Input filename of the image : ');
        try:
            with open(filename) as file:
             output = Image.open(filename)
             break
        except IOError as e:    # throw exception if image file cannot be opened
            print "Unable to open file"
    return (output, filename)

def get_mask_size():
#
#     Get radius minimum and maximum value for image function
#     Rmin (radius minimum) should be less than Rmax (radius maximum)
#     returns: rmin = radius minimum
#              rmax = radius maximum
#
    while True :
        m_size = raw_input('Input Mask Size : ');
        m_size = int(m_size)
        return (m_size)

def img_to_file(img, filename):
#
#     Convert and save array of image to the image file
#     Input  : img = array of image
#            : filename = file name in string
#     returns: output = Image file
#
    output = Image.fromarray(img.astype(np.uint8))
    output.save(filename)
    print filename + " is created"
    return output

def prepare_mask(m_size):           # Task 1 Number 1
    sigma = (m_size - 1.0) / (2.0 * 2.575)
    m_array = np.zeros((m_size,m_size))
    const = 1 / (2 * np.pi * sigma * sigma)

    m_radius = m_size / 2;
    sum_gauss = 0
    for x in range (m_size):
        for y in range (m_size):
            m_array[x,y] = const * np.exp(-1 * (np.power(x - m_radius,2)+np.power(y - m_radius,2)) / (2 *  sigma * sigma))
            sum_gauss = sum_gauss + m_array[x,y]
    # normalize
    for x in range(m_size):
        for y in range(m_size):
            m_array[x,y] = m_array[x,y] * (1 / sum_gauss)
    return m_array

def prepare_mask_2(m_size):             # Task 1 Number 2
    sigma = (m_size - 1.0) / (2.0 * 2.575)
    m_array = np.zeros((m_size,m_size))

    const = 1 / (np.sqrt(2 * np.pi)* sigma)

    m_radius = m_size / 2;
    
    sum_gauss = 0
    for y in range (m_size):
        for x in range (m_size):
            m_array[x,y] = const * np.exp(-1 * np.power(x - m_radius,2) / (2 *  sigma * sigma))
            
    for x in range (m_size):
        for y in range (m_size):
            m_array[x,y] *= const * np.exp(-1 * np.power(y - m_radius,2) / (2 *  sigma * sigma))
            sum_gauss = sum_gauss + m_array[x,y]
    
    # normalize
    for x in range(m_size):
        for y in range(m_size):
            m_array[x,y] = m_array[x,y] * (1 / sum_gauss)
    return m_array


def image_function_task1(img, m_array, m_size):

    width, height = img.size    # get width and height size
    output = np.zeros(shape=(width,height), dtype=np.int)   # create new array 2d

    img_array = np.asarray(img)
    m_size_half = m_size / 2
    print m_size_half
    # output = img_array;
    output = np.lib.pad(img_array, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'edge')
    output.setflags(write=True)
    output.shape
    print output
    for y in xrange(m_size_half,height-m_size_half+1) :    # traverse and process pixels in image arrays row-wise
        for x in xrange(m_size_half,width-m_size_half+1) :
            sum_output = 0
            for j in xrange (-m_size_half,m_size_half+1) :
                for i in xrange (-m_size_half,m_size_half+1) :
                    sum_output += output[x - i][y - j] * m_array[m_size_half - i][m_size_half - j]
                sum_output += output[x - i][y - j] * m_array[m_size_half - i][m_size_half - j]
            output[x,y] = sum_output
    return output[m_size_half:width+m_size_half,m_size_half:height+m_size_half]


def image_function_task1_3(img, m_array, m_size):

    start = time.time()

    width, height = img.size    # get width and height size
    
    img_array = np.asarray(img)

    pad_value = 256 - m_size

    m_array = np.lib.pad(m_array, ((0,pad_value), (0,pad_value)), 'constant', constant_values=0)

    img_fft = np.fft.fft2(img_array)
    m_fft = np.fft.fft2(m_array)

    mul_fft = img_fft*m_fft

    #Apply inverse FFT to the new complex function
    new_ifou = np.fft.ifft2(mul_fft)

    #Find the magnitude part of the inversed function to build the image
    output = np.abs(new_ifou)

    elapse = time.time()

    print elapse-start

    return output[m_size:width,m_size:width]    

######## Main Program ########
# img, filename = get_img()

# Temporary ######
filename = "bauckhage.jpg"
img = Image.open(filename)
######################


filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt

m_size = get_mask_size()

print "Processing masks..."

m_array = prepare_mask(m_size)
m_array2 = prepare_mask_2(m_size)

print "Processing Task 1.1..."

image_result1 = image_function_task1(img, m_array, m_size)    # process the image
new_filename1 = filename_split[0] + "-task1-1." + filename_split[1]    # create filename

print "Processing Task 1.2..."

image_result2 = image_function_task1(img, m_array2, m_size)
new_filename2 = filename_split[0] + "-task1-2." + filename_split[1]    # create filename

print "Processing Task 1.3..."

image_result3 = image_function_task1_3(img, m_array, m_size)    # process the image
new_filename3 = filename_split[0] + "-task1-3." + filename_split[1]    # create filename

result1 = img_to_file(image_result1, new_filename1)    # save image from array
result2 = img_to_file(image_result2, new_filename2)    # save image from array
result3 = img_to_file(image_result3, new_filename3)    # save image from array




######## End ########
