import time
import voltage
import BatteryMonitor
import WeightedAverageCalculator


# set up voltage reader
vs = voltage.VoltageSensor(26) # GPIO 26

# set up battery monitor to convert the voltage we read to state of charge %'s
bm = BatteryMonitor.BatteryMonitor()

# set up weighted avg calculator
wac = WeightedAverageCalculator.WeightedAverageCalculator(alpha=0.9)

def test() -> None:

    while True:

        # read voltage
        volts:float = vs.voltage(duration=0.05, samples=10) # raw
        volts = wac.feed(volts) # pass through averaging filter

        # calculate SOC
        soc:float = bm.soc(volts)
        socs:str = str(round(soc * 100, 1)) + "%"

        # print
        print("Volts: " + str(volts) + ", SOC: " + socs)

        # sleep
        time.sleep(1.0)

test()