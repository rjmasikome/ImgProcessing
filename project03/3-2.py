#!/usr/bin/python
import Image
import numpy as np
import math as m

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
        filename='bauckhage.jpg';#raw_input('Input filename of the image : ');
        try:
            with open(filename) as file:
             output = Image.open(filename)
             break
        except IOError as e:    # throw exception if image file cannot be opened
            print "Unable to open file"
    return (output, filename)

def process_image(img, img_new, amp_x, freq_x, ph_x, amp_y, freq_y, ph_y):
#
#     Get radius minimum and maximum value for image function
#     Rmin (radius minimum) should be less than Rmax (radius maximum)
#     returns: rmin = radius minimum
#              rmax = radius maximum
#
    width, height = img.size
    w, h = img_new.shape
    img_array = np.asarray(img)

    for y in range(height) :    # traverse and process pixels in image arrays row-wise
        for x in range(width) :
             delta_x = amp_x * m.sin((y*freq_x*m.pi/180)- ph_x)
             delta_y = amp_y * m.sin((x*freq_y*m.pi/180)- ph_y)

             x_new = delta_x + width/2
             y_new = delta_y + height/2

             if (x_new < w) or (x_new > 0):
                if (y_new < h) or (y_new > 0):
                    img_new[x+x_new, y+y_new] = img_array[x,y]

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


######## Main Program ########
img, filename = get_img()
filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt

w,h = img.size;

image_result = np.zeros(shape=(w*2,h*2), dtype=np.int) 

process_image(img, image_result, 10, 5, 0, 10, 5, 0);


new_filename = filename_split[0] + "-3." + filename_split[1]    # create filename
result = img_to_file(image_result, new_filename)    # save image from array

######## End ########
