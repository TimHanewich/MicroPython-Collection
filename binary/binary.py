"""
binary.py - a lightweight module for converting bytes to and from bits.
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/blob/master/binary/

MIT License
Copyright 2024 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

def bits_to_byte(bools:list[bool]) -> int:
    """Converts a series of bit values (preferrably 8 to make a full byte), expressed as bools to a byte value."""
    val:int = 0
    for b in bools:
        val = val << 1 | int(b)
    return val

def byte_to_bits(byte:int):
    """Converts a byte value into its equivalent 8 bits, expressed as bools."""
    if byte < 0:
        raise Exception("Unable to convert value '" + str(byte) + "' into a byte. Cannot be less than 0!")
    elif byte > 255:
        raise Exception("Unable to convert value '" + str(byte) + "' into a byte. Cannot be greater than 255!")
    return [(byte >> i) & 1 == 1 for i in range(7, -1, -1)] # made w/ GenAI