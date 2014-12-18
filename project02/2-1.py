#!/usr/bin/python

import Image
import numpy as np
import time
import matplotlib.pyplot as plt #use for debugging
import csv
import os

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
        if m_size%2 == 0: print "Mask size should be odd"
        else: return (m_size)

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
    shape=(m_size,m_size)
    sigma=(m_size-1.)/(2.*2.575)
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    h = h/h.sum()
    return h

def prepare_mask_2(m_size):             # Task 1 Number 2
    sigma = (m_size - 1.0) / (2.0 * 2.575)
    m_array = np.zeros(m_size)
    const = 1 / (np.sqrt(2 * np.pi)* sigma)
    m_radius = m_size / 2;
    x= np.ogrid[-m_radius:m_radius+1]
    m_array = const * np.exp(-1 * np.power(x,2) / (2 *  sigma * sigma))
    m_array = m_array / m_array.sum()
    return m_array

def image_function_task1(img, m_array, m_size):
    width, height = img.size    # get width and height size
    output = np.zeros(shape=(width,height), dtype=np.int)   # create new array 2d

    img_array = np.asarray(img)
    m_size_half = m_size / 2

    output = np.lib.pad(img_array, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'edge')
    output.setflags(write=True)
    for y in xrange(m_size_half,height+m_size_half) : 
        for x in xrange(m_size_half,width+m_size_half) :
            sum_output = 0
            for j in xrange (-m_size_half,m_size_half) :
                for i in xrange (-m_size_half,m_size_half) :
                    sum_output += output[x + i][y + j] * m_array[i+m_size_half][j+m_size_half]
            output[x,y] = sum_output
    return output[m_size_half:width+m_size_half,m_size_half:height+m_size_half]

def convolve1D(arr2,arr1,m_size,length):
    length_pad = length + m_size - 1
    y = np.zeros(length_pad+m_size)
    for i in xrange(length_pad):
        y[i] = 0;
        for j in xrange(m_size):
            y[i] += arr1[i - j] * arr2[j]
    return y[0:length_pad]

def image_function_task1_2(img, m_array, m_size):
    width, height = img.size
    output = np.zeros(shape=(width,height), dtype=np.float)   

    img_array = np.asarray(img)
    m_size_half = m_size / 2
    output = np.lib.pad(img_array, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'edge')
    for x in range(width):
        output[x,:] = convolve1D(m_array,output[x,:], m_size, width)
    for y in range(height):
        output[:,y] = convolve1D(m_array,output[:,y], m_size, height)
    return output[m_size-1:width+m_size,m_size-1:height+m_size] 

def image_function_task1_3(img, m_array, m_size):
    img_array = np.asarray(img)

    if m_size%2 == 0:
        img_array_pad = np.lib.pad(img_array, ((m_size/2,m_size/2), (m_size/2,m_size/2)), 'edge')
    else:
        img_array_pad = np.lib.pad(img_array, (((m_size/2)+1,m_size/2), ((m_size/2)+1,m_size/2)), 'edge')

    pad_value = len(img_array_pad) - m_size

    m_array_pad = np.lib.pad(m_array, ((0,pad_value), (0,pad_value)), 'constant', constant_values=0)

    img_fft = np.fft.fft2(img_array_pad)
    m_fft = np.fft.fft2(m_array_pad)
    
    mul_fft = img_fft*m_fft

    #Apply inverse FFT to the new complex function
    new_ifou = np.fft.ifft2(mul_fft)

    #Find the magnitude part of the inversed function to build the image
    output = np.abs(new_ifou)

    return output[m_size:len(img_array_pad),m_size:len(img_array_pad)]

def append_toFile(elapsed, m_size, taskNum):
    #
    # This function is for saving the runtime to File
    #
    directory = "data"+str(taskNum)

    if not os.path.exists(directory):
        os.makedirs(directory)

    outputName = "data"+ str(taskNum) +"/"+ str(m_size) + ".txt"
    with open(outputName, "a") as myfile:
        myfile.write(str(elapsed)+';')


def getAverage(taskNum, maskArray):
    #
    # This function is to get the average runtime from the file
    # Read the whole row and parse it to float
    # and also filter out Empty string
    #
    averageArray = []
    for mask in maskArray :
        filename = "data"+ str(taskNum) +"/" + str(mask) + ".txt"
        results = list(csv.reader(open(filename), delimiter=";"))
        results = filter(None,results[0])
        results = [float(x) for x in results]
        averageArray.append(sum(results)/len(results))

    return averageArray

