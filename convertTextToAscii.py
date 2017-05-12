import sys
len = 0
f = open(str(sys.argv[2]), 'a')
with open(str(sys.argv[1]),'r') as read_file:
    #opening sequence
    print('255', end= ' ', file=f)
    for line in read_file:
        # print(' '.join(format(ord(x), 'b') for x in line), end = ' ', file =f)
        # len+=1
        
        for character in line:
            print (ord(character),end= ', ', file=f)
            len+=1
    #closing sequence
    print('0 0 0 0 0 0 0 0', end= ' ', file =f)
print (len)
