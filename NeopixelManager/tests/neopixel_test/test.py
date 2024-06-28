import neopixel
import color_toolkit

def test_gp(gp:int) -> None:
    rc:tuple[int, int, int] = color_toolkit.random_color()
    pixels = neopixel.Neopixel(12, 0, gp, "GRB")
    pixels.fill(rc)
    pixels.show()
    print("Showed color " + str(rc) + " on GP " + str(gp))