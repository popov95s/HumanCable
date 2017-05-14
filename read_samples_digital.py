
import sys
import time
import serial

serial_port = serial.Serial('COM4', baudrate=int(sys.argv[2]), timeout=1)
serial_port.flush()
start_time = time.time()
def read_serial_forever():
	
	f = open("Analysis/" + str(sys.argv[1]), 'a') 
	for i in range(0,50000):
		try:
			values=serial_port.read(1)
			if values:
				try:
					print(int.from_bytes(values, byteorder='big'), end='',file=f)
				except:
					print("file nf")
		except:
			print("Exiting")
			break
	start_time = time.time()	
read_serial_forever()
print (time.time()- start_time)
print ("Done")
serial_port.close()