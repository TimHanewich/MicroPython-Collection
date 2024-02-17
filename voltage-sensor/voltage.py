import machine
import time

class MovingAverageFilter:
    def __init__(self, weight:float = 0.98):
        self.weight = weight
        self._last_val:float = None
    
    def filter(self, reading:float) -> float:
        if self._last_val == None:
            self._last_val = reading
            return reading
        else:
            val = (self._last_val * self.weight) + (reading * (1 - self.weight))
            self._last_val = val
            return val
        
class VoltageSensor:
    def __init__(self, adc_gpio:int) -> None:
        self._adc = machine.ADC(adc_gpio)

    def _sample_analog(self) -> int:
        """Takes average of analog reading over short period of time."""
        duration:float = 1.5
        samples:int = 30
        delay:float = duration / samples
        total:int = 0
        for x in range(samples):
            total = total + self._adc.read_u16()
            time.sleep(delay)
        return int(round(total / samples, 0))

    def voltage(self) -> float:
        analog:int = self._sample_analog()
        max_analog:int = 65535
        min_analog:int = 600
        max_voltage:float = 16.3
        min_voltage:float = 0.0
        TR:float = ((analog - min_analog) / (max_analog - min_analog)) * (max_voltage - min_voltage)
        TR = min(max(TR, min_voltage), max_voltage)
        return TR
    
