# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 15:40:04 2014

@author: Ying
"""
from PIL import Image
import numpy as np
import scipy.signal


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
    
def getgauss2D(size):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    shape=(size,size)
    sigma=(size-1.)/(2.*2.575)
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    h = h / (2 * np.pi * sigma * sigma)
    print h
    return h    
    
    
    ######## Main Program ########
# img, filename = get_img()

# Temporary ######
filename = "bauckhage.jpg"
img = Image.open(filename)
######################


filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt
size= get_mask_size()
x = getgauss2D(size)

y = np.empty_like(x)
y[:, :-1] = (x[:, 1:] - x[:, :-1]) 
y[:, -1] = -x[:, -1] 
grady=scipy.signal.convolve2d(img,y)

z = np.empty_like(x)
z[:-1,: ] = (x[1:, :] - x[:-1, :]) 
z[-1,: ] = -x[-1, :] 
gradx=scipy.signal.convolve2d(img,z)


gradmag=(gradx**2+grady**2)**0.5

new_filename = filename_split[0] + "-task2." + filename_split[1]    # create filename

result = img_to_file(gradmag, new_filename)
