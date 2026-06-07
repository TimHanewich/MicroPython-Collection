from machine import I2S, Pin
import time
import math

# Set up I2S
audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=2048)

# Set up bytearray we will read into
# Set the length to what you calculate is the length needed given the duration you want and sample rate being used
read_buffer = bytearray(8_000)

# read
print("Reading now.")
t1 = time.ticks_ms()
bytes_read = audio_in.readinto(read_buffer)
t2 = time.ticks_ms()
print(str(len(read_buffer)) + " bytes read in " + str(t2 - t1) + " ms: " + str(read_buffer))

# deinit
print()
print("De-init...")
audio_in.deinit()
print("Done. Bye!")

# calc
all_squares:int = 0
for b in read_buffer:
    all_squares = all_squares + b**2
all_squares_avg = all_squares / len(read_buffer)
vol:float = math.sqrt(all_squares_avg)
print("Volume: " + str(vol))