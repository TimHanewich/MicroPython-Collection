import time
import machine

class GUVA_S12SD:
    
    def __init__(self, adc_pin:int):
        self._adc = machine.ADC(adc_pin)
        
    @property
    def UVI(self) -> int:
        
        # measure ADC sample
        tot:int = 0.0
        for x in range(10):
            tot = tot + self._adc.read_u16()
            time.sleep(0.01)
        val:float = tot / 10
        
        # convert to a voltage
        voltage:float = (val / 65536) * 3.3 # 65536 is the MAX value it would display if it was reading a full 3.3v (reference voltage for the Raspberry Pi Pico), so basically expressing it as a percentage. And then multiply by 3.3 to get the voltage.
        
        # convert voltage to UV index
        mV:int = int(voltage * 1000) # convert from volts to milivolts
        
        # infer UV index from mV, according to this graphic: https://i.imgur.com/qtNq3Wm.png
        if mV < 50:
            return 0
        elif mV >= 227 and mV < 318:
            return 1
        elif mV >= 318 and mV < 408:
            return 2
        elif mV >= 408 and mV < 503:
            return 3
        elif mV >= 503 and mV < 606:
            return 4
        elif mV >= 606 and mV < 696:
            return 5
        elif mV >= 696 and mV < 795:
            return 6
        elif mV >= 795 and mV < 881:
            return 7
        elif mV >= 881 and mV < 976:
            return 8
        elif mV >= 976 and mV < 1079:
            return 9
        elif mV >= 1079 and mV < 1170:
            return 10
        else: # anything greater than 1170
            return 11