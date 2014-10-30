import Image
import numpy as np


#Initialization
img = Image.open("bauckhage.jpg")

#Fourier transform
fourier = np.fft.fft2(img)

#Fourier shift
fshift = np.fft.fftshift(fourier)

#Take the log of the fourier shift
spectrum = np.log(np.abs(fshift))

log_min = spectrum.min()
log_max = spectrum.max()

#Make sure the log scale from 0 to 1
spectrum = (spectrum - spectrum.min()) / (spectrum.max() - spectrum.min())

#Make the array from 0 - 255 and cast to integer instead of float
new_img = (spectrum * 255).astype(np.uint8)

# Save the image from array
result = Image.fromarray(new_img)
result.save('image_1.bmp')
print "New image_1 is available"

#Taking the input of Rmin and Rmax
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

#Initializing variables and array
width, height = result.size

array_new = []
for x in range(width*height) :
    array_new.append(x)

i = 0
j = 0
h_half = height/2
w_half = width/2

img_array = list(result.getdata())

#Put on the loop the needed calculation
for i in range(height) :
    for j in range(width) :
        if pow(j - w_half,2) + pow(i - h_half,2) >= rmin*rmin:
            if pow(j - w_half,2) + pow(i - h_half,2) <= rmax*rmax:
                array_new[j+i*width] = img_array[j+i*width]
            else :
                array_new[j+i*width] = 0
        else :
            array_new[j+i*width] = 0

#Parse the array into image
new_img_2 = Image.new('L', (256,256))
new_img_2.putdata(array_new)
new_img_2.save('image_2.bmp')
print "New image_2 is available"

#Parse the image into umpy tuppled array and make the value to 1 apart from 0
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