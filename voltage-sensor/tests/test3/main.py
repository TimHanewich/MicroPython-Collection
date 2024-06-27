import machine
import ssd1306
import WeightedAverageCalculator
import time

# set up SSD1306
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up adc
adc = machine.ADC(machine.Pin(26)) # GP26

# set up weighted avg calculator
wac = WeightedAverageCalculator.WeightedAverageCalculator(alpha=0.95)

def test() -> None:

    while True:
        
        # show and avg
        val:int = adc.read_u16()
        vala:float = wac.feed(float(val))

        # display
        oled.fill(0)
        oled.text(str(vala), 0, 0)
        oled.show()


        # sleep
        time.sleep(1.0)

test()