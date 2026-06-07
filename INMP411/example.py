from machine import I2S, Pin
import time
import math

# Set up I2S
audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=2048)

# Set up bytearray we will read into
# Set the length to what you calculate is the length needed given the duration you want and sample rate being used
read_buffer = bytearray(8_000)

for i in range(0, 20):

    # read
    #print("Reading sample # " + str(i) + "... ")
    t1 = time.ticks_ms()
    bytes_read = audio_in.readinto(read_buffer)
    t2 = time.ticks_ms()
    #print(str(len(read_buffer)) + " bytes read in " + str(t2 - t1) + " ms: " + str(read_buffer))

    # How many actual samples did we just get (each sample is 4 bytes)
    num_samples:int = bytes_read // 4

    # calc loudness across this sample
    all_squares:int = 0
    for s in range(num_samples):
        # convert to int
        byte1_index:int = s * 4      # the index of the first byte of the 4-byte integer
        rawint:int = int.from_bytes(read_buffer[byte1_index:byte1_index+4], "little")
        if rawint >= 0x80000000:
            rawint = rawint - 0x100000000
        all_squares = all_squares + rawint**2
    all_squares_avg = all_squares / num_samples
    vol:float = math.sqrt(all_squares_avg)
    print("Volume: " + str(vol))
    

# deinit
print()
print("De-init...")
audio_in.deinit()
print("Done. Bye!")