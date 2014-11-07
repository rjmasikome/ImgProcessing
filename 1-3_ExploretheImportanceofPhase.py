import Image
import numpy as np
import math


#Initialization
img1 = Image.open("bauckhage.jpg")
img2 = Image.open("clock.jpg")

#Fourier transform
fourier1 = np.fft.fft2(img1)
fourier2 = np.fft.fft2(img2)

#Magnitude of 1st image and phase of 2nd image
width, height = img1.size
mag1 = [[] for i in range(height)]
phase2 = [[] for i in range(height)]
for i in range(height):
    for j in range(width):
        mag1[i].append(math.sqrt(fourier1[i][j].real**2+fourier1[i][j].imag**2))
        phase2[i].append(math.atan2(fourier2[i][j].imag,fourier2[i][j].real))

#Generating new Fourier transform function
func_new = [[] for i in range(height)]
for i in range(height):
    for j in range(width):
        re = mag1[i][j]*math.cos(phase2[i][j])
        im = mag1[i][j]*math.sin(phase2[i][j])
        func_new[i].append(complex(re, im))

#Inverse Fourier transform
inverse_new = np.fft.ifft2(func_new)
inverse_new = np.abs(inverse_new)

#Saving the new image
new_img = inverse_new.astype(np.uint8)
result = Image.fromarray(new_img)
result.save('New image.bmp')
print "New image is available"