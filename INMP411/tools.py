def convert_32bit_to_8bit(audio_data:bytes, amplification:int = 20) -> bytes:

    # reduce from 32-bit to 8-bit
    num_samples:int = len(audio_data) // 4
    audio_data2:bytearray = bytearray(num_samples)
    for i in range(num_samples):
        original_offset:int = i * 4

        # construct original int32
        asint = int.from_bytes(audio_data[original_offset:original_offset+4], "little") # unpacks as uint32
        if asint >= 2_147_483_648: 
            asint = asint - 4_294_967_296 # convert to int32 if needed

        # Amplify
        asint = asint * amplification

        # Determine uint8
        por:float = (asint + 2_147_483_648) / 4_294_967_296
        asuint8 = int(por * 255)

        # constrain!
        if asuint8 > 255:
            asuint8 = 255

        # populate new audio data
        audio_data2[i] = asuint8

    return audio_data2