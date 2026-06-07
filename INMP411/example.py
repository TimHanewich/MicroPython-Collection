from machine import I2S, Pin
import time
import math

# Set up I2S
audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=2048)

# Set up bytearray we will read into
# Set the length to what you calculate is the length needed given the duration you want and sample rate being used
read_buffer = bytearray(8_000)

for i in range(0, 50):

    # read
    #print("Reading sample # " + str(i) + "... ")
    t1 = time.ticks_ms()
    bytes_read = audio_in.readinto(read_buffer)
    t2 = time.ticks_ms()
    #print(str(len(read_buffer)) + " bytes read in " + str(t2 - t1) + " ms: " + str(read_buffer))

    # How many actual samples did we just get (each sample is 4 bytes)
    num_samples:int = bytes_read // 4

    # Calculate RMS ("root mean square") as an indication of avg. loudness across this sample
    all_squares:float = 0.0
    for s in range(num_samples):

        # convert to int
        byte1_index:int = s * 4                                                            # the index of the first byte of the 4-byte integer
        rawint:int = int.from_bytes(read_buffer[byte1_index:byte1_index+4], "little")      # by default, this converts it to an UNSIGNED int32 (min of 0, max of 4,294,967,295)

        # The I2S protocol though is an int32, not uint32! So we must manually convert it to a int32
        # (MicroPython doesn't support this natively in int.from_bytes())
        if rawint >= 0x80000000:                          # if > 2,147,483,648 (max value of int32)
            rawint = rawint - 0x100000000                 # Subtract 4,294,967,296 to convert to int32 (if it exceeds int32 value, immediately starts at int32 lower bound)

        # Convert to -1.0 to 1.0 (think of a sine wave in audacity)
        asfloat:float = rawint / 2_147_483_647

        # square and add to tally
        all_squares = all_squares + asfloat**2

    all_squares_avg:float = all_squares / num_samples
    vol:float = math.sqrt(all_squares_avg)
    print("Volume: " + str(vol))

# deinit (this is super important! If you don't deinit, it won't be able to init again w/o a full power reset)
print()
print("De-init...")
audio_in.deinit()
print("Done. Bye!")