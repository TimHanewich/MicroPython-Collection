import time
import machine
import reyax
import ssd1306

setup_delay_seconds:float = 0.25

# set up ssd1306
i2c = machine.I2C(1, sda=machine.Pin(6), scl=machine.Pin(7))
print(i2c.scan())
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.text("Hello!", 0, 0)
oled.show()
time.sleep(setup_delay_seconds)


# set up RYLR998
u = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))
r = reyax.RYLR998(u)
oled.fill(0)
oled.text("RYLR998", 0, 0)
oled.text("setup!", 0, 12)
oled.show()
time.sleep(setup_delay_seconds)

# Pulse?
oled.fill(0)
oled.text("Pulse?...", 0, 0)
oled.show()
time.sleep(setup_delay_seconds)
if r.pulse:
    oled.text("Success!", 0, 12)
    oled.show()
    time.sleep(setup_delay_seconds)
else:
    oled.text("No!", 0, 12)
    oled.show()
    time.sleep(9999999)

# display config screen
oled.fill(0)
oled.text("N: " + str(r.networkid), 0, 0)
oled.text("A: " + str(r.address), 0, 12)
oled.text("B: " + str(r.band), 0, 24)
oled.text("P: " + str(r.rf_parameters).replace("(", "").replace(")", "").replace(" ",""), 0, 36)
oled.text("S: " + str(r.output_power), 0, 48) # S is short for "strength"
oled.show()
time.sleep(5.0)

# set up!
oled.fill(0)
oled.text("Setup!", 0, 0)
oled.show()

# cycle for new messages
msg_showed_ticks_ms:int = None # if None, that can be interpretted as a message wasn't received and shown yet.
while True:
    msg:reyax.ReceivedMessage = r.receive()
    if msg != None: # there is a brand new message! Show it!
        oled.fill(0)
        oled.text("A: " + str(msg.address), 0, 0)
        oled.text("L: " + str(msg.length), 0, 12)
        oled.text("RSSI: " + str(msg.RSSI), 0, 24)
        oled.text("SNR: " + str(msg.SNR), 0, 36)
        oled.text(msg.data.decode("ascii"), 0, 48)
        oled.show()
        msg_showed_ticks_ms = time.ticks_ms()
    else:
        if msg_showed_ticks_ms == None or (time.ticks_ms() - msg_showed_ticks_ms) >= 5000:
            oled.fill(0)
            oled.text("Waiting...", 0, 0)
            oled.show()
    
    time.sleep(0.1)
