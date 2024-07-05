"""
colors.py: a library for manipulating RGB-based colors.
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/tree/master/colors

MIT License
Copyright Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import random

def random_color() -> tuple[int, int, int]:
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r, g, b)

def brighten(color:tuple[int, int, int], strength:float = 1.0) -> tuple[int, int, int]:
    """Brighten/dim a color according to a specified strenght level. Strength > 1.0 will brighten, Strength < 1.0 will dim."""

    # convert
    r:float = color[0] * strength
    g:float = color[1] * strength
    b:float = color[2] * strength

    # min/max
    r = min(max(r, 0), 255)
    g = min(max(g, 0), 255)
    b = min(max(b, 0), 255)

    # round
    r:int = int(r)
    g:int = int(g)
    b:int = int(b)

    # return
    return (r, g, b)

def relative_luminance(color:tuple[int, int, int]) -> float:
    """Calculates the relative luminance of a given color. The relative luminance is a measure of how bright a color appears to the human eye."""
    return (0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2])
    
def gradient_point(color1:tuple[int, int, int], color2:tuple[int, int, int], percent:float) -> tuple[int, int, int]:
    """Calculates a color that is a certain percentage between two given colors"""
    r = round(color1[0] + ((color2[0] - color1[0]) * percent))
    g = round(color1[1] + ((color2[1] - color1[1]) * percent))
    b = round(color1[2] + ((color2[2] - color1[2]) * percent))
    return (r, g, b)

def gradient_slices(color1:tuple[int, int, int], color2:tuple[int, int, int], count: int) -> list[tuple[int, int, int]]:
    """Generates a list of colors that form a gradient between two given colors"""

    # create list of percentages we should get
    percents:list[float] = []
    gap = 1.0 / max(1, (count - 1))
    for x in range(0, count):
        percents.append(x * gap)
  
    # calculate the proper gradient for each one
    ToReturn:list[tuple[int, int, int]] = []
    for percent in percents:
        ToReturn.append(gradient_point(color1, color2, percent))
    
    return ToReturn

def spectrum_point(percent:float) -> tuple[int, int, int]:
    """Generates a color on the visible spectrum based on a given percentage. The percentage is used to determine the point on the spectrum, with 0% being red and 100% being violet."""
    
    r = 255
    g = 0
    b = 0
    ToAdd = int(round(1020 * percent, 0))

    # add to g
    while g < 255 and ToAdd > 0:
        g = g + 1
        ToAdd = ToAdd - 1

    # subtract from r
    while r > 0 and ToAdd > 0:
        r = r - 1
        ToAdd = ToAdd - 1

    # add to b
    while b < 255 and ToAdd > 0:
        b = b + 1
        ToAdd = ToAdd - 1
    
    # subtract from g
    while g > 0 and ToAdd > 0:
        g = g - 1
        ToAdd = ToAdd - 1

    return (r, g, b)

def spectrum_slices(count:int) -> list[tuple[int, int, int]]:
    """Generates a list of colors, each representing a point on the visible spectrum, divided into a specified number of slices."""

    # create list of percentages we should get
    percents:list[float] = []
    gap = 1.0 / max((count - 1), 1)
    for x in range(0, count):
        percents.append(x * gap)

    ToReturn:list[tuple[int, int, int]] = []
    for percent in percents:
        ToReturn.append(spectrum_point(percent))

    return ToReturn
