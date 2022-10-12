import machine

class voltage_sensor:

    __adc_input__ = None

    def __init__(self, adc_input:int) -> None:
        self.__adc_input__ = machine.ADC(adc_input)
        pass

    def measure(self) -> float:
        value = self.__adc_input__.read_u16()
        tr = self.__analog_to_volts__(value)
        return tr

        
    def __analog_to_volts__(self, analog:int) -> float:

        # assumed values - adjust if necessary to get a more accurate calculated voltage value
        max_adc = 65535
        min_adc = 600
        max_voltage = 16.5
        min_voltage = 0.25

        tr = ((analog - min_adc) / (max_adc - min_adc)) * (max_voltage - min_voltage)
        return tr

vs = voltage_sensor(0)
print(vs.__analog_to_volts__(12300))


