# NeopixelManager
`NeopixelManager` is a superstructure class *around* the standard `Neopixel` class that has the added capability of estimating current consumption for a full strand of neopixels at whatever color/brightness setting. This estimate is done using an understanding of current consumption at varying color and brightness settings as described below.

## Example Usage
```
import neopixel

pixels = neopixel.Neopixel(5, 0, 22, "GRB") # set up 5 pixels
nm = neopixel.NeopixelManager(pixels) # initialize an instance of the NeopixelManager class
nm.fill((255, 255, 255)) # fill with all white
nm.show() # show
print("Current consumption, in mA: " + str(nm.current)) # 175.3816

nm.set_pixel(0, (0, 0, 255))
nm.set_pixel(0, (128, 0, 0))
nm.show()
print("Current consumption, in mA: " + str(nm.current)) # 146.1742
```