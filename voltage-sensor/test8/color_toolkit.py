# Made by Tim Hanewich
# Version: 1

import random

def random_color() -> tuple[int, int, int]:
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r, g, b)

# actually makes the LED dimmer (darker, less bright)
def dim_color(color:tuple[int, int, int], percent:float) -> tuple[int, int, int]:
    return gradient_point(color, (0, 0, 0), percent)


# actually makes the LED brighter (whiter, more bright)
def brighten_color(color:tuple[int, int, int], percent:float) -> tuple[int, int, int]:
    return gradient_point(color, (255, 255, 255), percent)

def relative_luminance(color:tuple[int, int, int]) -> float:
    ToReturn = (0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2])
    return ToReturn

# makes the color whiter while attempting to respect the same luminance
def whiten_color(color:tuple[int, int, int], percent:float) -> tuple[int, int, int]:
    
    # calculate the color we want
    color_:tuple[int, int, int] = brighten_color(color, percent)

    # determine the luminances
    l_start:float = relative_luminance(color)
    l_end:float = relative_luminance(color_)

    # dim until the luminance of the end is below or equal to what it was to begin with
    p_dip:int = 1
    while l_end > l_start:
        color_ = adjust_brightness(color_, (p_dip / 100) * -1) # dim by the next percentage
        l_end = relative_luminance(color_)
        p_dip = p_dip + 1 # dip by another 1% next time

    return color_



# percent can be between -1.0 and 1.0.
# 1.0 = boost brightness 100% (will produce white)
# -1.0 dim 100% (will produce black)
# anything in between is a gradient between white and black
def adjust_brightness(color:tuple[int, int, int], percent:float) -> tuple[int, int, int]:

    # get the % to use
    tup = percent
    if tup > 1.0:
        tup = 1.0
    elif tup < -1.0:
        tup = -1.0

    if tup > 0.0:
        return gradient_point(color, (255, 255, 255), tup)
    elif tup < 0.0:
        return gradient_point(color, (0, 0, 0), tup * -1)
    else:
        return color

    

    

def gradient_point(color1:tuple[int, int, int], color2:tuple[int, int, int], percent:float) -> tuple[int, int, int]:
    r = round(color1[0] + ((color2[0] - color1[0]) * percent))
    g = round(color1[1] + ((color2[1] - color1[1]) * percent))
    b = round(color1[2] + ((color2[2] - color1[2]) * percent))
    return (r, g, b)

def gradient_slices(color1:tuple[int, int, int], color2:tuple[int, int, int], count: int) -> list[tuple[int, int, int]]:

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

def point_on_visible_spectrum(percent:float) -> tuple[int, int, int]:
    
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

def rainbow_slices(count:int) -> list[tuple[int, int, int]]:

    # create list of percentages we should get
    percents:list[float] = []
    gap = 1.0 / max((count - 1), 1)
    for x in range(0, count):
        percents.append(x * gap)

    ToReturn:list[tuple[int, int, int]] = []
    for percent in percents:
        ToReturn.append(point_on_visible_spectrum(percent))

    return ToReturn


def generate_rainbow_swirl(led_count:int) -> list[list[tuple[int, int, int]]]:
    slices:list[tuple[int, int, int]] = rainbow_slices(led_count)

    # generate
    ToReturn:list[list[tuple[int, int, int]]] = []
    for offset in range(0, led_count):
 
        # assemble the index pattern
        pattern:list[int] = []
        current = offset
        while current > 0:
            pattern.append(current)
            current = current - 1
        
        while len(pattern) < led_count:
            pattern.append(current)
            current = current + 1

        # assemble the actual colors
        ToAdd:list[tuple[int, int, int]] = []
        for i in pattern:
            ToAdd.append(slices[i])
        
        # add this frame
        ToReturn.append(ToAdd)

    return ToReturn

