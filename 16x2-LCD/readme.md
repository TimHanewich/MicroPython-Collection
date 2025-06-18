# Interfacing with a 16x2 LCD Display from a Raspberry Pi Pico (MicroPython)
I have one of [these generic 16x2 LCD displays](https://a.co/d/cL9BH0b) from a kit I purchased several years ago. I followed some tutorials online, used sample code, and got it working. Sharing my learnings here.

**Lesson #1 (VERY IMPORTANT): use a screwdriver to turn the back potentiometer to control the backlight of the displayed characters, as depicted below**

![pot](https://i.imgur.com/yoQynbe.png)

The above is *very* important. Note that this is changing the backlight strength of the **characters themselves** (displayed text), NOT the green/blue backlight. I was toiling with the LCD for some time trying to figure out why it wasn't showing text - turns out, I just had the text brightness down to 0%! Turning the potentiometer fixed my issue right away.

## Tutorial
First, upload both the [lcd_api.py](./src/lcd_api.py) and [pico_i2c_lcd.py](./src/pico_i2c_lcd.py) files to your Raspberry Pi Pico. This driver code is from [Dave Hylands](https://github.com/dhylands) and can be found in [this repository](https://github.com/dhylands/python_lcd).

The following sample tests cycles through a few demonstrations:

```
import machine
import time
import pico_i2c_lcd

# Get LCD's I2C address
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17)) # change the numbers here to your I2C interface!
print("I2C Scan: " + str(i2c.scan()))
addr = i2c.scan()[0]
print("I will assume this is the I2C address of your LCD: " + str(addr) + " (" + str(hex(addr)) + ")")

# set up LCD interface
lcd = pico_i2c_lcd.I2cLcd(i2c, addr, 2, 16) # 2 is the height, 16 is the width (in # of characters)

# turn on backlight as a starting state for the tests
lcd.backlight_on()

# continuously run demonstration!
while True:
    
    # print something
    lcd.clear()
    lcd.putstr("Hello!")
    time.sleep(2)
    
    # print something (two lines)
    lcd.clear()
    lcd.putstr("Hello...\nNew line!")
    time.sleep(2)
    
    # demonstrate cursor on
    lcd.clear()
    lcd.show_cursor()
    lcd.putstr("cursor on")
    time.sleep(2)
    
    # demonstrate cursor off
    lcd.clear()
    lcd.hide_cursor()
    lcd.putstr("cursor off")
    time.sleep(2)
    
    # demonstrate blink cursor on
    lcd.clear()
    lcd.blink_cursor_on()
    lcd.putstr("blink cursor\nON")
    time.sleep(2)
    
    # demonstrate blink cursor off
    lcd.clear()
    lcd.blink_cursor_off()
    lcd.hide_cursor() # turning on the blink cursor also turns on the standard cursor, so we must turn that off as well if we don't want it
    lcd.putstr("blink cursor\nOFF")
    time.sleep(2)
    
    # demonstrate backlight off
    # with the backlight off, the text actually IS still there, it is just hard to see (need high light environment)
    lcd.clear()
    lcd.backlight_off()
    lcd.putstr("Backlight off!")
    time.sleep(2)
    
    # put backlight back on
    lcd.clear()
    lcd.backlight_on()
    lcd.putstr("Backlight on!")
    time.sleep(2)
```

## Displaying Custom Characters
You can also display *custom characters* on the LCD display. Each character is a 5x8 matrix (5 pixels across, 8 pixels tall). You can fully customize a character by specifying what pixels should be populated.

To do this, I highly recommend using [maxpromer's LCD Character Creator](https://maxpromer.github.io/LCD-Character-Creator/):

![char creator](https://i.imgur.com/63wo5o5.png)

As you can see, each row can be represented by 5 bits. For each row, we can use the state of the 5 bits to make a byte. For example, to represent the **first row** (top row) in Python, it would be `0b01010`. The second would be `0b11111`, the third `0b01110`, and so on.

We can then put each of these rows into an array of bytes to represent a full character map:

```
heart = bytes([0b01010, 0b11111, 0b01110, 0b00100, 0b00000, 0b00000, 0b00000, 0b00000])
```

To display this on the LCD display, we first must "save it" to the LCD display's memory as one of the **eight** available CGRAM custom characters it can display.

```
lcd.custom_char(0, heart) # store the custom character (a heart in this case) to customer character 0
```

Finally, to then use that custom character, we can use the traditional `putstr()` method! Simply append `chr(0)` to the string to indicate character 0 being used in that position and the LCD will summon what it has stored for character 0.

```
lcd.putstr(chr(0) + " <-- heart!")
```

Full example below:

```
import machine
import time
import pico_i2c_lcd

# Get LCD's I2C address
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17)) # change the numbers here to your I2C interface!
print("I2C Scan: " + str(i2c.scan()))
addr = i2c.scan()[0]
print("I will assume this is the I2C address of your LCD: " + str(addr) + " (" + str(hex(addr)) + ")")

# set up LCD interface
lcd = pico_i2c_lcd.I2cLcd(i2c, addr, 2, 16) # 2 is the height, 16 is the width (in # of characters)

# create, store, and display a custom character!
lcd.backlight_on()
heart = bytes([0b01010, 0b11111, 0b01110, 0b00100, 0b00000, 0b00000, 0b00000, 0b00000])
lcd.custom_char(0, heart) # store the custom character (a heart in this case) to customer character 0
lcd.putstr(chr(0) + " <-- heart!")

```

## Other Tutorials
- [Tom's Hardware Tutorial](https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico) is excellent.