# Weighted Average Calculator
The `WeightedAverageCalculator.py` module provides a simple class that allows for the filtering of a stream of values through an averaging filter.

## Example Usage
```
>>> import WeightedAverageCalculator
>>> wac = WeightedAverageCalculator.WeightedAverageCalculator
>>> wac = WeightedAverageCalculator.WeightedAverageCalculator()
>>> wac.feed(3.0)
3.0
>>> wac.feed(2.9)
2.99
>>> wac.feed(2.0)
2.891
>>> wac.feed(3.2)
```

In the example above, you can see that the WAC acts as an averaging filter. You can adjust how this averaging behaves by adjusting the value for `alpha` upon creating the class.