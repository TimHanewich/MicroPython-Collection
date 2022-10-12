import machine
import time

class voltage_sensor:

    __adc_input__ = None

    def __init__(self, adc_input:int) -> None:
        self.__adc_input__ = machine.ADC(adc_input)
        pass

    def measure(self) -> float:
        value = self.__adc_input__.read_u16()
        tr = self.__analog_to_volts__(value)
        return tr

    # takes a series of measurements and returns the average
    def measure_set(self, count:int = 5, delay_seconds:float = 0.25) -> float:
        vals = []
        for x in range(0, count):
            val = self.measure()
            vals.append(val)
            time.sleep(delay_seconds)
        avg_val = self.__avg__(vals)
        return avg_val
        
    def __analog_to_volts__(self, analog:float) -> float:

        # assumed values - adjust if necessary to get a more accurate calculated voltage value
        max_adc = 65535
        min_adc = 600
        max_voltage = 16.5
        min_voltage = 0.25

        tr = ((analog - min_adc) / (max_adc - min_adc)) * (max_voltage - min_voltage)
        return tr

    def __avg__(self, data) -> float:
        sum = 0
        for v in data:
            sum = sum + v
        tr = sum / len(data)
        return tr


