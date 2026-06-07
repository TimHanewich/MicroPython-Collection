from machine import I2S, Pin

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
print()
print("De-init...")
audio_in.deinit()
print("De-init complete.")


# Function for creating the header
def create_wave_header(data_length:int, sample_rate:int) -> bytes:
    """
    Function for creating the 44-byte header of a .wav file.

    Args:
        data_length (int): The total size (length) of the raw audio data, in bytes.
        sample_rate (int): The sampling frequency the audio bytes were captured at (i.e. 8,000 for 8 kHz)

    Returns:
        bytes: A 44-byte packed binary packet representing the .wav header. Prepend this to the audio data to construct a .wav file!
    """

    ToReturn:bytearray = bytearray()

    # add RIFF
    ToReturn.extend("RIFF".encode("ascii"))

    # add total file size, but excluding this and the RIFF marker
    TotalLength:int = data_length + 36
    ToReturn.extend(TotalLength.to_bytes(4, "little"))

    # Add WAVE
    ToReturn.extend("WAVE".encode("ascii"))

    # Add format chunk market
    ToReturn.extend("fmt ".encode("ascii"))

    # Add length of above format data
    LengthOfAboveFormatData:int = 16
    ToReturn.extend(LengthOfAboveFormatData.to_bytes(4, "little"))

    # Add format type
    FormatType:int = 1
    ToReturn.extend(FormatType.to_bytes(2, "little"))

    # Add number of channels
    NumChannels = 1
    ToReturn.extend(NumChannels.to_bytes(2, "little"))

    # Add sample rate
    ToReturn.extend(sample_rate.to_bytes(4, "little"))

    # Add byte rate (number of bytes per second)
    ByteRate:int = 32_000
    ToReturn.extend(ByteRate.to_bytes(4, "little"))

    # Add Block Align (number of bytes per sample?)
    BlockAlign:int = 4
    ToReturn.extend(BlockAlign.to_bytes(2, "little"))

    # Add bits per sample
    BitsPerSample = 32
    ToReturn.extend(BitsPerSample.to_bytes(2, "little"))

    # Add "data" splitter
    ToReturn.extend("data".encode("ascii"))

    # Add data size, in bytes
    ToReturn.extend(data_length.to_bytes(4, "little"))

    return bytes(ToReturn)

# Create the header
print("Creating header...")
header = create_wave_header(len(audio_data), 8_000)
print("Header of length " + str(len(header)) + " created.")

# Save to file
print("Saving to file...")
f = open("recording.wav", "wb")
f.write(header)
f.write(audio_data)
f.close()
print("Saved!")