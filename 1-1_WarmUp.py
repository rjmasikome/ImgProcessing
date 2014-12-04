#!/usr/bin/python
import Image
import numpy as np

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

def get_r_value():
#
#     Get radius minimum and maximum value for image function
#     Rmin (radius minimum) should be less than Rmax (radius maximum)
#     returns: rmin = radius minimum
#              rmax = radius maximum
#
    while True :
        rmin = raw_input('Input Rmin : ');
        rmax = raw_input('Input Rmax : ');

        rmin = int(rmin)    # cast rmin value to integer
        rmax = int(rmax)    # cast rmax value to integer

        if(rmin > rmax):    # check rmin and rmax condition
            print "Rmin should be less than Rmax\n"
        else:
            break
    return (rmin, rmax)

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

def image_function_task1(img, rmin, rmax):
#
#     Mapping every pixels in the image with this function :
#     _G(x,y) = 0     , if rmin <= ||(x,y) - (w/2,h/2)|| <= rmax
#     _G(x,y) = G(x,y), if otherwise
#     Input  : img = array of image
#              rmin = radius minimum value
#              rmax = radius maximum value
#     returns: output = Image file
#
    width, height = img.size    # get width and height size

    output = np.zeros(shape=(width,height), dtype=np.int)   # create new array 2d with dimension
                                                            # width x height and integer datatype 
    i = 0   # initialize increment variable
    j = 0
    h_half = height/2   # initialize constant requirement
    w_half = width/2

    img_array = np.asarray(img)

    for j in range(height) :    # traverse and process pixels in image arrays row-wise
        for i in range(width) :
            if pow(i - w_half,2) + pow(j - h_half,2) >= rmin*rmin:
                if pow(i - w_half,2) + pow(j - h_half,2) <= rmax*rmax :
                    output[i, j] = 0
                else :
                    output[i, j] = img_array[i, j]
            else :
                output[i, j] = img_array[i, j]
    return output

######## Main Program ########
img, filename = get_img()
filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt

rmin, rmax = get_r_value()

image_result = image_function_task1(img, rmin, rmax)    # process the image

new_filename = filename_split[0] + "-task1." + filename_split[1]    # create filename
result = img_to_file(image_result, new_filename)    # save image from array

######## End ########
