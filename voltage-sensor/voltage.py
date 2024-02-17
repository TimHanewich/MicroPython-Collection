import machine
import time
       
class VoltageSensor:
    def __init__(self, adc_gpio:int) -> None:
        self._adc = machine.ADC(adc_gpio)

    def _sample_analog(self) -> int:
        """Takes average of analog reading over short period of time."""
        # I've learned that, no matter what duration you take samples over, the min, mean, and max should be the same. So taking these samples rapidly over 1.5 seconds is fine.
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
    
