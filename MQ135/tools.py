class WeightedAverageCalculator:

    def __init__(self, alpha:float = 0.9, starting_value:float = None) -> None:
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
        