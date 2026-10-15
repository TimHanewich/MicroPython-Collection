import machine
import time
import joysticks

adc1 = machine.ADC(26)
adc2 = machine.ADC(27)


def transform(ival:float, deadzone:float = 0.2, ceiling:float = 0.8) -> float:
    """
    Provide the input as a float from 0.0 to 1.0 and get the output as a range from -1.0 and 1.0, but with a center dead zone and outer dead zone applied!
    
    deadzone: Inputs only considered above this, in either direction. Anything within will be considered as no input.
    ceiling: Beyond this level of input in either direction, max movement is considered "full" (100% input)
    """
        
    # convert to -1.0 to 1.0 range
    full_range:float = (ival * 2) - 1.0
    
    # Settings
    discernable_range:float = ceiling - deadzone
    
    # Calculation
    over_dead_zone:float = max(abs(full_range) - deadzone, 0.0)
    percent_of_dr:float = over_dead_zone / discernable_range
    constrained:float = min(percent_of_dr, 1.0)
    
    # final step = flip the signs if needed so negatives are preserved
    if full_range < 0.0:
        constrained = constrained * -1
    
    return constrained

while True:
    val1 = adc1.read_u16()
    val2 = adc2.read_u16()
    
    val1p = val1 / 65535
    val2p = val2 / 65535   # value as a percentage
    
    transformed:float = transform(val2p)
    print(str(int(round(transformed*100,0))) + "%")
    time.sleep(0.1)
    

    
