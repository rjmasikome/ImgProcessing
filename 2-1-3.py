#!/usr/bin/python

import Image
import numpy as np
import matplotlib.pyplot as plt

def get_img():
    while True :
        filename = raw_input('Input filename of the image : ');
        try:
            with open(filename) as file:
             output = Image.open(filename)
             break
        except IOError as e:
            print "Unable to open file"
    return (output, filename)

def get_mask_size():
    while True :
        m_size = raw_input('Input Mask Size : ');
        m_size = int(m_size)
        return (m_size)

def img_to_file(img, filename):
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
    return m_array


def image_function_task1_3(img, m_array, m_size):

    width, height = img.size    # get width and height size
    
    img_array = np.asarray(img)
    m_array = np.lib.pad(m_array, ((0,241), (0,241)), 'constant', constant_values=0)

    img_fft = np.fft.fft2(img_array)
    m_fft = np.fft.fft2(m_array)

    mul_fft = img_fft*m_fft

    #Apply inverse FFT to the new complex function
    new_ifou = np.fft.ifft2(mul_fft)

    #Find the magnitude part of the inversed function to build the image
    output = np.abs(new_ifou)

    return output[m_size:width,m_size:width]


######## Main Program ########
img, filename = get_img()
filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt

m_size = get_mask_size()

m_array = prepare_mask(m_size)

image_result = image_function_task1_3(img, m_array, m_size)    # process the image
print image_result
plt.imshow(image_result)
plt.gray()
plt.show()
new_filename = filename_split[0] + "-task2-1-3." + filename_split[1]    # create filename
result = img_to_file(image_result, new_filename)    # save image from array

######## End ########
