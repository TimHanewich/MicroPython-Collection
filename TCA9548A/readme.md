# TCA9548A I2C Multiplexer
![https://i.imgur.com/VkSvdJu.jpeg]

The I2C protocol is a powerful tool for connecting multiple devices with minimal wiring, but it comes with a significant limitation—address conflicts. Many I2C peripherals have fixed addresses, making it impossible to connect identical devices to the same bus without interference. That’s where the TCA9548A I2C multiplexer comes in.

The TCA9548A is an integrated circuit designed to expand I2C connectivity by allowing multiple devices with the same address to coexist on a single microcontroller. Acting as a switchboard, this multiplexer provides eight selectable I2C channels, enabling a seamless way to interface multiple devices without worrying about address conflicts. With simple software commands, you can dynamically switch between different I2C peripherals, making it an invaluable tool for sensor arrays, complex automation systems, and robotics applications.

The TCA9548A has an I2C address of `0x70`, which is `112` as an integer.

I purchased [this set of 6 on Amazon](https://a.co/d/308x3UD) and have had success with them!

## How does it work?
The TCA9548A is very simple to use! Simply write a single byte that corresponds to which of the **eight** buses that you want to redirect the I2C traffic to. For example:

```
import machine

# I2C that the multiplexer is attached to
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

# switch to channel 0
i2c.writeto(0x70, bytes([1 << 0]))
print("Devices on channel 0: " + str(i2c.scan())) # will show 0x70 (112) and any other devices attached to that channel
```

So, in the above example, if we had an I2C device connected to bus 0, that device *and* the TCA9548A (`112`) would appear in that scan.

The key above I found is *the notation* of how you are switching. I tried directly writing a value of `0` to it, but this did not work... the notation below must be used, it is not truly zero based, but rather based on where the `1` bit is in a sequence, seen below.

```
i2c.writeto(0x70, bytes([1 << 0])) # switch to channel 0
i2c.writeto(0x70, bytes([1 << 1])) # switch to channel 1
i2c.writeto(0x70, bytes([1 << 2])) # switch to channel 2
i2c.writeto(0x70, bytes([1 << 3])) # switch to channel 3
# etc...
```

## Sample Code
I'm sharing a few different examples of sample code to demonstrate how the TCA9548A can be used in MicroPython:
- [Most basic example, cycling through each channel and printing the devices](./src/example.py)
- [Using two identical VL53L0X sensors, same addresses, but on different buses](./src/example_tof.py) - *requires the [vl503l0x.py](../VL53L0X/src/vl53l0x.py) module.
    - As seen in this example, when instantiating an instance of a helper class, it is best to have **two separate instances** for each sensor, with each **only attempting to interface with its corresponding sensor when that channel is active**.
