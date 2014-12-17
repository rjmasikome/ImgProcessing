from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd

def normalize(number):
    number = np.abs(number)
    number = (number - number.min()) / (number.max() - number.min())
    output = (number * 255).astype(np.uint8)

    return output

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
    h = h/h.sum()
    #h = h / (2 * np.pi * sigma * sigma)
    #print h
    return h


def getgauss1D(size):
    sigma =(size-1.0)/(2.0*2.575)
    halfsize = np.floor(size/2.0)
    x= np.ogrid[-halfsize:halfsize+1]
    h = np.exp(-x**2/(2.0*np.pi**2))
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    h = h/h.sum()
    #h = h / (np.sqrt(2.0*np.pi)*sigma) #norm1
    #h2 = h
    #print h1
    #print h2
    #plt.plot(x,h1)
    #plt.plot(x,h2)
    #plt.show()
    return h

def getgaussderiv1d(input1d):
    output = np.convolve(input1d, [1, -1],mode="same")
    return output

######## Main Program ########
# img, filename = get_img()

# Temporary ######
filename = "bauckhage.jpg"
img = Image.open(filename)
######################

filename_split = filename.split(".")    # split file name, ex: filename.txt -> var[0] = filename, var[1] = txt
size=get_mask_size()
width, height = img.size
img_array = np.asarray(img)

#gauss 1d
gauss1 = getgauss1D(size)

#get derivative of gaussian
gaussderiv = getgaussderiv1d(gauss1)

#create gradient magnitude image
gradx = np.zeros(shape=(width,height), dtype=np.float)
grady = np.zeros(shape=(width,height), dtype=np.float)
for x in range(width):
    gradx[x,:] = np.convolve(gaussderiv,img_array[x,:], mode='same')
for y in range(height):
    grady[:,y] = np.convolve(gaussderiv,img_array[:,y], mode='same')
gradmag = np.sqrt(gradx**2 + grady**2)


#save into a jpeg file
gradmag_norm = normalize(gradmag)
new_filename = filename_split[0] + "-task2." + filename_split[1]    # create filename
result = img_to_file(gradmag_norm, new_filename)


plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.subplot(222),plt.imshow(gradmag, cmap = 'gray')
plt.subplot(223),plt.imshow(gradx, cmap = 'gray')
plt.subplot(224),plt.imshow(grady, cmap = 'gray')
plt.show()


#####
#TEMPORARY (for DEBUG purpose only)
gauss2d = np.ones(shape=(size,size), dtype=np.float)
a = np.zeros(shape=(size,size), dtype=np.float)
for x in range(size):
    a[x,:] = np.convolve(gauss1[x],gauss1,mode='same')
gauss2d = a / a.sum()
print "gauss2d from 1d"
print gauss2d
print "\n"
print "gauss2d(original equation)"
print getgauss2D(size)
######

