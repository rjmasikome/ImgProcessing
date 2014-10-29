#!/usr/bin/python
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

with open('bauckhage.pgm','r') as f:
# Parsing file pgm
    # marker
    read_var = f.read(3)
    # image width
    width = f.read(3)
    width = int(width)
    # space
    read_var = f.read(1)
    # image height
    height = f.read(3)
    height = int(height)
    # offset
    read_var = f.read(5)

    # print image width and height
    print 'Image Width\t: ' + str(width)
    print 'Image Height\t: ' + str(height)

    # initialize and get byte array
    array = []
    while True:
        read_var = f.read(1)
        #print read_var
        try :
            int_read_var = int(read_var.encode('hex'),16)
            array.append(int_read_var)
        except :
            break

# Process
# initialize new array
array_new = []
for x in range(width*height) :
    array_new.append(x)

# initialize variable
i = 0
j = 0
h_half = height/2
w_half = width/2

for j in range(height) :
    for i in range(width) :
        if pow(i - w_half,2) + pow(j - h_half,2) >= rmin*rmin:
            if pow(i - w_half,2) + pow(j - h_half,2) <= rmax*rmax :
                array_new[i+j*width] = 0
            else :
                array_new[i+j*width] = array[i+j*width]
        else :
            array_new[i+j*width] = array[i+j*width]

# create new file
with open('bauckhage_new.pgm','w') as f:
    f.write("P5\n")
    f.write("%d %d\n" % (width, height))
    f.write("255\n")
    for item in array_new:
      f.write(chr(item))
