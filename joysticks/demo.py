import machine
import time
import joysticks

# Set up ADCs for two axes of the joystick
adc1 = machine.ADC(26)
adc2 = machine.ADC(27)

while True:

    # Get the raw uint16 reading (0 to 65,535)
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
    #transformed1:float = transform(val1_fr, -0.10, 0.15, 0.85)
    #transformed2:float = transform(val2_fr, -0.09, 0.15, 0.85)

    transformed1:float = joysticks.transform(val1_fr, -0.10, 0.05, 0.85)
    transformed2:float = joysticks.transform(val2_fr, -0.09, 0.05, 0.85)

    # print the transformation
    print(str(int(round(transformed1*100,0))) + "%, " + str(int(round(transformed2*100,0))) + "%")

    # wait
    time.sleep(0.1)
    

    
