"""
Just a simple class for passing a stream of values through a weighted average filter continuously.
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/tree/master/WeightedAverageCalculator

MIT License
Copyright Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class WeightedAverageCalculator:
    def __init__(self, alpha:float = 0.9, starting_value:float = None) -> None:
        """Alpha is a value that determines how strong the averaging will be. A high alpha value favors historical values yet is insensitive to quick fluctuations while a low alpha value is more sensitive to quick fluctuations (more granular, but also noisier)."""
        self._alpha = alpha
        self._last = starting_value

    def feed(self, value:float) -> float:
        """Accepts a new reading value and returns the weighted average of this and the previous readings."""

        if self._last == None: # we have no previous readings. So just return this value! (the first one!)
            self._last = value
            return value
        else: # we have previous readings stored
            ToReturn:float = (self._last * self._alpha) + (value * (1 - self._alpha)) # calculate the weighted average
            self._last = ToReturn # set the last before returning
            return ToReturn
        