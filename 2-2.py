from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd
import scipy.signal as sg

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
    return h

def getgauss1D(m_size):             # Task 1 Number 2
    sigma = (m_size - 1.0) / (2.0 * 2.575)
    m_array = np.zeros(m_size)
    const = 1 / (np.sqrt(2 * np.pi)* sigma)
    m_radius = m_size / 2;

    sum_gauss = 0
    for i in xrange (m_size):
        m_array[i] = const * np.exp(-1 * np.power(i - m_radius,2) / (2 *  sigma * sigma))
        sum_gauss +=  m_array[i]

    m_array = m_array * (1 / sum_gauss)

    return m_array

# def getgauss1D(size):
#     sigma =(size-1.0)/(2.0*2.575)
#     halfsize = np.floor(size/2.0)
#     x= np.ogrid[-halfsize:halfsize+1]
#     h = np.exp(-x**2/(2.0*np.pi**2))
#     h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
#     h = h/h.sum()
#     #h = h / (np.sqrt(2.0*np.pi)*sigma) #norm1
#     #h2 = h
#     #print h1
#     #print h2
#     #plt.plot(x,h1)
#     #plt.plot(x,h2)
#     #plt.show()
#     return h

def getgaussderiv1d(input1d):
    output = np.convolve(input1d, [1, -1],mode="same")
    return output

def getgaussderiv2d(input2d):

    x = input2d
    y = np.empty_like(x)
    y[:, :-1] = (x[:, 1:] - x[:, :-1])
    y[:, -1] = -x[:, -1]

    z = np.empty_like(x)
    z[:-1,: ] = (x[1:, :] - x[:-1, :])
    z[-1,: ] = -x[-1, :]
    return y,z

    # [width, height] = input2d.shape
    # outputX = np.zeros(shape=(width,height), dtype=np.float)
    # outputY = np.zeros(shape=(width,height), dtype=np.float)
    # for x in range(width):
    #     #outputX[x,:] = np.convolve(input2d[x,:], [1, -1],mode="same")
    #     outputX[x,:] = np.convolve(input2d[x,:], [1, 0, -1],mode="same")
    #
    # for x in range(height):
    #     # outputY[:,x] = np.convolve(input2d[:,x], [1, -1],mode="same")
    #     outputY[:,x] = np.convolve(input2d[:,x], [1,0, -1],mode="same")
    #return [outputX, outputY]


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

#==================
#gauss 1d
gauss1 = getgauss1D(size)

#get derivative of gaussian
gaussderiv = getgaussderiv1d(gauss1)

#create gradient magnitude image based on gaussian1d
gradx = np.zeros(shape=(width,height), dtype=np.float)
grady = np.zeros(shape=(width,height), dtype=np.float)
for x in range(width):
    gradx[x,:] = np.convolve(gaussderiv,img_array[x,:], mode='same')
for x in range(height):
    gradx[:,x] = np.convolve(gauss1,gradx[:,x], mode='same')

for y in range(width):
    grady[y,:] = np.convolve(gauss1,img_array[y,:], mode='same')
for y in range(height):
    grady[:,y] = np.convolve(gaussderiv,grady[:,y], mode='same')
gradmag = np.sqrt(gradx**2 + grady**2)


#save into a jpeg file
gradmag_norm = normalize(gradmag)
new_filename = filename_split[0] + "-task2_gauss1d." + filename_split[1]    # create filename
result = img_to_file(gradmag_norm, new_filename)

#####
# #TEMPORARY (for DEBUG purpose only)
plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.subplot(222),plt.imshow(gradmag, cmap = 'gray')
plt.subplot(223),plt.imshow(gradx, cmap = 'gray')
plt.subplot(224),plt.imshow(grady, cmap = 'gray')
plt.show()
######

#==================
#gauss 2d
gauss2 = getgauss2D(size)

#create gradient magnitude image based on gaussian2d directly
[gaussderiv2X, gaussderiv2Y] = getgaussderiv2d(gauss2)
grady=sg.convolve2d(img,gaussderiv2X)
gradx=sg.convolve2d(img,gaussderiv2Y)

gradmag_norm = normalize(gradmag)
new_filename = filename_split[0] + "-task2_gauss2d." + filename_split[1]    # create filename
result = img_to_file(gradmag_norm, new_filename)



#####
# #TEMPORARY (for DEBUG purpose only)
# gauss2d = np.zeros(shape=(size,size), dtype=np.float)
# a = np.outer(gauss1, gauss1)
# gauss2d = a / a.sum()
# print "gauss2d from 1d"
# print gauss2d
# print "\n"
# print "gauss2d(original equation)"
# print getgauss2D(size)
######

