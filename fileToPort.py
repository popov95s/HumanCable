import serial
import sys
serial_port = serial.Serial('COM3', baudrate=int(sys.argv[1]), timeout=1)
serial_port.flush()


while True: 
    with open(sys.argv[2]) as read_file:
        for line in read_file.read().split():
            for bit in read_file:
                if bit.isdigit():
                    serial_port.write(str(bit))
                    print(bit, end =' ')


serial_port.close() # will cause error, forcing close of thread