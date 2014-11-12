import Image
import numpy as np

def get_img():
    #Get the input file from user
    while True :
        filename=raw_input('Input filename of the image : ');
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
        rmin=raw_input('Input Rmin : ');
        rmax=raw_input('Input Rmax : ');
        # cast to integer
        rmin = int(rmin)
        rmax = int(rmax)
        if(rmin > rmax):
            print "Rmin should be less than Rmax\n"
        else:
            break
    return (rmin, rmax)

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
    img_fshift = np.fft.fftshift(img_fourier)

    #Take the log of the fourier shift
    spectrum = np.log(np.abs(img_fshift))

    log_min = spectrum.min()
    log_max = spectrum.max()

    #Make sure the log scale from 0 to 1
    spectrum = (spectrum - spectrum.min()) / (spectrum.max() - spectrum.min())

    #Make the array from 0 - 255 and cast to integer instead of float
    output = (spectrum * 255).astype(np.uint8)
    return output

def suppress_freq(img, ftt_img, rmin, rmax):
    #Initializing variables and array
    width, height = img.size

    output = np.zeros(shape=(width,height), dtype=np.int)

    i = 0
    j = 0
    h_half = height/2
    w_half = width/2

    for i in range(height):
        for j in range(width):
            if pow(j - w_half,2) + pow(i - h_half,2) >= rmin*rmin:
                if pow(j - w_half,2) + pow(i - h_half,2) <= rmax*rmax:
                    output[i, j] = fft_img[i, j]

    return(output)
##================================================

#Initialization
img, filename = get_img()
filename_split = filename.split(".")

#Calculate Fourier Transfrom of the image
fft_img = fft_process(img)

# Save the image from array
new_filename = filename_split[0] + "-fft." + filename_split[1]
result = img_to_file(fft_img, new_filename)

#Taking the input of Rmin and Rmax
rmin, rmax = get_r_value()

#Calculate suppression of image frequency
suppress_freq_img = suppress_freq(result, fft_img, rmin, rmax)

#Parse the array into image
new_filename = filename_split[0] + "-surpressed." + filename_split[1]
result = img_to_file(suppress_freq_img.astype(np.uint8),new_filename)

'''
#Parse the image into numpy tuppled array and make the value to 1 apart from 0
a = np.asarray(new_img_2, dtype=float)
a = np.ceil(a/a.max())

#Multiply the Shifted fourier transform tuppled array to array a which correspond to third image 
filtered = a*fshift

#Reversing fourier transform
f_ishift = np.fft.ifftshift(filtered)
ifourier = np.fft.ifft2(f_ishift)
ifourier = np.abs(ifourier)

#Saving the image
new_img_3 = ifourier.astype(np.uint8)
result = Image.fromarray(new_img_3)
result.save('image_3.bmp')
print "New image_3 is available"
'''