def getMaskArray(taskNum):
    #
    # This function is to get the file list
    # And return the file name as mask size for graph
    # each mask runtime is stored in different 
    # file name which corresponds to the mask size 
    #
    dirName = "data" + str(taskNum)

    fullname = os.listdir(dirName)
    filelist = []
    for x in range(len(fullname)):
        fileName= os.path.splitext(fullname[x-1])[0]
        filelist.append(fileName)

    filelist = [int(i) for i in filelist]
    filelist.sort()

    return filelist

def task1(img,m_size,filename_split):
    print "Processing Task 1.1..."
    m_array = prepare_mask(m_size)

    start = time.time()
    image_result1 = image_function_task1(img, m_array, m_size)    # process the image
    new_filename1 = filename_split[0] + "-task1-1." + filename_split[1]    # create filename
    result1 = img_to_file(image_result1, new_filename1)    # save image from array

    elapsed = time.time() - start
    print "Elapsed time: " + str(elapsed)
    append_toFile(elapsed,m_size,1)

    return image_result1


def task2(img,m_size,filename_split):
    
    print "Processing Task 1.2..."
    m_array = prepare_mask_2(m_size)

    start = time.time()
    image_result2 = image_function_task1_2(img, m_array, m_size)
    new_filename2 = filename_split[0] + "-task1-2." + filename_split[1]    # create filename

    result2 = img_to_file(image_result2, new_filename2)    # save image from array

    elapsed = time.time() - start
    print "Elapsed time: " + str(elapsed)
    append_toFile(elapsed,m_size,2)

    return image_result2


def task3(img,m_size,filename_split):
    
    print "Processing Task 1.3..."
    m_array = prepare_mask(m_size)

    start = time.time()
    image_result3 = image_function_task1_3(img, m_array, m_size)    # process the image
    new_filename3 = filename_split[0] + "-task1-3." + filename_split[1]    # create filename

    result3 = img_to_file(image_result3, new_filename3)    # save image from array
    
    elapsed = time.time() - start
    print "Elapsed time: " + str(elapsed)
    append_toFile(elapsed,m_size,3)

    return image_result3


def task4(image1, image2, image3):

    # The Array of mask size
    # Get the mask list from each task 1 to task 3
    maskList1 = getMaskArray(1)
    maskList2 = getMaskArray(2)
    maskList3 = getMaskArray(3)

    # Get the Array of average runtime for each task
    averageArray1 = getAverage(1, maskList1)
    averageArray2 = getAverage(2, maskList2)
    averageArray3 = getAverage(3, maskList3)

    #Plotting using pyplot
    plt.figure("Result and Runtime comparison")
    plt.subplot(221),plt.title("Naive Convolution"),plt.imshow(image1, cmap = 'gray')
    plt.subplot(222),plt.title("Separable Convolution"),plt.imshow(image2, cmap = 'gray')
    plt.subplot(223),plt.title("Separable FFT"),plt.imshow(image3, cmap = 'gray')
    plt.subplot(224),plt.title("Runtime"),plt.xlabel("Mask Size"),plt.ylabel("Time(s)"),plt.plot(maskList1,averageArray1, '-o', label="Naive"),plt.plot(maskList2,averageArray2, '-o', label="Separable"),plt.plot(maskList3,averageArray3, '-o', label="FFT"),plt.legend(loc='upper left')
    plt.show()

######## Main Program ########
img, filename = get_img()

##This field is for data generation genData.sh and debug
#filename = "bauckhage.jpg"
#img = Image.open(filename)

# Split file name, ex: filename.txt -> var[0] = filename, var[1] = txt
filename_split = filename.split(".")    
m_size = get_mask_size()

print "Using mask size " + str(m_size) + "x" + str(m_size)

# Separating each task to calculate the run time of each process
img1 = task1(img,m_size,filename_split)
img2 = task2(img,m_size,filename_split)
img3 = task3(img,m_size,filename_split)

#Plotting the graph of Average Run Time vs Mask Size
task4(img1, img2, img3)

######## End ########