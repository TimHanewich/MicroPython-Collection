import machine
import time
import json

datas = []

u = machine.UART(0, rx=machine.Pin(17), baudrate=9600)
while len(datas) < 250:
    print("Reading...")
    data = u.read()
    if data != None:
        try:
            data2 = data.decode()
            datas.append(data2)
            print(data2)
        except:
            print("FAILURE WITH " + str(data))
    else:
        print("NOTHING received!")
    time.sleep(1.0)
    
f = open("data.json", "a")
f.write(json.dumps(datas))
f.close()
