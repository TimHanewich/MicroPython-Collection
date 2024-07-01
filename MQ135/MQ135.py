import time
import machine

class MQ135:

    def __init__(self, adc:machine.ADC) -> None:
        self._adc = adc

        # settings for reading
        self.samples:int = 10 # how many samples to take when reading
        self.across_ms:int = 500 # across what period of time (in miliseconds) to take these samples
        self.baseline:int = 30000 # the observed u16 ADC baseline reading of the sensor in clean or relatively clean air
        self.alpha:float = 0.9 # weighted average calculation (if they provide the last value)

    def read(self, last:float = None) -> float:
        """Returns a reading from the sensor between 0.0 and 1.0, expressing the quality of the air (lower is clean air, higher is dirty air)."""

        # perform read
        delay_ms:int = int(self.across_ms / self.samples)
        allsummed:int = 0
        for _ in range(0, self.samples):
            val = self._adc.read_u16()
            allsummed = allsummed + val
            time.sleep_ms(delay_ms)
        val:float = allsummed / self.samples

        # constrain within floor (baseline is the floor)
        val = max(val, self.baseline) 

        # calculate as percentage of gap
        percentage:float = (val - self.baseline) / (65025 - self.baseline) #65025 is the max value for u16

        # if they provided the last value, perform a weighted average calculation
        if last != None:
            percentage = (last * self.alpha) + (percentage * (1 - self.alpha))

        return percentage