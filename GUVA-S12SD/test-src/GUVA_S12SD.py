import time
import machine

class GUVA_S12SD:
    
    def __init__(self, adc_pin:int):
        self._adc = machine.ADC(adc_pin)
        
    @property
    def UVI(self) -> int:
        
        # measure ADC sample
        tot:int = 0
        for x in range(10):
            tot = tot + self._adc.read_u16()
            time.sleep(0.01)
        val:float = tot / 10
        
        # convert to a voltage
        voltage:float = (val / 65536) * 3.3 # 65536 is the MAX value it would display if it was reading a full 3.3v (reference voltage for the Raspberry Pi Pico), so basically expressing it as a percentage. And then multiply by 3.3 to get the voltage.
        
        # convert voltage to UV index
        mV:int = int(voltage * 1000) # convert from volts to milivolts
        
        # infer UV index from mV, according to this graphic: https://i.imgur.com/qtNq3Wm.png
        ToReturn:int = 0
        if mV < 227: # I know the graphic calls for < 50... however, there is an aparent gap between 50 and 227 in that graphic.
            ToReturn = 0
        elif mV >= 227 and mV < 318:
            ToReturn = 1
        elif mV >= 318 and mV < 408:
            ToReturn = 2
        elif mV >= 408 and mV < 503:
            ToReturn = 3
        elif mV >= 503 and mV < 606:
            ToReturn = 4
        elif mV >= 606 and mV < 696:
            ToReturn = 5
        elif mV >= 696 and mV < 795:
            ToReturn = 6
        elif mV >= 795 and mV < 881:
            ToReturn = 7
        elif mV >= 881 and mV < 976:
            ToReturn = 8
        elif mV >= 976 and mV < 1079:
            ToReturn = 9
        elif mV >= 1079 and mV < 1170:
            ToReturn = 10
        else: # anything greater than 1170
            ToReturn = 11

        # return!
        return ToReturn