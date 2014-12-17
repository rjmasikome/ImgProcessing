#!/usr/bin/python

import Image
import numpy as np
import time
import matplotlib.pyplot as plt #use for debugging
import csv

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
    m_array = np.zeros(m_size)
    const = 1 / (np.sqrt(2 * np.pi)* sigma)
    m_radius = m_size / 2;
    
    sum_gauss = 0
    for i in xrange (m_size):
        m_array[i] = const * np.exp(-1 * np.power(i - m_radius,2) / (2 *  sigma * sigma))
        sum_gauss +=  m_array[i]  
    
    m_array = m_array * (1 / sum_gauss)

    return m_array

def image_function_task1(img, m_array, m_size):

    width, height = img.size    # get width and height size
    output = np.zeros(shape=(width,height), dtype=np.int)   # create new array 2d

    img_array = np.asarray(img)
    m_size_half = m_size / 2
    
    output = np.lib.pad(img_array, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'edge')
    output.setflags(write=True)

    for y in xrange(m_size_half,height+m_size_half) :    # traverse and process pixels in image arrays row-wise
        for x in xrange(m_size_half,width+m_size_half) :
            sum_output = 0
            for j in xrange (-m_size_half,m_size_half+1) :
                for i in xrange (-m_size_half,m_size_half+1) :
                    sum_output += output[x - i][y - j] * m_array[m_size_half - i][m_size_half - j]
                sum_output += output[x - i][y - j] * m_array[m_size_half - i][m_size_half - j]
            output[x,y] = sum_output
    return output[m_size_half:width+m_size_half,m_size_half:height+m_size_half]

def convolve1D(arr2,arr1,m_size,length,m_size_h):
    # h = np.fliplr(arr2);
    length_pad = length + m_size - 1

    y = np.zeros(length_pad+m_size);
    for i in xrange(length_pad):
        y[i] = 0;
        for j in xrange(m_size):
            y[i] += arr1[i - j] * arr2[j];

    return y[m_size_h:length+m_size_h]

def image_function_task2(img, m_array, m_size):

    width, height = img.size    # get width and height size
    output = np.zeros(shape=(width,height), dtype=np.float)   # create new array 2d

    img_array = np.asarray(img)
    m_size_half = m_size / 2

    image_buf = np.lib.pad(img_array, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'edge')
    print output.shape
    for x in range(width):
        output[x,:] = convolves1D(m_array,image_buf[x,:], m_size, width, m_size_half)

    output_buf = np.lib.pad(output, ((m_size_half,m_size_half), (m_size_half,m_size_half)), 'edge')
    for y in range(height):
        output[:,y] = convolves1D(m_array,output_buf[:,y], m_size, height, m_size_half)

    return output 

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


def task1(img,m_size,filename_split):
    start = time.time()
    print "Processing Task 1.1..."
    m_array = prepare_mask(m_size)

    image_result1 = image_function_task1(img, m_array, m_size)    # process the image
    new_filename1 = filename_split[0] + "-task1-1." + filename_split[1]    # create filename
    result1 = img_to_file(image_result1, new_filename1)    # save image from array

    elapsed = time.time() - start
    print "Elapsed time: " + str(elapsed)
    append_toFile(elapsed,m_size,1)


def task2(img,m_size,filename_split):
    start = time.time()
    print "Processing Task 1.2..."
    m_array = prepare_mask_2(m_size)

    image_result2 = image_function_task1_2(img, m_array, m_size)
    new_filename2 = filename_split[0] + "-task1-2." + filename_split[1]    # create filename

    result2 = img_to_file(image_result2, new_filename2)    # save image from array

    elapsed = time.time() - start
    print "Elapsed time: " + str(elapsed)
    append_toFile(elapsed,m_size,2)


def task3(img,m_size,filename_split):
    start = time.time()
    print "Processing Task 1.3..."
    m_array = prepare_mask(m_size)

    image_result3 = image_function_task1_3(img, m_array, m_size)    # process the image
    new_filename3 = filename_split[0] + "-task1-3." + filename_split[1]    # create filename

    result3 = img_to_file(image_result3, new_filename3)    # save image from array
    
    elapsed = time.time() - start
    print "Elapsed time: " + str(elapsed)
    append_toFile(elapsed,m_size,3)


def task4(image):

    # The Array of mask size
    maskArray = [3,5,7,9,11,13,15,17,19,21]

    # Get the Array of average runtime for each task
    averageArray1 = getAverage(1, maskArray)
    averageArray2 = getAverage(2, maskArray)
    averageArray3 = getAverage(3, maskArray)

    #Plotting using pyplot
    plt.figure("Running Time vs Mask Size")
    plt.subplot(221),plt.title("Original Image"),plt.imshow(image, cmap = 'gray')
    plt.subplot(222),plt.title("Task 1 Runtime"),plt.ylabel("Time(s)"),plt.plot(maskArray,averageArray1, '-o')
    plt.subplot(223),plt.title("Task 2 Runtime"),plt.xlabel("Mask Size"),plt.ylabel("Time(s)"),plt.plot(maskArray,averageArray2, '-o')
    plt.subplot(224),plt.title("Task 3 Runtime"),plt.xlabel("Mask Size"),plt.ylabel("Time(s)"),plt.plot(maskArray,averageArray3, '-o')

    plt.show()

######## Main Program ########
# img, filename = get_img()

# Temporary for Debug #
filename = "bauckhage.jpg"
img = Image.open(filename)
######################

# Split file name, ex: filename.txt -> var[0] = filename, var[1] = txt
filename_split = filename.split(".")    
m_size = get_mask_size()

# Separating each task to calculate the run time of each process
task1(img,m_size,filename_split)
task2(img,m_size,filename_split)
task3(img,m_size,filename_split)

#Plotting the graph of Average Run Time vs Mask Size
task4(img)

######## End ########