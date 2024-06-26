import machine
import ssd1306
import WeightedAverageCalculator
import time

# set up SSD1306
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up adc
adc0 = machine.ADC(machine.Pin(26)) # GP26
adc1 = machine.ADC(machine.Pin(27)) # GP27
adc2 = machine.ADC(machine.PIn(28)) # GP28

def test() -> None:

    while True:
        
        # show and avg
        val0:int = adc0.read_u16()
        val1:int = adc1.read_u16()
        val2:int = adc2.read_u16()

        # display
        oled.fill(0)
        oled.text("0: " + str(val0), 0, 0)
        oled.text("1: " + str(val1), 0, 12)
        oled.text("2: " + str(val2), 0, 24)
        oled.show()


        # sleep
        time.sleep(0.25)

test()