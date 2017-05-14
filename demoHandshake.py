import serial
import Analysis.ringbuffer as ringbuffer
import numpy as np
import time
import Analysis.globals as globals
from msvcrt import getch
import sys
BUFFER_SIZE = 1000
data = ringbuffer.RingBuffer(BUFFER_SIZE)
import ctypes




CHAR_BUFFER_SIZE = 16
opening_sequence_checker= ringbuffer.RingBuffer(CHAR_BUFFER_SIZE)
closing_sequence_checker = ringbuffer.RingBuffer(CHAR_BUFFER_SIZE)


serial_port = serial.Serial('COM4', baudrate=int(sys.argv[1]), timeout=1)
serial_port.flush()

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int('0b' + ''.join(str(e) for e in bits), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
globals.openSeq=False

def returnBitArray(sample):
    bitarray=[]
    if sample is not None:
        for bit in sample:
            if(bit<127.5):
                bitarray.append(0)
            elif bit>127.5:
                bitarray.append(1)
            else:
                bitarray.append(2)
    return bitarray
def check_all_ones(buffer, check_bit):
    for bit in buffer.get_samples:
        if bit != check_bit:
            return False
    return True
def check_opening_sequence(buffer):
    #print (list(buffer.get_samples)[::1])
    if list(buffer.get_samples)[::-1] ==[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]:
        return True
    else: 
        return False
    
def check_closing_sequence(buffer):
    if list(buffer.get_samples)[::-1] ==  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]:
        return True
    else:
        return False
def has_invalid(buffer):
    for bit in buffer.get_samples:
        if bit!=0 and bit!=1:
            return True
    return False

message = []
globals.openSeq=False
def read_serial_forever():
    global data
    try :
        for i in range(0,1000):
            while globals.openSeq is False :
                try:
                    values = serial_port.read(1)
                except:
                    print('Exiting thread')
                    break
                if values and len(list(values))==1: 
                    closing_sequence_checker.insert_new(np.array(returnBitArray(values)).astype(np.int))
                    if check_opening_sequence(closing_sequence_checker) == True:
                        #print(" Opening sequence")
                        globals.openSeq= True
                        
                       # time.sleep(0.01)
                        break
                    data.insert_new(np.array(list(values)).astype(np.int))
                #time.sleep(0.01)
            while globals.openSeq is True:
                try:
                    values = serial_port.read(8)
                except:
                    print('Exiting thread')
                    break    
                if values and len(list(values))==8:
                    opening_sequence_checker.insert_new(np.array(returnBitArray(values)).astype(np.int))
                    #print (list(opening_sequence_checker.get_samples)[::-1])
                    if check_closing_sequence(opening_sequence_checker)==True or has_invalid(opening_sequence_checker)==True and len(message)>20:
                        globals.openSeq=False
                        #print ("Closed sequence")
                        print (''.join(message))
                        ctypes.windll.user32.MessageBoxW(0, ''.join(message), "Received: ", 1)
                        exit(0)
                       # time.sleep(0.01)
                        break
                    tmp = np.array(list(values))
                    if check_all_ones(opening_sequence_checker,0)==False:
                        try :
                            # print(text_from_bits(returnBitArray(values)[::-1]))
                            if  int('0b' + ''.join(str(e) for e in (returnBitArray(values)[::-1])), 2) in range(30,124):
                                message.append(text_from_bits(returnBitArray(values)[::-1]))
                        except: 
                            print("",end ='')
                    data.insert_new(tmp.astype(np.int))
                else:
                    print ("Closed sequence because of lack of number of values")
                    globals.openSeq=False
                   # time.sleep(0.01)
                    break

               # time.sleep(0.01)
    except KeyboardInterrupt:
        exit(0)

read_serial_forever()