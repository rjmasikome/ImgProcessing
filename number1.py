#!/usr/bin/python
    rmax=raw_input('Input Rmax : ');
with open('bauckhage.pgm','r') as f:
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

    # process
    array_new = []
    rmin = 30
    rmax = 35
    if
    #Pij = P(i*jmax +j) = Pk
    print array[2]
