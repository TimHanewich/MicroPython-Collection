# BatteryMonitor
This module provides a simple class, `BatteryMonitor` for estimating a battery's state of charge as a percentage, based upon the read voltage of the battery.

## Example Usage
```
from BatteryMonitor import *

bm = BatteryMonitor()
print("State of Charge for 3.5V: " + str(bm.soc(3.5))) # 0.3, or 30%
```

## Discharge Profiles
Battery discharge curves can vary significantly depending on the type of battery, its chemistry, design, and application. While there are some commonalities, each battery type has its unique characteristics, and their discharge curves can differ in several ways.

The `BatteryMonitor` class supports extension of other battery discharge curves through the use of "discharge profiles". As seen in the `PROFILE_18650` variable of the [`BatteryModule.py`](./BatteryMonitor.py) file, this is nothing more than a simple list of tuples, corresponding to known voltage-SOC pairs. 

When initializing a new instance of the `BatteryMonitor` class, you can easily provide your own battery discharge profile, mapping corresponding points on the battery discharge curve as `(voltage, SOC)` tuples. 

For example:

```
from BatteryMonitor import *

PROFILE_LEAD_ACID = [
    (12.7, 1.0),  # 12.7V - 100% SOC
    (12.5, 0.9),   # 12.5V - 90% SOC
    (12.3, 0.8),   # 12.3V - 80% SOC
    (12.1, 0.7),   # 12.1V - 70% SOC
    (11.9, 0.6),   # 11.9V - 60% SOC
    (11.7, 0.5),   # 11.7V - 50% SOC
    (11.5, 0.4),   # 11.5V - 40% SOC
    (11.3, 0.3),   # 11.3V - 30% SOC
    (11.1, 0.2),   # 11.1V - 20% SOC
    (10.9, 0.1),   # 10.9V - 10% SOC
    (10.5, 0.0)    # 10.5V - 0% SOC
]

bm = BatteryMonitor(PROFILE_LEAD_ACID)
print(bm.soc(12.35)) # 0.825 (82.5%)
```

If you do not specify a profile when initializing a new instance of the `BatteryMonitor` class, the standard 18650 (single-cell lithium ion) battery discharge profile will be selected.

The `BatteryMonitor` module comes with three discharge profiles loaded into memory, available for use:
- `PROFILE_18650` - 18650 battery discharge, single cell Lithium Ion battery. (4.2V - 3.0V)
- `PROFILE_LEAD_ACID` - Lead-acid battery discharge (car/motorcycle/atv/etc battery). (12.7V - 10.5V)
- `PROFILE_1S_LIPO` - Single-cell Lithium Polymer (LiPo) battery. (4.2V - 3.6V)