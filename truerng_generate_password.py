#!/usr/bin/python3

# TrueRNG Read - Create Password from TrueRNG input
# Chris K Cockrum
# 7/23/20
#
# Requires Python 3.8, pyserial
#
# On Linux - may need to be root or set /dev/tty port permissions to 666
#
# Python 3.8.xx is available here: https://www.python.org/downloads/
# Install Pyserial package with:   python -m pip install pyserial

import serial
import os
import time
import math
from serial.tools import list_ports

# Number of random characters to generate
NUMBER_OF_CHARACTERS = 20 

# Set com port to default None
rng_com_port = None

# Set mode (only has effect on TrueRNGpro and TrueRNGproV2)
capture_mode = 'MODE_NORMAL'

########################
# Function: modeChange #
########################
# Supported Modes
# MODE_NORMAL       300       /* Streams combined + Mersenne Twister */
# MODE_PSDEBUG      1200      /* PS Voltage in mV in ASCII */
# MODE_RNGDEBUG     2400      /* RNG Debug 0x0RRR 0x0RRR in ASCII */
# MODE_RNG1WHITE    4800      /* RNG1 + Mersenne Twister */
# MODE_RNG2WHITE    9600      /* RNG2 + Mersenns Twister*/
# MODE_RAW_BIN      19200     /* Raw ADC Samples in Binary Mode */
# MODE_RAW_ASC      38400     /* Raw ADC Samples in Ascii Mode */
# MODE_UNWHITENED   57600     /* Unwhitened RNG1-RNG2 (TrueRNGproV2 Only) */
# MODE_NORMAL_ASC   115200    /* Normal in Ascii Mode (TrueRNGproV2 Only) */
# MODE_NORMAL_ASC_SLOW 230400    /* Normal in Ascii Mode - Slow for small devices (TrueRNGproV2 Only) */
def modeChange(MODE, PORT):
    # "Knock" Sequence to activate mode change
    ser = serial.Serial(port=PORT,baudrate=110,timeout=1)
    time.sleep(0.5)
    ser.close()
    ser = serial.Serial(port=PORT,baudrate=300,timeout=1)
    ser.close()
    ser = serial.Serial(port=PORT,baudrate=110,timeout=1)
    ser.close()
    if MODE=='MODE_NORMAL':
        ser = serial.Serial(port=PORT,baudrate=300,timeout=1)
    if MODE=='MODE_PSDEBUG':
        ser = serial.Serial(port=PORT,baudrate=1200,timeout=1)
    if MODE=='MODE_RNGDEBUG':
        ser = serial.Serial(port=PORT,baudrate=2400,timeout=1)
    if MODE=='MODE_RNG1WHITE':
        ser = serial.Serial(port=PORT,baudrate=4800,timeout=1)
    if MODE=='MODE_RNG2WHITE':
        ser = serial.Serial(port=PORT,baudrate=9600,timeout=1)
    if MODE=='MODE_RAW_BIN':
        ser = serial.Serial(port=PORT,baudrate=19200,timeout=1)
    if MODE=='MODE_RAW_ASC':
        ser = serial.Serial(port=PORT,baudrate=38400,timeout=1)
    if MODE=='MODE_UNWHITENED':
        ser = serial.Serial(port=PORT,baudrate=57600,timeout=1)
    if MODE=='MODE_NORMAL_ASC':
        ser = serial.Serial(port=PORT,baudrate=115200,timeout=1)
    if MODE=='MODE_NORMAL_ASC_SLOW':
        ser = serial.Serial(port=PORT,baudrate=230400,timeout=1)
    ser.close()


# Print Header
print('TrueRNGpro Data Read Example')
print('http://ubld.it')
print('==================================================')


# Call list_ports to get com port info
ports_avaiable = list_ports.comports()

# Loop on all available ports to find TrueRNG
print('Com Port List')
for temp in ports_avaiable:
 #   print(temp[1] + ' : ' + temp[2])
    if '04D8:F5FE' in temp[2]:
        print('Found TrueRNG on ' + temp[0])
        if rng_com_port == None:        # always chooses the 1st TrueRNG found
            rng_com_port=temp[0]
    if '16D0:0AA0' in temp[2]:
        print('Found TrueRNGpro on ' + temp[0])
        if rng_com_port == None:        # always chooses the 1st TrueRNG found
            rng_com_port=temp[0]
    if '04D8:EBB5' in temp[2]:
        print('Found TrueRNGproV2 on ' + temp[0])
        if rng_com_port == None:        # always chooses the 1st TrueRNG found
            rng_com_port=temp[0]

print('==================================================')

# Print which port we're using
print('Using com port:  ' + str(rng_com_port))

# Print block size and number of loops
print('Capture Mode:    ' + capture_mode)
print('==================================================')

# Change to above mode (only has effect on the TrueRNGpro and TrueRNGproV2)
modeChange(capture_mode, rng_com_port)

# Try to setup and open the comport
try:
    ser = serial.Serial(port=rng_com_port,timeout=10)  # timeout set at 10 seconds in case the read fails
except:
    print('Port Not Usable!')
    print('Do you have permissions set to read ' + rng_com_port + ' ?')

# Open the serial port if it isn't open
if(ser.isOpen() == False):
    ser.open()

# Set Data Terminal Ready to start flow
ser.setDTR(True)

# This clears the receive buffer so we aren't using buffered data
ser.flushInput()

# Keep track of total bytes read
totalbytes=0

# Try to read the port and record the time before and after
try:
    x=ser.read(2048)   # read bytes from serial port
except:
    print('Read Failed!!!')

# Set index for random buffer to zero
index=0;

print('Entropy')
print('Printable Characters are   : 6.58 bits/char')
print('Letter / Number Characters : 5.95 bits/char')

print('==================================================')

found=0

password = '  Printable Characters Password: '

# Loop on how many characters to generate
while found < 20:
    # Convert 3 bytes of random x values to one integer
    temp = x[index]

    # Increment to the next byte of random for the next loop
    index=index+3

    # Find the remainder mod wordlistlength (generates a number between 0 and (wordlistlength-1) )
    # Ignore word if under 3 characters long
    if (temp > 32) & (temp<127):
        found=found+1
        password = password + chr(temp)

print(password)

found=0

password = 'Letters / Numbers Only Password: '

# Loop on how many characters to generate
while found < 20:
    # Convert 3 bytes of random x values to one integer
    temp = x[index]

    # Increment to the next byte of random for the next loop
    index=index+3

    # Find the remainder mod wordlistlength (generates a number between 0 and (wordlistlength-1) )
    # Ignore word if under 3 characters long
    if ((temp >= 48) & (temp<=57)) | ((temp >= 65) & (temp<=90)) | ((temp >= 97) & (temp<=122)):
        found=found+1
        password = password + chr(temp)

print(password)

print('==================================================')

# Close the serial port
ser.close()

# If we're on Linux set min on com port back to 1
# Pyserial screws this up
if os.name == 'posix':
    os.system('stty -F '+rng_com_port+' min 1')
