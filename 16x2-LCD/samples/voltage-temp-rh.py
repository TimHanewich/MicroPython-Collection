import machine
import time
import pico_i2c_lcd
import math
import random

# Get LCD's I2C address
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17)) # change the numbers here to your I2C interface!
print("I2C Scan: " + str(i2c.scan()))
addr = i2c.scan()[0]
print("I will assume this is the I2C address of your LCD: " + str(addr) + " (" + str(hex(addr)) + ")")

# set up LCD interface
lcd = pico_i2c_lcd.I2cLcd(i2c, addr, 2, 16) # 2 is the height, 16 is the width (in # of characters)

# store degree symbol as a custom character (it doesn't work as is)
degree:bytes = bytes([0b00110, 0b01001, 0b01001, 0b00110, 0b00000, 0b00000, 0b00000, 0b00000])
lcd.custom_char(0, degree) # store the degre symbol as custom char #0

def display_data(temp:float, humidity:float, voltage:float) -> None:
    """Provide temperature as the temp in fahrenheight (i.e. 98.7), provide humidity as a relative humidity percentage (i.e. 0.65 for 65% RH), and voltage as a voltage (i.e. 12.2)"""
    
    # there is no need to clear the LCD because every character that is NOT used will be written over with an empty space
     
    # assemble line 1 (voltage)
    vDisplay:str = str(round(voltage, 1)) + " v"
    vSpacesBefore:int = math.floor((16 - len(vDisplay)) / 2)
    vSpacesAfter:int = 16 - vSpacesBefore - len(vDisplay)
    line1:str = (' ' * vSpacesBefore) + vDisplay + (' ' * vSpacesAfter)
    lcd.putstr(line1)
    
    # assemble line 2 (temp + humidity)
    tDisplay:str = str(round(temp, 1)) + " " + chr(0) + "F"
    hDisplay:str = str(round(humidity * 100, 1)) + " %H"
    SpacesBetween = 16 - len(tDisplay) - len(hDisplay) # how many spaces to put in between
    line2:str = tDisplay + (' ' * SpacesBetween) + hDisplay
    
    # print both lines! (both should be 16 characters wide)
    lcd.move_to(0, 0)
    lcd.putstr(line1 + line2)
    

# turn on backlight as a starting state for the tests
lcd.backlight_on()

while True:
    temperature:float = random.uniform(40.0, 110.0)
    humidity:float = random.uniform(0.0, 1.0)
    voltage:float = random.uniform(9.0, 16.5)
    display_data(temperature, humidity, voltage)
    time.sleep(1.0)