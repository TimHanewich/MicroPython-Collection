import time
import machine
from QMC5883L import QMC5883L
import ssd1306

i2c_qmc = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
print(i2c_qmc.scan())

i2c_ssd = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
print(i2c_ssd.scan())

# Set up QMC
qmc = QMC5883L(i2c_qmc)
qmc.initialize(1, 100, 2, 64)

# set up SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c_ssd)

# count down
countdown:int = 8
for t in range(0, countdown):
    cd:int = countdown - t
    oled.fill(0)
    oled.text("Calibrate in ", 0, 0)
    oled.text(str(cd), 0, 12)
    oled.show()
    time.sleep(1)
    
# set up vals
min_x:int = 999999
max_x:int = 0
min_y:int = 999999
max_y:int = 0
min_z:int = 999999
max_z:int = 0
    
# calibrate
duration_ms:int = 30000
started_at:int = time.ticks_ms()
while (time.ticks_ms() - started_at) < duration_ms:
    
    # print update
    duration_so_far = time.ticks_ms() - started_at
    seconds_remaining:int = int((duration_ms - duration_so_far) / 1000)
    oled.fill(0)
    oled.text("Calibrating...", 0, 0)
    oled.text(str(seconds_remaining), 0, 12)
    oled.show()
    
    # record
    x,y,z = qmc.read()
    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)
    min_z = min(z, min_z)
    max_z = max(z, max_z)
    
    # wait
    time.sleep(0.01)
    
# print the min and max vals
oled.fill(0)
oled.text("X: " + str(min_x) + ", " + str(max_x), 0, 0)
oled.text("Y: " + str(min_y) + ", " + str(max_y), 0, 12)
oled.text("Z: " + str(min_z) + ", " + str(max_z), 0, 24)
oled.show()