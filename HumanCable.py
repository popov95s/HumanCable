import serial
import Analysis.ringbuffer as ringbuffer
import numpy as np
import time
import threading
import matplotlib
#matplotlib.use('TKAgg')  # need to use this on OSX for animate w/ blit=True
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D
import Analysis.globals as globals
from msvcrt import getch
import sys
BUFFER_SIZE = 500
data = ringbuffer.RingBuffer(BUFFER_SIZE)

CHAR_BUFFER_SIZE = 8
opening_sequence_checker= ringbuffer.RingBuffer(CHAR_BUFFER_SIZE)
closing_sequence_checker = ringbuffer.RingBuffer(CHAR_BUFFER_SIZE)

# setup the figure to plot with
fig = plt.figure()

# setup the plot
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_xlim(0, BUFFER_SIZE-1)
ax1.set_ylim(0, 255)
line1 = Line2D([], [], color='red', linewidth=0.5)
ax1.add_line(line1)

serial_port = serial.Serial('COM3', baudrate=int(sys.argv[1]), timeout=1)
serial_port.flush()

def isTouching(sample):
    if sample < 1.0:
        print(" No event")
    elif sample < 3.0:
        print(" Hover")
    elif sample < 7.0:
        print(" Touched shield")
    elif sample < 100.0:
        print(" Wire touch")
    
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
            elif bit>220:
                bitarray.append(1)
            else:
                bitarray.append(2)
    return bitarray
# initialization, plot nothing (this is also called on resize)
def init():
    # called on first plot or redraw
    line1.set_data([], [])  # just draw blank background
    return line1,


# animation function.  This is called sequentially, after calling plt.show() (on main thread)
def animate(i):
    # generate some data to draw
    y=data.get_samples
    x = np.linspace(0, BUFFER_SIZE-1, BUFFER_SIZE)
    line1.set_data(x, y)
    # return line(s) to be drawn
    return line1,

def check_all_ones(buffer, check_bit):
    for bit in buffer.get_samples:
        if bit != check_bit:
            return False
    return True
def check_opening_sequence(buffer):
    print (list(buffer.get_samples)[::1])
    if list(buffer.get_samples)[::-1] ==[1,1,1,1,1,1,1,1]:
        return True
    else: 
        return False
    
def check_closing_sequence(buffer):
    if list(buffer.get_samples)[::-1] ==  [0,0,0,0,0,0,0,0]:
        return True
    else:
        return False
def has_invalid(buffer):
    for bit in buffer.get_samples:
        if bit!=0 and bit!=1:
            return True
    return False

def read_serial_forever():
    global data
    try :
        while True:
            while globals.openSeq is False :
                try:
                    values = serial_port.read(1)
                except:
                    print('Exiting thread')
                    break
                if values and len(list(values))==1: 
                    closing_sequence_checker.insert_new(np.array(returnBitArray(values)).astype(np.int))
                    if check_opening_sequence(closing_sequence_checker) == True:
                        print(" Opening sequence")
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
                    print (list(opening_sequence_checker.get_samples)[::-1])
                    if check_closing_sequence(opening_sequence_checker)==True or has_invalid(opening_sequence_checker)==True:
                        globals.openSeq=False
                        print ("Closed sequence")
                       # time.sleep(0.01)
                        break
                    tmp = np.array(list(values))
                    #isTouching(np.std(tmp))
                    if check_all_ones(opening_sequence_checker,1)==False:
                        try :
                            print(text_from_bits(returnBitArray(values)[::-1]))
                        except: 
                            print("")
                    data.insert_new(tmp.astype(np.int))
                else:
                    print ("Closed sequence because of lack of number of values")
                    globals.openSeq=False
                   # time.sleep(0.01)
                    break

               # time.sleep(0.01)
    except KeyboardInterrupt:
        exit(0)
t = threading.Thread(target=read_serial_forever, args=())
t.start()

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig,  # the figure to use
                               animate,  # the function to call
                               init_func=init,  # the function to init the drawing with
                               frames=200,  # the max value of "i" in the animate function, before resetting
                               interval=20,  # 20 ms between each call
                               blit=True)  # do not redraw anything that stays the same between animations

plt.show()

serial_port.close() # will cause error, forcing close of thread
t.join() # wait for thread to exit