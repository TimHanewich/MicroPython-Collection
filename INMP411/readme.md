# INMP441
![pic](https://i.imgur.com/UhxRJ4B.png)

I purchased [these INMP441](https://github.com/TimHanewich/MicroPython-Collection) from Amazon in June 2026. The following describes how to work with these modules via MicroPyton's [I2S class](https://docs.micropython.org/en/latest/library/machine.I2S.html).

Check out two examples on how to use the INMP441:
- Example live monitoring the decibels: [monitor.py](./monitor.py)
- Example recording into a `.wav` file: [record](./record/)

## Understanding Data Flow
I2S is a continuous flow of audio data (binary data) to the Raspberry Pi Pico, at a particularly high rate!

The INMP441 has an adjustable sample rate, which is the numebr of times per second it will "take a snapshot" of the audio wave:
- 8,000 Hz (**recommended for RPi Pico**)
- 16,000 Hz
- 32,000 Hz
- 44,100 Hz
- 48,000 Hz

Each individual sample is really **24 bits** of data (**3 bytes**), but it is *always* transmitted in **32 bit** packets (**4 bytes**), with the last byte just being `0` (empty).

So, at a sample rate of 8,000 Hz, that is 8,000 samples of 4 bytes, which would be 32,000 bytes per second (8,000 * 4)... so a lot! Thus, for example, 0.25 seconds of capture time at that 8,000 Hz would be 8,000 bytes.

## Example Timing
The way you capture data via I2S is you set up a `bytearray` with a certain amount of bytes that you want to capture, and then you use `I2S.readinto()` to read into it; this will be a blocking call, meaning it will sit and wait there until it fills that buffer.

So, given that, that means you can set up the size of the buffer based on *for how long* (duration) you want it to capture for. If i wanted to capture 250 ms worth of data for example, and had a sample rate of 8,000 Hz, that means I would set up a 8,000 byte buffer and then capture... it would block for exactly 250 ms! (this is because we know a rate of 8,000 Hz is 32,000 bytes per second, so quarter it for a quarter of a second)

## What is this data?
As mentioned above, 32 bits of data are received, representing a 4-byte integer (`int32`). The range of this integer is thus -2,147,483,648 to 2,147,483,647. You can then transform this as a floating point value between -1.0 to 1.0 that represents that audio wave at that particular point (think of a sine wave).

## Warning: Writing to Flash Storage Doesn't Work
Through testing, I found that writing to flash storage (onboard Pico storage) after the `I2S` has been initialized doesn't work. Likely because there is some overlap or inteferance of the background process of capturing via the internal `I2S` buffer, but for whatever reason it would *always* hang for me when I mixed together both I2S and flash storage!

However, this is **NOT** the case when interfacing with other peripherals via GPIO: for example, [this script](https://github.com/TimHanewich/MicroPython-Collection/blob/e8e332220c23af6268730fb8040b13ec9b2de3c3/INMP411/example_HC12.py) tested and proved its ability to send small data packets via HC-12, it worked well! Perhaps an external SD card breakout board would work well too.