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

    #1's
    fill_and_wait((1,1,1))
    fill_and_wait((1,0,0))
    fill_and_wait((0,1,0))
    fill_and_wait((0,0,1))

    #10's
    fill_and_wait((10,10,10))
    fill_and_wait((10,10,0))
    fill_and_wait((0,10,10))
    fill_and_wait((10,0,10))

    fill_and_wait((0, 0, 0)) # all off
    
    