from machine import I2S, Pin

audio_in = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.RX, bits=32, format=I2S.MONO, rate=8_000, ibuf=2048)
read_buffer = bytearray(128_000)

# read
print("Reading...")
bytes_read:int = audio_in.readinto(read_buffer)
print("Read " + str(bytes_read) + " bytes.")

# deinit (this is super important! If you don't deinit, it won't be able to init again w/o a full power reset)
print()
print("De-init...")
audio_in.deinit()
print("De-init complete.")

# Save it
f = open("raw", "wb")
print("Writing to file...")
f.write(read_buffer)
print("Written!")
f.close()