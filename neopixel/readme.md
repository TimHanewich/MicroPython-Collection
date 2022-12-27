# Neopixel library for controlling WS2812B addressable LED strip
From [Blaz Rolih](https://github.com/blaz-r)

## Example Code (from https://www.freva.com/how-to-control-a-neopixel-led-strip-with-a-raspberry-pi-pico/)
```
import time
from neopixel import Neopixel
 
numpix = 30
pixels = Neopixel(numpix, 0, 28, "GRB")
 
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
color0 = red
 
pixels.brightness(50)
pixels.fill(orange)
pixels.set_pixel_line_gradient(3, 13, green, blue)
pixels.set_pixel_line(14, 16, red)
pixels.set_pixel(20, (255, 255, 255))
 
while True:
    if color0 == red:
       color0 = yellow
       color1 = red
    else:
        color0 = red
        color1 = yellow
    pixels.set_pixel(0, color0)
    pixels.set_pixel(1, color1)
    pixels.show()
    time.sleep(1)
```

## Test Readings on WS2812B
This is using the strip here: https://www.amazon.com/gp/product/B078S6Z9KG/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1.  
All tests at 5V.
|LED's|Color|Current Draw|Notes|
|-|-|-|-|
|3|255, 255, 255|0.117 A||
|3|255, 0, 0|0.044 A||
|3|0,255,0|0.044 A||
|3|0,0,255|0.044 A||
|3|128,128,128|0.06 A||
|3|128,0,0|0.022 A||
|3|1,1,1|0.000 A (not measureable)||
|3|64,64,64|0.031 A||
|279|1,0,0|0.1 A||
|279|1,1,1|0.115 A||
|279|0,1,0|0.094 A||
|279|0,0,1|0.092 A||
|279|50,50,50|0.735 A|voltage drop clear (red-shifting)|
|279|100,100,100|0.950 A|voltage drop clear (red-shifting)|
|279|25,25,25|0.542 A|Very slight voltage drop visible|
|279|10,10,10|0.325 A||
