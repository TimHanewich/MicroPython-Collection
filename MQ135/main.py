import machine
import time
from tools import WeightedAverageCalculator

adc = machine.ADC(machine.Pin(26))

def raw() -> None:
    while True:
        val = adc.read_u16()
        print(val)
        time.sleep(0.25)

def shifted(baseline:int = 32000) -> None:
    # the baseline is what this particular reads with clean air (which would be 400 ppm)
    scaler:float = 400 / baseline
    while True:
        val = adc.read_u16()
        co2ppm:int = int(round(val * scaler, 0))
        print(co2ppm)
        time.sleep(0.25)

def gap(baseline:int = 32000) -> None:
    # baseline here is interpretted as the reading it gives with very clean air.
    maxv:int = 65025
    minv:int = baseline
    while True:
        val = adc.read_u16()
        percentage = (val - minv) / (maxv - minv)
        percentage = min(percentage, 1.0)
        percentage = max(percentage, 0.0)
        percentages = str(round(percentage * 100, 0)) + "%"
        print(percentages)
        time.sleep(0.25)

def gap2(baseline:int = 32000) -> None:
    # baseline here is interpretted as the reading it gives with very clean air.
    maxv:int = 65025
    minv:int = baseline
    wac = WeightedAverageCalculator()
    while True:
        val = adc.read_u16()
        val = wac.feed(val)
        print("WAV: " + str(val))
        percentage = (val - minv) / (maxv - minv)
        percentage = min(percentage, 1.0)
        percentage = max(percentage, 0.0)
        percentages = str(int(round(percentage * 100, 0))) + "%"
        print(percentages)
        time.sleep(0.25)


def gap3(baseline:int = 32000) -> None:
    # baseline here is interpretted as the reading it gives with very clean air.
    maxv:int = 65025
    minv:int = baseline
    wac = WeightedAverageCalculator(alpha=0.9)
    while True:
        val = adc.read_u16()

        # constrain the val
        val = min(max(val, minv), maxv)

        # calculate weighted average of the constrained value
        val = wac.feed(val)

        # transform the weighted average reading into a percentage. Constraining is not necessary because it was already constrained above
        percentage = (val - minv) / (maxv - minv)
        percentages = str(int(round(percentage * 100, 0))) + "%"
        print(percentages)
        time.sleep(0.25)


def stest(samples:int, duration_ms:int) -> tuple[int, int, int]:
    """
    Returns (min, avg, max) for a series of samples over a sample duration. This function is meant to test the average values in various sample sets of various durations. 
    Through testing, this has proved that average 10 samples over 1 second should roughly equal sampling even more samples over a longer duration.
    """

    duration_in_between_ms:int = int(duration_ms / samples)
    minv:int = None
    maxv:int = None
    allsummed:int = 0
    for x in range(0, samples):
        val = adc.read_u16()
        allsummed = allsummed + val
        if minv == None or val < minv:
            minv = val
        if maxv == None or val > maxv:
            maxv = val
        time.sleep_ms(duration_in_between_ms)

    # calculate avg
    avg = int(allsummed / samples)
    
    # return
    return (minv, avg, maxv)

def sample(last:float = None) -> float:
    """Returns a reading from the sensor between 0.0 and 1.0, expressing the quality of the air (lower is clean air, higher is dirty air)."""

    # settings
    samples:int = 10
    across_ms:int = 500
    baseline:int = 30000 # the observed baseline reading of the sensor in clean or relatively clean air
    alpha:float = 0.9 # weighted average calculation (if they provide the last value)

    # perform read
    delay_ms:int = int(across_ms / samples)
    allsummed:int = 0
    for _ in range(0, samples):
        val = adc.read_u16()
        allsummed = allsummed + val
        time.sleep_ms(delay_ms)
    val:float = allsummed / samples

    # constrain within floor (baseline is the floor)
    val = max(val, baseline) 

    # calculate as percentage of gap
    percentage:float = (val - baseline) / (65025 - baseline) #65025 is the max value for u16

    # if they provided the last value, perform a weighted average calculation
    if last != None:
        percentage = (last * alpha) + (percentage * (1 - alpha))

    return percentage