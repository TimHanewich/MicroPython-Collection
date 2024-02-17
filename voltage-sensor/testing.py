import machine
import time

adc = machine.ADC(26)

def sample(duration:float, samples:int) -> tuple[int, int, int]:
    delay:float = duration / samples
    min:int = 9999999
    max:int = -1
    total:int = 0
    for x in range(samples):
        reading = adc.read_u16()
        if reading < min:
            min = reading
        if reading > max:
            max = reading
        total = total + reading
        time.sleep(delay)
    
    # calc
    avg:int = int(round(total / samples, 0))
    return (min, avg, max)

class MovingAverageFilter:
    def __init__(self, weight:float = 0.9):
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
        

def analog_to_voltage(analog:int) -> float:
    max_analog:int = 65535
    min_analog:int = 600
    max_voltage:float = 16.3
    min_voltage:float = 0.0
    TR:float = ((analog - min_analog) / (max_analog - min_analog)) * (max_voltage - min_voltage)
    TR = min(max(TR, 0.0), max_voltage)
    return TR


maf = MovingAverageFilter(0.95)
while True:
    read = adc.read_u16()
    filtered = maf.filter(read)
    voltage = analog_to_voltage(filtered)
    #print(str(round(read, 1)) + " - " + str(filtered))
    print(round(voltage, 1))
    time.sleep(0.1)

