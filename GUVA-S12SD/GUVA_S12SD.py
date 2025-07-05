"""
GUVA_S12SD.py MicroPython driver for the GUVA-S12SD analog UV sensor.
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/tree/master/GUVA-S12SD

MIT License
Copyright 2025 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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