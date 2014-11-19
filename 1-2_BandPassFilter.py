import Image
from matplotlib import pyplot as plt
import numpy as np

def get_img():
    #Get the input file from user
    while True :
        filename=raw_input('Input filename of the image : ')
        try:
            with open(filename) as file:
             output = Image.open(filename)
             break
        except IOError as e:
            print "Unable to open file"
    return (output, filename)

def get_r_value():
    #Get rmin and rmax values form user
    while True :
        rmin=raw_input('Input Rmin : ')
        rmax=raw_input('Input Rmax : ')
        # cast to integer
        rmin = int(rmin)
        rmax = int(rmax)
        if(rmin > rmax):
            print "Rmin should be less than Rmax\n"
        else:
            break
    return (rmin, rmax)

def normalize(number):
    number = np.abs(number)
    number = (number - number.min()) / (number.max() - number.min())
    output = (number * 255).astype(np.uint8)
    
    return output

def img_to_file(img, filename):
    #Save image into a file
    output = Image.fromarray(img)
    output.save(filename)
    print filename + " is created"
    return output

def fft_process(img):
    #Calculate Fourier Transform of the image

    #Fourier transform
    img_fourier = np.fft.fft2(img)

    #Fourier shift
    output = np.fft.fftshift(img_fourier)

    return output

def log_of_fft(img_fshift):
    #Take the log of the fourier shift
    spectrum = np.log1p(np.abs(img_fshift))

    output = normalize(spectrum)

    return output

def suppress_freq(img_fshift, rmin, rmax):
    #Initializing variables and array
    width, height = np.shape(img_fshift)

    output = img_fshift

    i = 0
    j = 0
    h_half = height/2
    w_half = width/2


    for i in range(height):
        for j in range(width):
            if (pow(j - w_half,2) + pow(i - h_half,2) < rmin*rmin) or (pow(j - w_half,2) + pow(i - h_half,2) > rmax*rmax):
                    output[j, i] = 0
    return output

def ifft_process(img_fshift):
    #Reversing fourier transform
    f_ishift = np.fft.ifftshift(img_fshift)
    ifourier = np.fft.ifft2(f_ishift)

    output = normalize(ifourier)

    return output
    

##================================================

#Initialization
img, filename = get_img()
filename_split = filename.split(".")

#Taking the input of Rmin and Rmax
rmin, rmax = get_r_value()

#Calculate Fourier Transfrom of the image
img_fshift = fft_process(img)
img_log_fft = log_of_fft(img_fshift)

# Save the image from array
new_filename = filename_split[0] + "-log_fft." + filename_split[1]
result = img_to_file(img_log_fft, new_filename)

#Calculate suppression of image frequency
suppress_freq_img = suppress_freq(img_fshift, rmin, rmax)
log_sup_img = log_of_fft(suppress_freq_img)

#Save the image from array
new_filename = filename_split[0] + "-surpressed." + filename_split[1]
result = img_to_file(log_sup_img,new_filename)

#Calculate inverse fft to get the final result
img_back = ifft_process(suppress_freq_img)

#Save the image from array
new_filename = filename_split[0] + "-back." + filename_split[1]
result = img_to_file(img_back, new_filename)

#Visualization with plot
plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.subplot(222),plt.imshow(img_log_fft, cmap = 'gray')
plt.subplot(223),plt.imshow(log_sup_img, cmap = 'gray')
plt.subplot(224),plt.imshow(img_back, cmap = 'gray')
plt.show()
