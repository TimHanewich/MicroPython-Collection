import machine
import ssd1306
import time
import voltage

# set up SSD1306
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up voltage sensor
vs = voltage.VoltageSensor(26)

def test() -> None:

    while True:
        
        # burst read
        burst:int = vs._sample_analog(1.0, 40)

        # display
        oled.fill(0)
        oled.text("0: " + str(burst), 0, 0)
        oled.show()


        # sleep
        time.sleep(0.25)

test()