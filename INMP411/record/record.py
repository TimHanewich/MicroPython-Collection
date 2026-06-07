from machine import I2S, Pin
import tools

# Set up I2S
audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=2048)

# Set up buffer for how many bytes to read
# At a rate of 8,000 Hz = 32,0000 bytes per second = 128,000 bytes needed to capture 4 seconds worth of audio
audio_data = bytearray(128_000)

# read
print("Recording...")
bytes_read:int = audio_in.readinto(audio_data)
print("Recorded " + str(bytes_read) + " bytes.")

# deinit (this is super important! If you don't deinit, it won't be able to init again w/o a full power reset)
print("De-init...")
audio_in.deinit()
print("De-init complete.")

# convert to 8bit
print("Converting to 8bit...")
audio_data2:bytes = tools.convert_32bit_to_8bit(audio_data, 20)
print("Done")

# Create the header
print("Creating header...")
header = tools.create_wave_header(sample_rate=8_000, bits_per_sample=8, data_length=len(audio_data2))
print("Header of length " + str(len(header)) + " created.")

# Save to file
print("Saving to file...")
f = open("recording.wav", "wb")
f.write(header)
f.write(audio_data2)
f.close()
print("Saved!")