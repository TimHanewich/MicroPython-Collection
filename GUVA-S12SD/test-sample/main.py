import machine
import ssd1306
import GUVA_S12SD
import time

# set up OLED
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up GUVA
guva = GUVA_S12SD.GUVA_S12SD(26)

while True:

    oled.fill(0)

    # get UV Index rating
    uvi:int = guva.UVI
    oled.text("UVI: " + str(uvi), 0, 0)

    # get raw adc value
    adcval:int = guva._adc.read_u16()
    oled.text(str(adcval), 0, 16)

    oled.show()
    time.sleep(0.25)
