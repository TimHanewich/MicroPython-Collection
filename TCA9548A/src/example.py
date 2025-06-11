import machine

# I2C that the multiplexer is attached to
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

# switch to channel 0
i2c.writeto(0x70, bytes([1 << 0]))
print("Devices on channel 0: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 1
i2c.writeto(0x70, bytes([1 << 1]))
print("Devices on channel 1: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 2
i2c.writeto(0x70, bytes([1 << 2]))
print("Devices on channel 2: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 3
i2c.writeto(0x70, bytes([1 << 3]))
print("Devices on channel 3: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 4
i2c.writeto(0x70, bytes([1 << 4]))
print("Devices on channel 4: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 5
i2c.writeto(0x70, bytes([1 << 5]))
print("Devices on channel 5: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 6
i2c.writeto(0x70, bytes([1 << 6]))
print("Devices on channel 6: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel

# switch to channel 7
i2c.writeto(0x70, bytes([1 << 7]))
print("Devices on channel 7: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel