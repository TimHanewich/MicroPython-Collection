import neopixel
import time

pixels = neopixel.Neopixel(11, 0, 22, "GRB") 

def fill_and_wait(color:tuple[int, int, int]) -> None:
    pixels.fill(color)
    pixels.show()
    print("Now showing pixels on GP22 @ " + str(color))
    time.sleep(8)

# inf loop
while True:
    fill_and_wait((50, 0, 0)) # Red x1
    fill_and_wait((150, 0, 0)) # Red x2
    fill_and_wait((255, 0, 0)) # Red x3

    fill_and_wait((0, 50, 0)) # Green x1
    fill_and_wait((0, 150, 0)) # Green x2
    fill_and_wait((0, 255, 0)) # Green x3

    fill_and_wait((0, 0, 50)) # Blue x1
    fill_and_wait((0, 0, 150)) # Blue x2
    fill_and_wait((0, 0, 255)) # Blue x3

    fill_and_wait((50, 50, 50)) # White x1
    fill_and_wait((150, 150, 150)) # White x2
    fill_and_wait((255, 255, 255)) # White x3

    fill_and_wait((0, 0, 0)) # all off
    
    