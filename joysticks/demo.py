import machine
import time
import joysticks

adc1 = machine.ADC(26)
adc2 = machine.ADC(27)




while True:
    val1 = adc1.read_u16()
    val2 = adc2.read_u16()
    
    val1p = val1 / 65535
    val2p = val2 / 65535   # value as a percentage
    
    transformed:float = joysticks.transform(val2p)
    print(str(int(round(transformed*100,0))) + "%")
    time.sleep(0.1)
    

    
