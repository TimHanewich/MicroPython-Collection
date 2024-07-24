import reyax
import machine
import random
import time

u = machine.UART(0, tx=machine.Pin(12), rx=machine.Pin(13), baudrate=115200)
r = reyax.RYLR998(u)

print(r.networkid)
print(r.address)
print(r.band)
print(r.rf_parameters)
print(r.output_power)

while True:
    i = random.randint(0, 999999999)
    r.send(0, str(i).encode("ascii"))
    print("Just sent " + str(i))
    time.sleep(6)