import serial
import ringbuffer
import numpy as np
import time
import threading
import matplotlib
#matplotlib.use('TKAgg')  # need to use this on OSX for animate w/ blit=True
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D
import globals
from msvcrt import getch





serial_port = serial.Serial('COM3', baudrate=57600, timeout=1)
serial_port.flush()
    
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int('0b' + ''.join(str(e) for e in bits), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
globals.openSeq=False

def returnBitArray(sample):
    bitarray=[]
    if sample is not None:
        for bit in sample:
            if(bit<15):
                bitarray.append(0)
            elif bit>245:
                bitarray.append(1)
            else:
                bitarray.append(2)
    return bitarray





def read_serial_forever():
	while True:
		f = open("sample.txt", 'a') 
		try:
			values=serial_port.read(100)
			if values:
				values=returnBitArray(values)
				try:
					print(str(values),file=f)
				except:
					print("file nf")
				print(str(values))
		except:
			print("Exiting")
			break
		time.sleep(0.01)
	
read_serial_forever()
serial_port.close() # will cause error, forcing close of thread
