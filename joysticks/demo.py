import machine
import time
import joysticks

adc1 = machine.ADC(26)
adc2 = machine.ADC(27)


def transform(value:float, offset:float = 0.0, deadzone:float = 0.2, ceiling:float = 0.8) -> float:
    """
    Provide the input value from -1.0 to 1.0.
    
    offset: When untouched, the value the axis holds to naturally with no input at all. (a bias, say, for +8% input) This will be subtracted out to "center" around this value.
    deadzone: Inputs only considered above this, in either direction. Anything within will be considered as no input.
    ceiling: Beyond this level of input in either direction, max movement is considered "full" (100% input)
    """

    # subtract out the "offset" to "center around" the bias value.
    value_unoffset:float = value - offset
    
    # Settings
    discernable_range:float = ceiling - deadzone
    
    # Calculation
    over_dead_zone:float = max(abs(value_unoffset) - deadzone, 0.0)
    percent_of_dr:float = over_dead_zone / discernable_range
    constrained:float = min(percent_of_dr, 1.0)
    
    # final step = flip the signs if needed so negatives are preserved
    if value_unoffset < 0.0:
        constrained = constrained * -1
    
    return constrained

while True:
    val1 = adc1.read_u16()
    val2 = adc2.read_u16()

    # print the raw uint16 values (between 0 and 65,535)
    #print("Val1: " + str(val1) + ", Val2: " + str(val2))

    # value as a percentage from 0.0 to 1.0
    val1p = val1 / 65535
    val2p = val2 / 65535

    # Convert the 0.0-1.0 to -1.0-1.0
    val1_fr = (val1p * 2) - 1.0
    val2_fr = (val2p * 2) - 1.0

    # Print the full range percents
    #print("FR Percents: " + str(val1_fr) + ", " + str(val2_fr))

    # transform
    transformed1:float = transform(val1_fr, -0.10, 0.15, 0.85)
    transformed2:float = transform(val2_fr, -0.09, 0.15, 0.85)

    # print the transformation
    print(str(int(round(transformed1*100,0))) + "%, " + str(int(round(transformed2*100,0))) + "%")

    # wait
    time.sleep(0.1)
    

    
