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
print "New image is available"

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

width, height = result.size

array_new = []
for x in range(width*height) :
    array_new.append(x)

i = 0
j = 0
h_half = height/2
w_half = width/2

img_array = list(result.getdata())

for i in range(height) :
	for j in range(width) :
		if pow(j - w_half,2) + pow(i - h_half,2) >= rmin*rmin:
			if pow(j - w_half,2) + pow(i - h_half,2) <= rmax*rmax:
				array_new[j+i*width] = img_array[j+i*width]
			else :
				array_new[j+i*width] = 0
		else :
			array_new[j+i*width] = 0

new_img_2 = Image.new('L', (256,256))
new_img_2.putdata(array_new)
new_img_2.save('image_2.bmp')
print "New image_2 is available"

a = np.asarray(new_img_2, dtype=float)

log_res = (a/255)*(log_max-log_min)+log_min

i_log = np.exp(log_res)

ifshift = abs(np.fft.ifft2(i_log))
ifourier = np.fft.ifftshift(ifshift)


new_img_3 = ifourier.astype(np.uint8)

print new_img_3.min()
print new_img_3.max()

result = Image.fromarray(new_img_3)
result.save('image_3.bmp')

#scipy.misc.imsave('outfile.jpg', y)

#c = np.fft.irfft2(i_log)

#j = Image.fromarray(i_log.astype(np.uint8))
#j.save('img2.png')

#ifourier = np.fft.ifft2(new_img_2)

#Take the log of the fourier shift
#spectrum = np.log(np.abs(ifourier))

#Make sure the log scale from 0 to 1
#spectrum = (spectrum - spectrum.min()) / (spectrum.max() - spectrum.min())

#new_img_3 = (spectrum * 255).astype(np.uint8)

#result = Image.fromarray(new_img_3)
#result.save('image_3.jpg')

#scipy.misc.imsave('outfile.jpg', y)
#y.save("new.jpg")
