# NeopixelManager
`NeopixelManager` is a superstructure class *around* the standard `Neopixel` class that has the added capability of estimating current consumption for a full strand of neopixels at whatever color/brightness setting. This estimate is done using an understanding of current consumption at varying color and brightness settings as described below.

## Example Usage
Below is an example of how to use `NeopixelManager` (included in the `neopixel` module):
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

Please note that even after setting a different color for a pixel or pixels, the current consumption will not change until it is shown via the `show()` function! This is because when set, the color change has now actually shown on the strand yet until the `show()` function is called!

## Estimating Per-Pixel Current Consumption of Neopixels
All measurements were @ 5V supply.

Current Consumption of Raspberry Pi Pico on its own: **0.022 amps**

The following tests are observations of current consumption with several different color patterns (each pixel the same color):

With a strand of 12 pixels:
|Pixels|Color|Amps (including Pi)|W/O Pi|Amps Per Pixel|
|-|-|-|-|-|
|12|255,255,255|0.477|0.455|0.037916667|
|12|255,0,0|0.179|0.157|0.013083333|
|12|0,255,0|0.179|0.157|0.013083333|
|12|0,0,255|0.178|0.156|0.013|
|12|128,128,128|0.256|0.234|0.0195|
|11|1,1,1|0.028|
|11|1,0,0|0.027|
|11|0,1,0|0.027|
|11|0,0,1|0.027|
|11|10,10,10|0.045|
|11|10,10,0|0.035|
|11|0,10,10|0.035|
|11|10,0,10|0.035|
|11|50,0,0|0.05|0.028|0.0025454545|
|11|150,0,0|0.103|0.081|0.0073636364|
|11|255,0,0|0.161|0.139|0.0126363636|
|11|0,50,0|0.05|0.028|0.0025454545|
|11|0,150,0|0.104|0.082|0.0074545455|
|11|0,255,0|0.161|0.139|0.0126363636|
|11|0,0,50|0.05|0.028|0.0025454545|
|11|0,0,150|0.103|0.081|0.0073636364|
|11|0,0,255|0.160|0.138|0.0125454545|
|11|50,50,50|0.104|0.082|0.0074545455|
|11|150,150,150|0.265|0.243|0.0220909091|
|11|255,255,255|0.435|0.413|0.0375454545|
|11|0,0,0|0.027|0.005|0.0004545455|

Columns in the above table explained:
- **Color** - the RGB color that was shown on all 12 pixels.
- **Amps (including Pi)** - the total amps reading from the DC power supply (powering both the Pi Pico and Neopixels, nothing more)
- **W/O Pi** - The total amps, minus the known value that the Pi consumes, 0.022 amps (@ 5V)
- **Amps Per Pixel** - the amps from the **W/O Pi** column, divided by 12 (the number of pixels), to get a per-pixel amount.

In the above table, you may wonder why measuring the color (0, 0, 0), no color at all, is important. That is because these neopixels have an *idle current draw*. Even while not showing a color, they still consume a small amount of power, on a per-pixel basis.

## Digitally Estimating Current Consumption While Powering Neopixels
The following describes how I arrived at the ability to estimate current consumption for a strand of Neopixels:

![luminary values](https://i.imgur.com/eNnyeB5.png)

In the example above, you'll see I did some math. For each of the colors in the table of consumption in the section above, I added up the R, G, and B values. The consumption for all three is roughly similar (only B seems to under-consume a bit), so we can add them together. I called this new unit "Luminary Values". 

After adding these all up, I then summed up the *entirety* of every tests. And then did the same for the amps per pixel on each test. Then, I divided those two to get a rough estimate for how many amps each luminary value takes. The answer is `0.000045851370851` amps. I should probably express that in mA. But whatever.

Knowing that, I can now estimate the amperage consumption of a single neopixel based upon the sum of the R,G,B value it is displaying. You can see these estimates in the "Estimated" blue column.

In the "Off Actual" and the "Off as %", I am comparing that estimation against the actual reading in the "Single Pixel Amps" column (as a difference). You can see that in the higher-consumption scenarios, the accuracy is far better. This is due to a rounding error I believe. At such low current rates, my DC supply was not able to give me so many decimal points for a number so low, so it rounded up. Had I had more granularity during recording, the estimates would likely be more accurate at such low consumption. But, at least for high consumption, they seem to be at least moderately accurate.