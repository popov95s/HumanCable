import sys
len = 0
f = open(str(sys.argv[2]), 'a')
with open(str(sys.argv[1]),'r') as read_file:
    #opening sequence
    print('11111111', end= ' ', file=f)
    for line in read_file:
        for bit in line:
            print(bin(ord(bit))[2:].zfill(8)[::-1], end = ' ', file =f)
        
        
    #closing sequence
    print('00000000', end= ' ', file =f)

