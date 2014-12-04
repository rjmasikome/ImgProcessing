#!/usr/bin/python

import Image
import numpy as np
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

def prepare_mask(m_size):
    sigma = (m_size - 1.0) / (2.0 * 2.575)
    m_array = np.zeros((m_size,m_size))
    const = 1 / (2 * np.pi * sigma * sigma)
    print sigma*sigma
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

def image_function_task1(img, m_array, m_size):

    width, height = img.size    # get width and height size

    output = np.zeros(shape=(width,height), dtype=np.int)   # create new array 2d

    img_array = np.asarray(img)
    m_size_half = m_size / 2
    output = img_array;
    np.lib.pad(output, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'minimum')
    output.setflags(write=True)
    output.shape
    
    for y in xrange(m_size_half+1,height-m_size_half) :    # traverse and process pixels in image arrays row-wise
        for x in xrange(m_size_half+1,width-m_size_half) :
            sum_output = 0
            for j in xrange (-m_size_half,m_size_half+1) :
                for i in xrange (-m_size_half,m_size_half+1) :
                    sum_output += output[x - i][y - j] * m_array[m_size_half - i][m_size_half - j]
                sum_output += output[x - i][y - j] * m_array[m_size_half - i][m_size_half - j]
            output[x,y] = sum_output
    return output[m_size_half+1:width-m_size_half,m_size_half+1:width-m_size_half]



######## Main Program ########
img, filename = get_img()
filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt

m_size = get_mask_size()

m_array = prepare_mask(m_size)

image_result = image_function_task1(img, m_array, m_size)    # process the image
print image_result
plt.imshow(image_result)
plt.gray()
plt.show()
new_filename = filename_split[0] + "-task2-1." + filename_split[1]    # create filename
result = img_to_file(image_result, new_filename)    # save image from array

######## End ########
