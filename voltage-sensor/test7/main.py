import time
import voltage

# set up voltage sensor
vs = voltage.VoltageSensor(26)

def test() -> None:

    while True:
        
        # burst read
        burst:int = vs._sample_analog(1.0, 40)

        # display
        print("0: " + str(burst))

        # sleep
        time.sleep(0.25)

test()