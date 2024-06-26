import machine
import ssd1306
import time
import voltage
import neopixel

# set up SSD1306
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# set up neopixel
last_switched_ticks_ms:int = 0
switch_every_ticks_ms:int = 50000 # 5 seconds
current_status:bool = False # off = False, on = True
pixels = neopixel.Neopixel(12, 0, 22, "GRB")

# set up voltage sensor
vs = voltage.VoltageSensor(26)

while True:

    # handle pixels
    if (time.ticks_ms() - last_switched_ticks_ms) > switch_every_ticks_ms:
        if current_status == False:
            pixels.fill((255, 255, 255))
            current_status = True
        else:
            pixels.fill((0, 0, 0))
            current_status = False
        pixels.show() # show it
        last_switched_ticks_ms = time.ticks_ms()
    
    # burst read
    burst:int = vs._sample_analog(1.0, 40)

    # display
    oled.fill(0)
    oled.text("0: " + str(burst), 0, 0)
    oled.show()

    # sleep
    time.sleep(0.25)
