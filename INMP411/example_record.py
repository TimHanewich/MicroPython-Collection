from machine import I2S, Pin
import time
import math
import os

# Set up I2S
audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=16_000)

# temp file for writing bytes to
file_buf = open("temp", "wb") # "wb" starts clean every time (new file) while "ab" appends to whatever exists

try:

    # Set up bytearray to read into
    buf:bytearray = bytearray(1_028)

    # record
    target_byte_length:int = 160_000    # would be 5 seconds (32,000 bytes per second)
    bytes_written:int = 0
    while bytes_written < target_byte_length:

        # read
        print("Reading bytes...")
        bytes_read:int = audio_in.readinto(buf)
        print(str(bytes_read) + " bytes read.")

        # write it to file (append)
        print("Writing to file buffer...")
        file_buf.write(buf)
        print("Dumped to file buffer.")

        # increment write counter
        print("Incrementing counter...")
        bytes_written = bytes_written + bytes_read 
        print("Incremented.")

except Exception as ex:
    print("Fatal error: " + str(ex))

finally:

    # close file
    file_buf.close()
    print("File closed.")

    # deinit
    audio_in.deinit()
    print("De-init complete. Bye!")