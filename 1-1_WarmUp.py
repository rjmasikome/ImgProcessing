#!/usr/bin/python
import Image
import numpy as np

# get rmin and rmax from user
while True :
    rmin=raw_input('Input Rmin : ');
    rmax=raw_input('Input Rmax : ');
    # cast to integer
    rmin = int(rmin)
    rmax = int(rmax)
    if(rmin > rmax):
        print "Rmin should be less than Rmax\n"
    else:
        break

# Initialise variables and arrays
img = Image.open("bauckhage.jpg")
width, height = img.size            # Get width and height from original image
h_half = height/2                   # Make it half
w_half = width/2
i = 0
j = 0

array_new = []                      # Construct and initialise new array for process
for x in range(width*height) :
    array_new.append(x)

img_array = list(img.getdata())     # Convert data from image as array

# Process array
for j in range(height) :
    for i in range(width) :
        if pow(i - w_half,2) + pow(j - h_half,2) >= rmin*rmin:
            if pow(i - w_half,2) + pow(j - h_half,2) <= rmax*rmax :
                array_new[i+j*width] = 0
            else :
                array_new[i+j*width] = img_array[i+j*width]
        else :
            array_new[i+j*width] = img_array[i+j*width]

# Save the image from array
# Parameter in function new
# -- 1 (1-bit pixels, black and white, stored with one pixel per byte)
# -- L (8-bit pixels, black and white)
# -- P (8-bit pixels, mapped to any other mode using a colour palette)
# -- RGB (3x8-bit pixels, true colour)
# -- RGBA (4x8-bit pixels, true colour with transparency mask)
# -- CMYK (4x8-bit pixels, colour separation)
# -- YCbCr (3x8-bit pixels, colour video format)
# -- I (32-bit signed integer pixels)
# -- F (32-bit floating point pixels)

new_img = Image.new('L', (width,height))        
new_img.putdata(array_new)
new_img.save('New_Image.jpg')
print "New image is available"