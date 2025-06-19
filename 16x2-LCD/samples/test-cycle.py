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

# Add custom character, full on
SOLID:bytes = bytes([0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111])
lcd.custom_char(0, SOLID)

# set up backlight tracker var
backlighton:bool = False

# continuously run demonstration!
delay_time:float = 5.0
while True:

    # flip backlight
    if backlighton:
        lcd.backlight_off()
        backlighton = False
    else:
        lcd.backlight_on()
        backlighton = True

    # print something
    lcd.clear()
    lcd.putstr("Hello!")
    time.sleep(delay_time)
    
    # print something (two lines)
    lcd.clear()
    lcd.putstr("Hello...\nNew line!")
    time.sleep(delay_time)

    # print full
    ToPrint:str = chr(0) * 32 # my 16x2 display is 32 characters in total
    lcd.putstr(ToPrint)
    time.sleep(delay_time)
    
    # now do clear (empty)
    lcd.clear()
    time.sleep(delay_time)
    