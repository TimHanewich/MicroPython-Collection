from machine import I2S, Pin
import math

# Set up I2S
# the "ibuf" is the internal buffer - how many bytes it can hold while you do something (similar to UART RX)
audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=2048)

# Set up bytearray we will read into
# Set the length to what you calculate is the length needed given the duration you want and sample rate being used
# Example: at a rate of 8,000 samples per second and each sample being 4 bytes, that is 32,000 bytes per second
# So if we want to capture in increments of 0.1 seconds, capture 3,200 bytes (it will wait for 3,200 bytes to "fill up")
read_buffer = bytearray(1_600)

try:
    while True:

        # read the incoming data
        bytes_read = audio_in.readinto(read_buffer)

        # How many actual samples did we just get 
        # The INMP441 provides 4 bytes per sample (32 bits)
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

        # Calculate RMS (avg across these samples over a short span of time)
        all_squares_avg:float = all_squares / num_samples
        rms:float = math.sqrt(all_squares_avg) # this is the root mean square

        # Calculate dBFS: Decibels Relative to Full Scale
        # This is where the reference point of 0 is the maximum ceiling. So if we pretend "0 db" is the MAX this device can take
        # Then anything it reads should be below that
        dBFS:float = -100.0 # default to -100.0 which is ABSOLUTE silent
        if rms > 0: # if we have SOME sound
            dBFS = 20 * math.log10(rms) # calculate
        
        # Calculate dBSPL: Decibel Sound Pressure Level
        # This is more of an "absolute" decibel level where 0 dB is instead the absolute silence floor (shifted)
        # To calculate this, we must take into account how sensitive this particular device is
        # The INMP441 datasheet states a sensitive of -26 (https://i.imgur.com/oiKdugk.png)
        # So this means, at 94 dBSPL, the device would show -26 dBFS
        # So now we know to "shift" the "relative" dBFS to "absolute" dBSPL, we have to add 120 (gap between -26 and 94!)
        dBSPL:float = dBFS + 120.0

        # print
        print("RMS: " + str(round(rms * 100, 3)) + "%" + ", Decibels: " + str(int(round(dBSPL, 0))))

finally:
    print("De-init'ing I2S...")
    audio_in.deinit()
    print("De-init complete! Goodbye!")