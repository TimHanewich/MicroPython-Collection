# VL530LX Time of Flight Sensor
The VL53L0X is a time-of-flight sensor allowing distances to be accurately measured.

I did not write a library for these sensors myself, but am using two that I found:
- [VL53L0X.py by uceeatz](https://github.com/uceeatz/VL53L0X).
- [vl53l0x.py by Kevin McAleer](https://github.com/kevinmcaleer/vl53l0x) - based on the library by uceeatz, but with an additional `ping()` function built in to quickly capture the distance without having to run the `start()`, `read()`, and `stop()` functions from the original library.

**Please note that in both of these libraries, the reading from the sensor seems to be 50mm too high! When putting finger directly on/above sensor, it reads 50-51mm. So subtract 50 from the reading to get an accurate measurement.**

From what I can tell from testing, the maximum distance it can measure appears to be about 1,200 mm (after subtracting out the 50mm). After surpassing around this number, it reads 8140mm (after subtracting out the 50mm).

From what I can tell, at least with my sensor and the example code [here](./src/main.py), the measurement isn't actually accurate. 1200mm is close to 4 feet, but in my tests it was reading 1200 mm at like maybe 2 feet. So this can be used for relative distances but might need some tweaking for accurate distance measuring.

## Sample Code
For an example on how to use Kevin McAleer's version, see the code in [the src folder](./src/).