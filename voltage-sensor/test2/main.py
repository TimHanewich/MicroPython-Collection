import color_toolkit.color_toolkit
import machine
import time
import neopixel.neopixel
import ssd1306
import voltage
import BatteryMonitor
import WeightedAverageCalculator
import neopixel
import color_toolkit

# set up SSD1306
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up voltage reader
vs = voltage.VoltageSensor(26) # GPIO 26

# set up battery monitor to convert the voltage we read to state of charge %'s
bm = BatteryMonitor.BatteryMonitor()

# set up weighted avg calculator
wac = WeightedAverageCalculator.WeightedAverageCalculator(alpha=0.9)

# set up neopixel
pixels = neopixel.Neopixel(5, 0, 22, "GRB") # WS2812B on GP22

def test() -> None:

    while True:

        # fill with random color
        pixels.fill(color_toolkit.random_color())
        pixels.show()

        # read voltage
        volts:float = vs.voltage(duration=0.05, samples=10) # raw
        volts = wac.feed(volts) # pass through averaging filter

        # calculate SOC
        soc:float = bm.soc(volts)
        socs:str = str(round(soc * 100, 1)) + "%"
        
        # what to print on SSD-1306
        oled.fill(0)
        oled.text(str(round(volts, 2)) + "v", 0, 0)
        oled.text("SOC: " + socs, 0, 12)
        oled.show()

        # sleep
        time.sleep(1.0)

test()