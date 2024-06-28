import neopixel
import time

pixels = neopixel.Neopixel(12, 0, 22, "GRB")

def fill_and_wait(color:tuple[int, int, int]) -> None:
    pixels.fill(color)
    pixels.show()
    time.sleep(5)

# inf loop
while True:
    fill_and_wait((1, 1, 1)) # all white, min brightness
    fill_and_wait((1, 0, 0)) # red
    fill_and_wait((0, 1, 0)) # green
    fill_and_wait((0, 0, 1)) # blue
    fill_and_wait((10, 10, 10)) # all white, 10
    fill_and_wait((10, 10, 0)) # 10
    fill_and_wait((0, 10, 10)) # 10
    fill_and_wait((10, 0, 10)) # 10
    fill_and_wait((0, 0, 0)) # off
    